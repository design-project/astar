import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import PIL
from PIL import Image




class im2bin:
    def __init__(self):
        self.update()
        return
    '''
    def update(self):
        #open image and convert into greyscale
        im = Image.open('demo.jpeg')
        im_grey = im.convert('L') # convert the image to *greyscale*
        im_array = np.array(im_grey)

        num_rows, num_cols = np.shape(im_array)
        stepsize = 40
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
                if (map[i,j] < 2):
                    barriers_array.append((j+1,i+1))



        showmap = np.zeros((24,19))

        for i in range(0,self.height):
            for j in range(0,self.width):
                if (map[i,j] <2 ):
                    if i>=1 & j>=1:
                        barriers_array.append((j,i))
                        showmap[i,j] =1
                    if i>=1:
                        barriers_array.append((j+2,i))
                        barriers_array.append((j+1,i))
                        showmap[i,j+2]=1
                        showmap[i,j+1]=1
                    if j>=1:
                        barriers_array.append((j,i+1))
                        barriers_array.append((j,i+2))
                        showmap[i+1,j]=1
                        showmap[i+2,j]=1
                    barriers_array.append((j+1,i+1))
                    barriers_array.append((j+1,i+2))
                    barriers_array.append((j+2,i+1))
                    barriers_array.append((j+2,i+2))
                    showmap[i+1,j+1]=1
                    showmap[i+2,j+1]=1
                    showmap[i+1,j+2]=1
                    showmap[i+2,j+2]=1
        showmap = showmap.astype('uint8')*255
        im = Image.fromarray(showmap)
        im.save("results.jpg")



        self.barriers = set()
        self.barriers = set(barriers_array)


        np.savetxt("barriers.txt", barriers_array, delimiter=',')

        showmap = np.zeros((22, 17))
        for i in range(0, 22):
            for j in range(0, 17):
                print i,j
                if(map[i,j]<2):
                    showmap[i,j] = 0
                else:
                    showmap[i,j] = 1
        showmap = showmap.astype('uint8')*255
        im = Image.fromarray(showmap)
        im.save("results.jpg")
    '''
    def update(self):
        #open image and convert into greyscale
        im = Image.open('demo2.jpeg')
        im_grey = im.convert('L') # convert the image to *greyscale*
        im_array = np.array(im_grey)

        num_rows, num_cols = np.shape(im_array)
        stepsize = 45
        self.start = (2,10)
        self.end = (7, 9)
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

        np.savetxt("map2.txt", map)
        barriers_array = []
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (map[i,j] < 5):
                    barriers_array.append((j+1,i+1))
        self.barriers = set(barriers_array)
        np.savetxt("barriers2.txt", barriers_array, delimiter=',')

        showmap = np.zeros((21, 17))
        for i in range(0, 21):
            for j in range(0, 17):
                print i,j
                if(map[i,j]<5):
                    showmap[i,j] = 0
                else:
                    showmap[i,j] = 1
        showmap = showmap.astype('uint8')*255
        im = Image.fromarray(showmap)
        im.save("results2.jpg")
