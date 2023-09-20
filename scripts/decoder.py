# decoder.py
# Author: Ethan Coleman
a = [
    0, 108, 32,
    0, 1, 16, 20, 24, 17, 21, 25, 36, 40, 44, 37, 41, 45, 60, 61, 2, 3, 18, 22, 26, 19, 23, 27, 38, 42, 46, 39, 43, 47, 62, 63,
    0, 16, 28, 29, 32, 33, 30, 31, 34, 35, 0, 1, 60, 61, 2, 3, 62, 63,
    0, 16, 12, 13, 48, 49, 14, 15, 50, 51, 16, 17, 44, 45, 18, 19, 46, 47,
    0, 16, 8, 9, 52, 53, 10, 11, 54, 55, 28, 29, 32, 33, 30, 31, 34, 35,
    0, 16, 4, 5, 56, 57, 6, 7, 58, 59, 12, 13, 48, 49, 14, 15, 50, 51,
    0, 16, 0, 1, 60, 61, 2, 3, 62, 63, 8, 9, 52, 53, 10, 11, 54, 55,
    0, 16, 16, 17, 44, 45, 18, 19, 46, 47, 4, 5, 56, 57, 6, 7, 58, 59,
]

print(a[37])
for i in range(37, 37+16):
    print(f"Row: {(a[i] >> 4)}, Column: {((a[i] & 0x0F) >> 2)}, Plane: {(a[i] & 0x03)}")