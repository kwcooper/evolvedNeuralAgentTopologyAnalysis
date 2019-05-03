# make a movie from images

import glob
import imageio
import os
import time


path_name = "img/*.png"
start = time.time()
# grab files, sorted by modification time
#filenames = glob.glob("img/*.png")
filenames = sorted(glob.glob(path_name), key=os.path.getmtime)

# compile frames into imageio objects
print('Making movie, may take a sec...')
images = []
for filename in filenames:
    images.append(imageio.imread(filename))

# save that bad boy (use time to prevent overwriting)
name = 'mov/movie_' + str(int(time.time())) + '.gif'
imageio.mimsave(name, images)

print('Took', (time.time()-start))
print('Saved', name)
print('fin')
