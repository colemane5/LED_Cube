/* Led_Cube.ino
 * Author: Ethan Coleman
 */
#include <SPI.h>
#include <MsTimer2.h>
#include <LiquidCrystal.h>

unsigned long Timer = 0;
LiquidCrystal LCD( A5, A4, 5, 6, 7, 8 );

// The minimum time between frame updates.
unsigned short tick_rate = 500;

// The tick rates for different speed settings (precomputed to avoid float precision errors).
unsigned short tick_rates[] = {
  2580, 2150, 1792, 1493, 1244,
  1037, 864, 720, 600, 500,
  417, 347, 289, 241, 201,
  167, 139, 116, 96, 81
};

unsigned char speed_setting = 9;

#include "LedCubeData.h"
#include "ButtonDebounce.h"
#include "Patterns.h"
#include "EncoderMonitor.h"

void NextDisplay()
{
  // Send next pattern to Shift Registers.
  PORTC |= 0x0f;// set bottom bit low, turning off display.
  SPI.transfer16( ~LedCube_NextPlane() );
  // Turn on the current plane.
  PORTC &= ~(1 << LedCube_CurrentPlane );

} // End of NextDisplay

// setup code, run once:
void setup()
{
  MsTimer2::set(4, NextDisplay ); // 4ms period
  MsTimer2::start();

  // A3-A0 to outputs.
  DDRC |= 0x0f;
  // Set up display data.
  LedCube_ClearData();
  // Start up the SPI.
  SPI.begin();
  // Set the parameters for the transfers.
  SPI.beginTransaction(SPISettings(8000000, MSBFIRST, SPI_MODE0));

  // Set up the LCD.
  LCD.begin(16, 2);
  LCD.setCursor(0, 1);
  LCD.print("OFF");
  LCD.setCursor(7, 1);
  LCD.print("Speed:    ");
  LCD.setCursor(14, 1);
  LCD.print(speed_setting + 1);
  
  // Set up the button debounce and encoder turning.
  ButtonInitialize();
  EncoderInitialize();
  
  // Timer for moving the ON led's
  Timer = millis();

} // End of setup

// The number of frame bytes in the current pattern.
unsigned short size_frames;

// The list of frames in the current pattern.
unsigned char *frames;

// The current position in frames.
unsigned short curr_pos;

// Initialize the LEDs and pattern for the current mode.
void Initialize_Mode(unsigned char* pattern_loc)
{
  // Clears the LED Cube
  LedCube_ClearData();

  // Get the data for this pattern from program memory.
  unsigned char pattern[sizeof(pattern_loc)];
  memcpy_P(pattern, pattern_loc, sizeof(pattern_loc));

  // Get the number of frame bytes in this pattern.
  size_frames = ( ((unsigned short)pattern[0]) << 8 ) | pattern[1];

  // Get the number of bytes in the header frame.
  unsigned char size_header_frame = pattern[2];

  // Toggle the LEDs in the header frame.
  for (int i = 3; i < size_header_frame + 3; i++) 
  {
    LedCube_ToggleLed(
      (pattern[i] >> 4), 
      ((pattern[i] & 0x0F) >> 2), 
      (pattern[i] & 0x03)
      ); // The bits are 00 RR CC PP
  }

  // Initialize the frames array position.
  frames = &pattern[size_header_frame + 3];
  curr_pos = 0;
} // End of Initialize_Mode

// The amount of time to hold this frame for (default 1 tick).
unsigned char hold_time = 1;

// Toggles the LEDs for the next frame.
void Next_Frame() 
{
  // Restart pattern.
  if (curr_pos >= size_frames)
    curr_pos = 0;

  // Set the hold time for this pattern.
  hold_time = frames[curr_pos] + 1;

  // Get the number of LEDs to toggle.
  unsigned char n_toggles = frames[curr_pos + 1];

  // Toggle the LEDs.
  for (int i = curr_pos + 2; i < curr_pos + n_toggles + 2; i++) 
  {
      LedCube_ToggleLed(
        (frames[i] >> 4), 
        ((frames[i] & 0x0F) >> 2), 
        (frames[i] & 0x03)
      ); // The bits are 00 RR CC PP
  }

  // Update the current position for the next frame
  curr_pos = curr_pos + n_toggles + 2;
} // End of Next_Frame

// The number of last available mode.
#define MAX_MODE |||||

// State variables.
unsigned char Mode = 0;
bool IsActive = false;

// main code, run repeatedly:
void loop()
{
  unsigned short frame_length = hold_time * tick_rate;
  // Dynamic timer to update display.
  if ( millis() - Timer >= frame_length)
  {
    if (IsActive)
    {
      Next_Frame();
    }

    Timer += frame_length; // Update timer

  } // End of timer if.

  int buttonState = ButtonNextState(digitalRead(4));
  // Move to next mode (short button release).
  if( buttonState == 2 && IsActive )
  {
    Mode++;
    if ( Mode > MAX_MODE )
      Mode = 0;

    LCD.setCursor(0, 0);
    switch (Mode) 
    {
|||||
      default:
        break;
    }
  }

  // Turn LED cube on/off (long button release).
  else if( buttonState == 3 )
  {
    IsActive = !IsActive;
    LCD.setCursor(0, 1);
    LCD.print(IsActive ? "ON " : "OFF");
  }

  // Increment speed.
  if (encoderPosition >= 4) 
  {
    if (speed_setting < 19)
    {
      speed_setting += 1;
      tick_rate = tick_rates[speed_setting];
      LCD.setCursor(7, 1);
      LCD.print("Speed:    ");
      LCD.setCursor(14, 1);
      LCD.print(speed_setting + 1);
    }
    encoderPosition -= 4;
  }
  // Decrement speed.
  else if (encoderPosition <= -4)
  {
    if (speed_setting > 0)
    {
      speed_setting -= 1;
      tick_rate = tick_rates[speed_setting];
      LCD.setCursor(7, 1);
      LCD.print("Speed:    ");
      LCD.setCursor(14, 1);
      LCD.print(speed_setting + 1);
    }
    encoderPosition += 4;
  }
  
} // End of loop.