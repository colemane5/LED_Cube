# timing.py
# Author: Ethan Coleman
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import os
import pickle

FRAME_DIR = "C:\\Dev\\LED_Cube\\Frame Sets\\"
TIMING_DIR = "C:\\Dev\\LED_Cube\\output\\timing.p"

names = os.listdir(FRAME_DIR)
names_dict = dict(enumerate(names))

if not os.path.exists(TIMING_DIR):
    pickle.dump(dict(), open(TIMING_DIR, "wb"))
    timings = dict()
else:
    timings = pickle.load(open(TIMING_DIR, "rb"))
print(timings)

for n, name in names_dict.items():
    print(f"{n}: {name}")
num = int(input("Choose a pattern to time: "))
curr_dir = FRAME_DIR + names[num]

timing_set = list()
do_default = True if input("Use default timing? (Y/N): ") == 'Y' else False
if do_default:
    for path in os.listdir(curr_dir):
        timing_set.append(0)

else:
    for path in os.listdir(curr_dir):
        img = mpimg.imread(os.path.join(curr_dir, path))
        plt.figure(1)
        plt.clf()

        plt.imshow(img)
        plt.pause(0.1)
        timing_set.append(int(input("Frame times: ")) - 1)

timings[num] = timing_set
pickle.dump(timings, open(TIMING_DIR, "wb"))