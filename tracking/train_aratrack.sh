# There are the detailed training settings for ARATrack
# 1. download pretrained ConvMAE models (convmae_base.pth.pth/convmae_large.pth) at https://github.com/Alpha-VL/ConvMAE
# 2. set the proper pretrained convmae models path 'MODEL:BACKBONE:PRETRAINED_PATH' at experiment/aratrack/CONFIG_NAME.yaml.
# 3. uncomment the following code to train corresponding trackers.

### Training ARATrack
# Stage1: train ARATrack without state-aware-head
python tracking/train.py --script aratrack --config baseline --save_dir /YOUR/PATH/TO/SAVE/ARAtrack --mode multiple --nproc_per_node 8
## Stage2: train aratrack_online, i.e., state-aware-head
# python tracking/train.py --script arartrack_online --config baseline --save_dir /YOUR/PATH/TO/SAVE/ARAtrack --mode multiple --nproc_per_node 8 --stage1_model /STAGE1/MODEL

