import os

import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt


def pltshow(pred_map, name):
    plt.figure(2)
    pred_frame = plt.gca()
    plt.imshow(pred_map, 'jet')
    # plt.colorbar()
    pred_frame.axes.get_yaxis().set_visible(False)
    pred_frame.axes.get_xaxis().set_visible(False)
    pred_frame.spines['top'].set_visible(False)
    pred_frame.spines['bottom'].set_visible(False)
    pred_frame.spines['left'].set_visible(False)
    pred_frame.spines['right'].set_visible(False)
    pred_name = 'path' + name + '.jpg'
    # if not os.path.exists(pred_name):
    #     os.makedirs(pred_name)
    plt.savefig(pred_name, bbox_inches='tight', pad_inches=0, dpi=150)
    plt.close(2)
