# We only support manually setting the bounding box of first frame and save the results in debug directory.


python tracking/video_demo.py aratrack_online baseline video_path --params__model ARATrackOnline.pth.tar --debug 1
