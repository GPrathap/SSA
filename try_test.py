from scipy import misc
import numpy as np
import matplotlib.pyplot as plt
import cv2
from mpl_toolkits.mplot3d import Axes3D

import imagepers


# im = cv2.imread('/dataset/images/'+ str(0) +'_depth_image.jpg', 0)
# # im = misc.imresize(im, 2.0)
# im = im * (255 / np.max(im))

im = np.loadtxt("/dataset/test.txt").reshape(10,10)
im = (im/im.max())*255
im = im.astype(int)


g0 = imagepers.persistence(im)

print len(g0)

fig = plt.figure()
plt.imshow(im, interpolation="nearest")
plt.colorbar()
xx, yy = np.mgrid[0:im.shape[0], 0:im.shape[1]]

#fig = plt.figure()
#plt.contourf(xx, yy, im, np.arange(0, 255, 20))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title("Peristence diagram")
ax.plot([0, 255], [0, 255], '-', c='grey')
for i, homclass in enumerate(g0):
    p_birth, bl, pers, p_death = homclass
    if pers <= 1.0:
        continue

    x, y = bl, bl - pers
    ax.plot([x], [y], '.', c='b')
    ax.text(x, y + 2, str(i + 1), color='b')
ax.set_xlabel("Birth level")
ax.set_ylabel("Death level")
ax.set_xlim((-5, 260))
ax.set_ylim((-5, 260))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title("Loci of births")
for i, homclass in enumerate(g0):
    p_birth, bl, pers, p_death = homclass
    if pers <= 20.0:
        continue
    y, x = p_birth
    ax.plot([x], [y], '.', c='b')
    ax.text(x, y + 0.25, str(i + 1), color='b')

ax.set_xlim((0, im.shape[1]))
ax.set_ylim((0, im.shape[0]))
plt.gca().invert_yaxis()

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(xx, yy, im ,rstride=1, cstride=1, cmap=plt.cm.jet, linewidth=0)

plt.show()