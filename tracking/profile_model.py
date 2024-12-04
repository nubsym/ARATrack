import argparse
import torch
import os
import time
import importlib

from fvcore.nn import FlopCountAnalysis
from torchstat import stat

import _init_paths
from torch import nn
from lib.models.aratrack.aratrack_online import Attention, build_aratrack_online_score
from thop import profile
from thop.utils import clever_format
# from torchstat import stat

def parse_args():
    """
    args for training.
    """
    parser = argparse.ArgumentParser(description='Parse args for training')
    # for train
    parser.add_argument('--script', type=str, default='aratrack_online', help='training script name')
    parser.add_argument('--config', type=str, default='baseline', help='yaml configure file name')
    parser.add_argument('--display_name', type=str, default='ARATrack')
    parser.add_argument('--online_skip', type=int, default=200, help='the skip interval of aratrack-online')
    args = parser.parse_args()

    return args

def evaluate(model, template, search, skip=200, display_info='ARATrack'):
    """Compute FLOPs, Params, and Speed"""
    # compute flops and params except for score prediction
    macs, params = profile(model, inputs=(template, template, search, False), verbose=False)
    macs, params = clever_format([macs, params], "%.3f")
    print('==>Macs is ', macs)
    print('==>Params is ', params)

    # test speed
    T_w = 10
    T_t = 1000
    print("testing speed ...")
    with torch.no_grad():
        # overall
        for i in range(T_w):
            _ = model(template, template, search, run_score_head=True)
        start = time.time()
        for i in range(T_t):
            if i % skip == 0:
                _ = model.set_online(template, template)
            _ = model.forward_test(search)
        end = time.time()
        avg_lat = (end - start) / T_t
        print("\033[0;32;40m The average overall FPS of {} is {}.\033[0m" .format(display_info, 1.0/avg_lat))


def get_data(bs, sz):
    img_patch = torch.randn(bs, 3, sz, sz)
    return img_patch


if __name__ == "__main__":
    device = "cuda:0"
    torch.cuda.set_device(device)
    args = parse_args()
    '''update cfg'''
    prj_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    yaml_fname = os.path.join(prj_dir, 'experiments/%s/%s.yaml' % (args.script, args.config))
    print("yaml_fname: {}".format(yaml_fname))
    config_module = importlib.import_module('lib.config.%s.config' % args.script)
    cfg = config_module.cfg
    config_module.update_config_from_file(yaml_fname)
    print("cfg: {}".format(cfg))
    '''set some values'''
    bs = 1
    z_sz = cfg.TEST.TEMPLATE_SIZE
    x_sz = cfg.TEST.SEARCH_SIZE
    cfg.MODEL.BACKBONE.FREEZE_BN = False
    cfg.MODEL.HEAD_FREEZE_BN = False
    '''import stark network module'''
    if args.script == "aratrack_online":
        model_constructor = build_aratrack_online_score
        model = model_constructor(cfg)
        # get the template and search
        template = get_data(bs, z_sz)
        search = get_data(bs, x_sz)
        # transfer to device
        model = model.to(device)
        template = template.to(device)
        search = search.to(device)
        # evaluate the model properties
        evaluate(model, template, search, args.online_skip, args.display_name)

