import os
import numpy as np
import cv2
import argparse

parser = argparse.ArgumentParser('create image pairs')
parser.add_argument('--fold_A', dest='fold_A', help='input directory for image A', type=str, default='/media/linger/udata/data_time/data/pm2/VIS')
parser.add_argument('--fold_B', dest='fold_B', help='input directory for image B', type=str, default='/media/huahua/DATA/MTN_dataset_shin/DIV2K/thermal/B')
parser.add_argument('--fold_C', dest='fold_C', help='input directory for image C', type=str, default='/media/huahua/DATA/data/mask')
parser.add_argument('--fold_AB', dest='fold_AB', help='output directory', type=str, default='/media/huahua/DATA/data/pm7/ir_mk')
parser.add_argument('--num_imgs', dest='num_imgs', help='number of images', type=int, default=1000000)
parser.add_argument('--use_AB', dest='use_AB', help='if true: (0001_A, 0001_B) to (0001_AB)', action='store_true')
args = parser.parse_args()

for arg in vars(args):
    print('[%s] = ' % arg, getattr(args, arg))

splits = os.listdir(args.fold_A)

for sp in splits:
    img_fold_A = os.path.join(args.fold_A, sp)
    img_fold_B = os.path.join(args.fold_B, sp)
    img_fold_C = os.path.join(args.fold_C, sp)
    img_list = os.listdir(img_fold_A)
    if args.use_AB:
        img_list = [img_path for img_path in img_list if '_A.' in img_path]

    num_imgs = min(args.num_imgs, len(img_list))
    print('split = %s, use %d/%d images' % (sp, num_imgs, len(img_list)))
    img_fold_AB = os.path.join(args.fold_AB, sp)
    if not os.path.isdir(img_fold_AB):
        os.makedirs(img_fold_AB)
    print('split = %s, number of images = %d' % (sp, num_imgs))
    for n in range(num_imgs):
        name_A = img_list[n]
        path_A = os.path.join(img_fold_A, name_A)
        if args.use_AB:
            name_B = name_A.replace('_A.', '_B.')
        else:
            name_B = name_A
        name_C = name_A
        # path_B = os.path.join(img_fold_B, name_B)
        path_C = os.path.join(img_fold_C, name_C)
        if os.path.isfile(path_A):
            name_AB = name_A
            if args.use_AB:
                name_AB = name_AB.replace('_A.', '.')  # remove _A
            path_AB = os.path.join(img_fold_AB, name_AB)
            im_A = cv2.imread(path_A, 1) # python2: cv2.CV_LOAD_IMAGE_COLOR; python3: cv2.IMREAD_COLOR
            im_C = cv2.imread(path_C, 1)
            im_AB = np.concatenate([im_A, im_C], 1)
            cv2.imwrite(path_AB, im_AB)
