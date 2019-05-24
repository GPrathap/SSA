
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
#
from ssa import SingularSpectrumAnalysis

image_types = ["_depth_image.jpg", "_filtered_image.jpg", "_prossed_image.jpg", "_angle_image.jpg", "_smoothed_image.jpg", "_no_ground_image.jpg"]
# for i in range(15201, 15208):
#     for j, type_of_image in enumerate(image_types):
#         print (str(j) + type_of_image)
#         plt.subplot(6,1,j+1)
#         img=mpimg.imread('/dataset/images/result/8/'+str(i)+type_of_image)
#         plt.imshow(img)
#         plt.savefig("/home/geesara/images/try0/" +str(i)+'_iteration.jpg')



img=mpimg.imread('/dataset/images/result/8/15207_angle_image.jpg')
# plt.imshow(img)
# plt.show()

# for feature in img:
reconstructed_signal = SingularSpectrumAnalysis(img[15], 16, True).execute(8)
plt.show()



#
# ***
# 10716062_transformed.jpg
# 14391933_transformed.jpg
# 15414948_transformed.jpg
# 8683499_transformed.jpg
# 8770648_transformed.jpg
# ***
# img=mpimg.imread('/dataset/images/result/06/12719210_transformed.jpg')
# plt.imshow(img)
plt.show()