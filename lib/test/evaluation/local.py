from lib.test.evaluation.environment import EnvSettings

def local_env_settings():
    settings = EnvSettings()

    # Set your local paths here.

    settings.davis_dir = ''
    settings.got10k_lmdb_path = '/home/sym/SYM/tracking/code/ARATrack/data/got10k_lmdb'
    settings.got10k_path = '/home/sym/SYM/tracking/data/GOT-10k'
    settings.got_packed_results_path = ''
    settings.got_reports_path = ''
    settings.lasot_lmdb_path = '/home/sym/SYM/tracking/code/ARATrack/data/lasot_lmdb'
    settings.lasot_path = '/home/sym/SYM/tracking/data/LASOT_zip'
    settings.network_path = '/home/sym/SYM/tracking/code/ARATrack/test/networks'    # Where tracking networks are stored.
    settings.nfs_path = '/home/sym/SYM/tracking/code/ARATrack/data/nfs'
    settings.otb_path = '/home/sym/SYM/tracking/code/ARATrack/data/OTB2015'
    settings.prj_dir = '/home/sym/SYM/tracking/code/ARATrack'
    settings.result_plot_path = '/home/sym/SYM/tracking/code/ARATrack/test/result_plots'
    settings.results_path = '/home/sym/SYM/tracking/code/ARATrack/test/tracking_results'    # Where to store tracking results
    settings.save_dir = '/home/sym/SYM/tracking/code/ARATrack'
    settings.segmentation_path = '/home/sym/SYM/tracking/code/ARATrack/test/segmentation_results'
    settings.tc128_path = '/home/sym/SYM/tracking/code/ARATrack/data/TC128'
    settings.tn_packed_results_path = ''
    settings.tpl_path = ''
    settings.trackingnet_path = '/home/sym/SYM/tracking/data/trackingNetTest'
    settings.uav_path = '/home/sym/SYM/tracking/data/UAV123/UAV123'
    settings.vot_path = '/home/sym/SYM/tracking/code/ARATrack/data/VOT2019'
    settings.youtubevos_dir = ''
    settings.tnl2k_path = '/home/sym/SYM/tracking/data/TNL2K_test/TNL2k'
    settings.lasot_extension_subset_path = '/home/sym/SYM/tracking/data/LaSOT_Ext'

    return settings

