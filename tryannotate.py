from pathlib import Path as PathOF
import json
from pprint import pprint
import pylab as plt
import numpy as np
from matplotlib.path import Path

from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
import glob
import re
from sklearn.metrics import precision_recall_fscore_support

# ImageDraw.Draw(draw_img).polygon([(60, 50), (20, 60), (60, 30), (60, 20)],
#                             fill=1, outline=None)
#
# img = np.ma.masked_equal(np.array(draw_img), 0.)
# img = np.array(img, dtype=np.uint8)
# plt.imshow(img , interpolation="None")
# plt.show()

width, height = 536, 974
# dataset_location = "/home/geesara/project/icra/test/non_ground/non_ground/ds/ann/"
# dataset_location_ = "/home/geesara/project/icra/test/non_ground/ground_separation/ds/test_f1/ds/ann/"
# dataset_location = "/home/geesara/Documents/results/lidar/ds/ann/1/"
dataset_location = "/home/geesara/Documents/results/lidar/ds/ann/2/"
#
ground_truth = glob.glob1(dataset_location,'*_lidar_projected.jpg.json')
ground_truth = sorted(ground_truth, key=lambda x: float(re.findall("(\d+)", x)[0]))

non_ground_label = glob.glob1(dataset_location,'*_non_ground_projected.jpg.json')
# non_ground_label = glob.glob1(dataset_location,'*_ground_projected.jpg.json')
non_ground_label = sorted(non_ground_label, key=lambda x: float(re.findall("(\d+)", x)[0]))

final_result = []
for ground_truth_file, non_ground_label_file in zip(ground_truth, non_ground_label):
    # print(ground_truth_file)
    polygons = []

    with open(dataset_location + '/' + ground_truth_file) as ground_:
            with open(dataset_location + '/' + non_ground_label_file) as labeled:
                ground_data = json.load(ground_)
                labeled_data = json.load(labeled)
                draw_img_ground = Image.new('F', (1000, 350), 0)
                labeled_img = Image.new('F', (1000, 350), 0)
                for index in ground_data['objects']:
                    polygon = index['points']['exterior']
                    polygon_plygon = [(elem[0], elem[1]) for elem in polygon]
                    ImageDraw.Draw(draw_img_ground).polygon(polygon_plygon, fill=1, outline=None)

                for index in labeled_data['objects']:
                    polygon = index['points']['exterior']
                    polygon_plygon = [(elem[0], elem[1]) for elem in polygon]
                    ImageDraw.Draw(labeled_img).polygon(polygon_plygon, fill=1, outline=None)

                ground_img = np.ma.masked_equal(np.array(draw_img_ground), 0.)
                labeled_img = np.ma.masked_equal(np.array(labeled_img), 0.)

                ground_img = np.array(ground_img, dtype=np.uint8)
                labeled_img = np.array(labeled_img, dtype=np.uint8)
                # ff = f1_score(ground_img, labeled_img, average='weighted')
                scores = precision_recall_fscore_support(ground_img, labeled_img, average='weighted')
                final_result.append(scores[0:3])
                fig, ax = plt.subplots()
                frame1 = plt.gca()
                frame1.axes.xaxis.set_ticklabels([])
                frame1.axes.yaxis.set_ticklabels([])
                plt.imshow(ground_img, interpolation="None")
                plt.show()

final_result = np.array(final_result)
final_result_mean = final_result.mean(axis=0)
print(final_result_mean)
        # print(ff)
        # plt.imshow(img , interpolation="None")
        # plt.show()

    # print("============================")
    # # poly_path = Path(polygons)
    # #
    # # x, y = np.mgrid[:height, :width]
    # # coors = np.hstack((x.reshape(-1, 1), y.reshape(-1, 1)))  # coors.shape is (4000000,2)
    # #
    # # mask = poly_path.contains_points(coors)
    # # plt.imshow(mask.reshape(height, width))
    # # print("============================")
    # #
    # #
    # colors = 100 * np.random.rand(len(polygons))
    # p = PatchCollection(polygons, cmap=matplotlib.cm.jet, alpha=0.4)
    # p.set_array(np.array(colors))
    # ax.add_collection(p)
    # plt.colorbar(p)

    # plt.show()