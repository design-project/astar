import pylab as pl
import matplotlib.cm as cm
import numpy as np
import PIL
from PIL import Image

stepsize = 40


class im2bin:
    def __init__(self):
        self.update()
        return

    def update(self):
        #open image and convert into greyscale
        im = Image.open('demo.jpeg')
        im_grey = im.convert('L') # convert the image to *greyscale*
        im_array = np.array(im_grey)

        num_rows, num_cols = np.shape(im_array)

        self.start = (3, 22)
        self.end = (8, 10)
        self.dir = (0,-1)
        self.height = int(num_rows/stepsize)
        self.width = int(num_cols/stepsize)

        map = np.zeros((self.height, self.width))
        sum=0
        print(str(self.height))
        print(str(self.width))
        for i in range(0,self.height):
            for j in range(0, self.width):
                for k in range(stepsize*i, stepsize*i+stepsize):
                    for z in range(stepsize*j, stepsize*j+stepsize):
                        sum = sum + im_array[k,z]
                        map[i,j] = sum/stepsize
                        sum=0

        np.savetxt("map.txt", map)

        barriers_array = []
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (map[i,j] < 100000):
                    barriers_array.append((j+1,i+1))
        self.barriers = set()
        self.barriers = set(barriers_array)


        np.savetxt("barriers.txt", barriers_array, delimiter=',')
