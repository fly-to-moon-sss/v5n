import os
from PIL import Image, ImageDraw


# 获取图片宽高
def get_image_width_high(full_image_name):
    image = Image.open(full_image_name)
    image_width, image_high = image.size[0], image.size[1]
    return image_width, image_high


# 读取原始标注数据
def read_label_txt(full_label_name, full_image_name):
    fp = open(full_label_name, mode="r")
    lines = fp.readlines()
    fp.close()
    image_width, image_high = get_image_width_high(full_image_name)
    object_list = []
    for line in lines:
        array = line.split()
        x_label_min = (float(array[1]) - float(array[3]) / 2) * image_width
        x_label_max = (float(array[1]) + float(array[3]) / 2) * image_width
        y_label_min = (float(array[2]) - float(array[4]) / 2) * image_high
        y_label_max = (float(array[2]) + float(array[4]) / 2) * image_high
        category = int(array[0])
        obj_info = [x_label_min, y_label_min, x_label_max, y_label_max, category]

        object_list.append(obj_info)
    return object_list


def main():
    image_path = 'images/val/'  # 图片文件路径
    label_path = 'labels/val/'  # 标注文件路径
    output_path = 'out'     # 输出图片路径
    all_image = os.listdir(image_path)
    for i in range(len(all_image)):
        full_image_path = os.path.join(image_path, all_image[i])
        # 分离文件名和文件后缀
        image_name, image_extension = os.path.splitext(all_image[i])
        # 拼接标注路径
        full_label_path = os.path.join(label_path, image_name+'.txt')
        # 打开图片
        img = Image.open(full_image_path)
        # 读取标注数据
        object_list = read_label_txt(full_label_path, full_image_path)
        # 画框
        draw = ImageDraw.Draw(img)
        for obj_info in object_list:
            x1, y1, x2, y2 = obj_info[:4]
            draw.line([(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)], fill=(255, 0, 0), width=5)
        # 将画框后的图片保存至输出路径
        img.save(os.path.join(output_path, all_image[i]))


if __name__ == '__main__':
    main()