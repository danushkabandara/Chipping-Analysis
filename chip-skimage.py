from skimage import data
from skimage.viewer import ImageViewer
from skimage.io import imread
from skimage import feature
from skimage.transform import (hough_line, hough_line_peaks, probabilistic_hough_line)
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from scipy.signal import find_peaks
image = imread(r'D:\\Chipping_analysis\\chip1.jpg', as_gray=True)
from skimage import filters

sobel_edges = filters.sobel(image)
canny_edges =  feature.canny(image, sigma=5)



# straight-line Hough transform on the canny edges
h, theta, d = hough_line(canny_edges)

# Generating figure 1
fig, axes = plt.subplots(1, 3, figsize=(15, 6))
ax = axes.ravel()

ax[0].imshow(image, cmap=cm.gray)
ax[0].set_title('Input image')
ax[0].set_axis_off()

ax[1].imshow(image, cmap=cm.gray)
m = 0
c= 0
for _, angle, dist in zip(*hough_line_peaks(h, theta, d)):
    y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
    y1 = (dist - image.shape[1] * np.cos(angle)) / np.sin(angle)
    m=(y0-y1)/image.shape[1] #based on the cartesian line eqn y=mx+c
    c= y1-m*image.shape[1] # based on the cartesian line eqn y=mx+c
    ax[1].plot((0, image.shape[1]), (y0, y1), '-r')
ax[1].set_xlim((0, image.shape[1]))
ax[1].set_ylim((image.shape[0], 0))
ax[1].set_axis_off()
ax[1].set_title('straight line edge')
ax[2].imshow(canny_edges)
ax[2].set_title('actual edge')
plt.tight_layout()
#plt.show()

#calculate the distance between hough edge and canny edge-> crack_function
canny_edge_function = np.argmax(canny_edges, axis=0)
crack_function = []
for i in range(0,len(canny_edge_function)):
    if canny_edge_function[i] > 70:
        crack_function.append( canny_edge_function[i] - (m*i + c) )
    else:
        crack_function.append(0)
crack_function = np.array(crack_function)#convert to numpy array
#peakfinding


peaks, properties = find_peaks(crack_function, prominence=3, width=10)
ax[0].plot(crack_function)
ax[0].plot(peaks, crack_function[peaks], "x")
ax[0].vlines(x=peaks, ymin=crack_function[peaks] - properties["prominences"],ymax = crack_function[peaks], color = "C1")
ax[0].hlines(y=properties["width_heights"], xmin=properties["left_ips"],xmax=properties["right_ips"], color = "C1")
plt.show()
#viewer = ImageViewer(canny_edges)

#viewer.show()