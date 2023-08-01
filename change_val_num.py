import os
import random
import shutil


# VOCdevkit -> VOC2012 -> ImageSets -> Segmentation -> val.txt
# 假设VOC2012验证集txt文件路径为 "./VOCdevkit/VOC2012/ImageSets/Segmentation/val.txt"

def split_validation_set(val_txt_path, new_val_txt_path, num_samples):
    with open(val_txt_path, 'r') as f:
        val_samples = f.readlines()

    random.shuffle(val_samples)
    selected_samples = val_samples[:num_samples]

    with open(new_val_txt_path, 'w') as f:
        f.writelines(selected_samples)


def copy_images_and_annotations(src_folder, dest_folder, val_txt_path):
    with open(val_txt_path, 'r') as f:
        selected_samples = f.readlines()

    selected_samples = [sample.strip() for sample in selected_samples]

    for sample in selected_samples:
        image_name = sample + '.jpg'
        annotation_name = sample + '.png'

        src_image_path = os.path.join(src_folder, 'JPEGImages', image_name)
        src_annotation_path = os.path.join(src_folder, 'SegmentationClass', annotation_name)

        dest_image_path = os.path.join(dest_folder, 'JPEGImages', image_name)
        dest_annotation_path = os.path.join(dest_folder, 'SegmentationClass', annotation_name)

        shutil.copy(src_image_path, dest_image_path)
        shutil.copy(src_annotation_path, dest_annotation_path)


if __name__ == '__main__':
    # 原始VOC2012验证集文件路径
    original_val_txt_path = "data/VOCdevkit/VOC2012/ImageSets/Segmentation/val.txt"

    # 新的截取的验证集文件路径
    new_val_txt_path = "data/VOCdevkit/VOC2012/ImageSets/Segmentation/val_subset.txt"

    # 截取的样本数量
    num_samples_to_select = 300  # 假设截取100个样本

    # 调用函数截取验证集样本
    split_validation_set(original_val_txt_path, new_val_txt_path, num_samples_to_select)

    # VOC2012数据集文件夹路径
    voc2012_folder = "data/VOCdevkit/VOC2012"
    new_val_folder = "data/VOCdevkit/VOC2012_subset"

    # 复制截取的验证集样本到新文件夹
    if not os.path.exists(new_val_folder):
        os.makedirs(os.path.join(new_val_folder, 'JPEGImages'))
        os.makedirs(os.path.join(new_val_folder, 'SegmentationClass'))

    copy_images_and_annotations(voc2012_folder, new_val_folder, new_val_txt_path)
