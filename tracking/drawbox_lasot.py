# encoding: utf-8
import os
import numpy as np
import cv2

# 选择第几个视频
# TODO:选择某个视频   # failure_case 68 -1 (volleyball-19)  dog-1 19 0   tiger-6: 63 3  monkey-4 44 2
video_num = 12  # 19(dog-19)  # 29(goldfish-7,8)  # 48(pig-2,13# )  # 12(cattle-13)  # 28(giraffe-2)  # 61(swing-10)  # 50 (rabbit-10)  # 52(rabot-1)  # 56 (sheep-3,7,9)  # 70 (zebra-10)  # 11 (cat-3)  #5 (bird-2)
# 37 (kangaroo)  0,3
sequence_id = 1  # 2 # 2, 3  # 0,3  # 1,2,3  # 3  # 0  # 0  # 0,2,3  # 0,  # 1  # 2


# TODO:数据集所在路径
src_pic_path = '/home/sym/SYM/tracking/data/LASOT_zip'

all_pic = os.listdir(src_pic_path)  # 注意os.listdir获取到的路径是乱序的，要用.sort函数排序
all_pic.sort()

each_video_path = [os.path.join(src_pic_path, video_path) for video_path in all_pic]
# print(each_video_path)
# choose one video
# one_video = each_video_path[video_num] # for got
video_names = os.listdir(each_video_path[video_num])  # for lasot
video_names.sort()
one_video = os.path.join(each_video_path[video_num], video_names[sequence_id])  # for lasot
result = one_video.split('/')
video_name = result[len(result) - 1]
print('choosed video_name: ({})--'.format(video_num), video_name)

# TODO：算法评测结果所在路径
eval_result_path = '/home/sym/SYM/tracking/code/pysot-toolkit-master/tracker'
all_eval_trackers = os.listdir(eval_result_path)  # AiATrack, MixFormer, OSTrack, Ours, ROMTrack, STRAK
all_eval_trackers.sort()
each_eval_tracker = [os.path.join(eval_result_path, eval_tracker) for eval_tracker in all_eval_trackers]  # evaluation results of all trackers
each_eval_tracker.sort()
# print(each_eval_tracker)

# choose one tracker
one_tracker = each_eval_tracker[0]  # 2
each_eval_result = os.listdir(one_tracker)
each_eval_result.sort()  # ['Basketball.txt', 'Biker.txt', 'Bird1.txt', ... ,'Walking2.txt', 'Woman.txt']
each_eval_result = os.listdir(os.path.join(one_tracker,each_eval_result[video_num-1]))  # for lasot
each_eval_result.sort()
# print(each_eval_result)

# each_eval_result_path = [os.path.join(one_tracker, eval_result) for eval_result in each_eval_result]
# print(each_eval_result_path)
#
# ---------------------------------------------
all_trakcers_result = []
for tracker in each_eval_tracker:
    each_eval_result_path = [os.path.join(tracker,os.path.join(eval_result.split('-')[0], eval_result)) for eval_result in each_eval_result]
    all_trakcers_result.append(each_eval_result_path)
# print('all_trackers_result', all_trakcers_result)  # [['./Results_OTB100/CCOT/Basketball.txt', ... ,], ...]
# ---------------------------------------------

all_list = []  # a video of one tracker
for num in range(0, len(all_trakcers_result)):
    # with open(all_trakcers_result[num][video_num-1]) as eval_result:  # choose a video of one tracker
    with open(all_trakcers_result[num][sequence_id]) as eval_result:
        dataset = []
        lines = eval_result.readlines()

        # read datas in txt file, transform to String formation
        try:
            for line in lines:
                temp1 = line.strip('\n')
                temp2 = temp1.split('\t')
                dataset.append(temp2)

                # new_dataset = [new_line[0].split(',') for new_line in dataset]  # .split(',')按逗号分割字符串 for got
                new_dataset = dataset  # for lasot
            # print('new_dataset', new_dataset)
            # str转化成int型
            for i in range(0, len(new_dataset)):
                for j in range(len(new_dataset[i])):
                    new_dataset[i][j] = int(float(new_dataset[i][j]))
            all_list.append(new_dataset)
        except:
            for line in lines:
                temp1 = line.strip('\n')
                temp2 = temp1.split(',')
                dataset.append(temp2)

                new_dataset = [new_line[0].split(',') for new_line in dataset]  # .split(',')按逗号分割字符串 for got
                # new_dataset = dataset  # for lasot
            # print('new_dataset', new_dataset)
            # str转化成int型
            for i in range(0, len(new_dataset)):
                for j in range(len(new_dataset[i])):
                    new_dataset[i][j] = int(float(new_dataset[i][j]))
            all_list.append(new_dataset)

# print(all_list)
gt = os.path.join(one_video, 'groundtruth.txt')
with open(gt) as gt_result:
    dataset = []
    gt_lines = gt_result.readlines()
    # read datas in txt file, transform to String formation
    for gt_line in gt_lines:
        gt_temp1 = gt_line.strip('\n')
        gt_temp2 = gt_temp1.split('\t')
        dataset.append(gt_temp2)

        new_dataset = [new_line[0].split(',') for new_line in dataset]  # .split(',')按逗号分割字符串 for got
    # str转化成int型
    for i in range(0, len(new_dataset)):
        for j in range(len(new_dataset[i])):
            new_dataset[i][j] = int(float(new_dataset[i][j]))
    all_list.append(new_dataset)

#
# every frame in a video
frames_list = os.listdir(os.path.join(one_video, 'img'))  # for lasot
# frames_list = os.listdir(one_video)  # for got
frames_list.sort()
frames_path = [os.path.join(os.path.join(one_video, 'img'), frame_path) for frame_path in frames_list]
# frames_path = [os.path.join(one_video, frame_path) for frame_path in frames_list]  # for got

# print(frames_path)

# TODO：画图结果保存路径
dst_pic_path = '/home/sym/SYM/tracking/paper/AOFTrack/failure_case/'  # /failure_case/
dst_pic_path = dst_pic_path + video_name

# 判断是否有文件夹，如果没有则新建   如果有的话，说明已经生成过了。需要删除原文件后再次执行程序
f = os.path.exists(dst_pic_path)
if f is False:
    os.makedirs(dst_pic_path)

    # show the tracking results
    for index, path in enumerate(frames_path): #
        img = cv2.imread(path)
        if 'groundtruth' in path:
            break
        # print(img.shape)
        # --------------------------------------
        # results of trackers
        # all_list[a][b] 解释：a为某个算法，b为某个算法的某帧结果
        # a 对应的算法 : CCOT CFNet DaSiamRPN DeepSRDCF ECO fDSST GradNet MDNet Ours OursOld SiamDWfc SiamDWrpn SiamFC SiamRPN SRDCF Staple
        # TODO:选择想要画的算法结果，注意：需要改all_list[a][index]中的a这一项
        # track_gt = all_list[15][index]  # Staple
        # # draw bounding boxes
        # cv2.rectangle(img, (track_gt[0], track_gt[1]), (track_gt[0] + track_gt[2], track_gt[1] + track_gt[3]), (255, 255, 255), thickness=2)  # 白色

        # track_gt_1 = all_list[4][index]  # ROMTrack
        # cv2.rectangle(img, (track_gt_1[0], track_gt_1[1]), (track_gt_1[0] + track_gt_1[2], track_gt_1[1] + track_gt_1[3]), (255, 0, 0), thickness=8)  # 蓝色

        track_gt_2 = all_list[-1][index]  # gt
        cv2.rectangle(img, (track_gt_2[0], track_gt_2[1]), (track_gt_2[0] + track_gt_2[2], track_gt_2[1] + track_gt_2[3]), (0, 255, 0), thickness=8)  # 绿色

        track_gt_3 = all_list[3][index]  # Ours
        cv2.rectangle(img, (track_gt_3[0], track_gt_3[1]), (track_gt_3[0] + track_gt_3[2], track_gt_3[1] + track_gt_3[3]), (0, 0, 255), thickness=8) # 红色

        # track_gt_4 = all_list[1][index]  # MixFormer
        # cv2.rectangle(img, (track_gt_4[0], track_gt_4[1]), (track_gt_4[0] + track_gt_4[2], track_gt_4[1] + track_gt_4[3]), (255, 0, 255), thickness=8)  # 紫色
        #
        # track_gt_5 = all_list[3][index]  # TrDimp
        # cv2.rectangle(img, (track_gt_5[0], track_gt_5[1]), (track_gt_5[0] + track_gt_5[2], track_gt_5[1] + track_gt_5[3]), (0, 0, 0), thickness=8)  # 黑色
        #
        # track_gt_6 = all_list[2][index]  # OSTrack
        # cv2.rectangle(img, (track_gt_6[0], track_gt_6[1]), (track_gt_6[0] + track_gt_6[2], track_gt_6[1] + track_gt_6[3]), (0, 255, 255), thickness=8)  # 黄色

        # track_gt_7 = all_list[12][index]  # SiamFC
        # cv2.rectangle(img, (track_gt_7[0], track_gt_7[1]), (track_gt_7[0] + track_gt_7[2], track_gt_7[1] + track_gt_7[3]), (0, 0, 0), thickness=2)  #
        # --------------------------------------

        # cv2.putText(img, '#{}'.format(index), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)  # (20,80)
        cv2.putText(img, '#{}'.format(index), (20, 80), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 3)
        # cv2.putText(img, '#{}'.format(index), (20, 120), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 0, 255), 6)
        # cv2.putText(img, video_name, (10, int(img.shape[0] * 0.9)), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 255, 255), 2)

        cv2.imwrite(dst_pic_path + '/' + '{}.jpg'.format(index), img)
        # cv2.imshow('src_img', img)
        # cv2.waitKey(0)
else:
    print('已经生成过({})，请删除原文件后重新执行程序'.format(video_name))




