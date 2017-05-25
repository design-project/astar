import pylab as pl
import matplotlib.cm as cm
import numpy as np
import PIL
from PIL import Image

stepsize = 100


class im2bin:
    def __init__(self):
        #open image and convert into greyscale
        im = Image.open('demo.jpeg')
        im_grey = im.convert('L') # convert the image to *greyscale*
        im_array = np.array(im_grey)

        num_rows, num_cols = np.shape(im_array)

        self.start = (2, 2)
        self.end = (8, 2)
        self.dir = (0,1)
        self.height = int(num_rows/stepsize)
        self.width = int(num_cols/stepsize)

        map = np.zeros((self.height, self.width))
        sum=0

        for i in range(0,self.height):
            for j in range(0, self.width):
                for k in range(stepsize*i, stepsize*i+stepsize):
                    for z in range(stepsize*j, stepsize*j+stepsize):
                        sum = sum + im_array[k,z]
                        map[i,j] = sum/stepsize
                        sum=0

        barriers_array = []
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (map[i,j] < 10000):
                    barriers_array.append((j+1,i+1))
        self.barriers = {}
        self.barriers = set(barriers_array)

        np.savetxt("barriers.txt", barriers_array, delimiter=',')

    def update(self):
        return
