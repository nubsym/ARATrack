# Different test settings for ARATrack on LaSOT/TrackingNet/GOT10K/UAV123/TNL2k/LaSOT_ext
# First, put your trained ARATrack-online models on SAVE_DIR/models directory. 
# Then,uncomment the code of corresponding test settings.
# Finally, you can find the tracking results on RESULTS_PATH and the tracking plots on RESULTS_PLOT_PATH.

##########-------------- ARATrack -----------------##########
### LaSOT test and evaluation
python tracking/test.py aratrack_online baseline --dataset lasot --threads 32 --num_gpus 8 --params__model ARATrackOnline.pth.tar --params__search_area_scale 4.8
python tracking/analysis_results.py --dataset_name lasot --tracker_param baseline

### LaSOT_ext test and evaluation
python tracking/test.py aratrack_online baseline --dataset LaSOT_extension_subset --threads 32 --num_gpus 8 --params__model ARATrackOnline.pth.tar --params__search_area_scale 4.8
python tracking/analysis_results.py --dataset_name LaSOT_extension_subset --tracker_param baseline

### TrackingNet test and pack
# python tracking/test.py aratrack_online baseline --dataset trackingnet --threads 32 --num_gpus 8 --params__model ARATrackOnline.pth.tar
# python lib/test/utils/transform_trackingnet.py --tracker_name ARATrackOnline.pth.tar --cfg_name baseline

### GOT10k test and pack
# python tracking/test.py aratrack_online baseline --dataset got10k_test --threads 32 --num_gpus 8 --params__model ARATrackOnline.pth.tar
# python lib/test/utils/transform_got10k.py --tracker_name ARATrackOnline.pth.tar --cfg_name baseline

### UAV123
# python tracking/test.py aratrack_online baseline --dataset uav --threads 32 --num_gpus 8 --params__model ARATrackOnline.pth.tar --params__search_area_scale 4.5
# python tracking/analysis_results.py --dataset_name uav --tracker_param baseline

### TNL2k
#python tracking/test.py aratrack_online baseline --dataset tnl2k --threads 32 --num_gpus 8 --params__model ARATrackOnline.pth.tar
#python tracking/analysis_results.py --dataset_name tnl2k --tracker_param baseline

