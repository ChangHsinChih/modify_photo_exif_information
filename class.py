import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from PIL import Image, ExifTags


# 增加最大像素限
Image.MAX_IMAGE_PIXELS = None  # 禁用检查


def get_exif_data(image_path):
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        if exif_data:
            return exif_data
    except Exception as e:
        print(f"Error reading EXIF data for {image_path}: {e}")
        return None
    return None



def move_image(file_path, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    shutil.move(file_path, os.path.join(dest_folder, os.path.basename(file_path)))


def classify_images(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            exif_data = get_exif_data(file_path)
            if not exif_data:
                move_image(file_path, os.path.join(folder_path, '无exif信息'))
            else:
                    # 获取 TAG 名称与 ID 的映射
                datetime_tag_id = [key for key, value in ExifTags.TAGS.items() if value == "DateTimeOriginal"]
                gpsinfo_tag_id = [key for key, value in ExifTags.TAGS.items() if value == "GPSInfo"]
                # print(datetime_tag_id[0])
                # print(gpsinfo_tag_id[0])

                if datetime_tag_id[0] not in exif_data and gpsinfo_tag_id[0] not in exif_data:
                    move_image(file_path, os.path.join(folder_path, '无date和GPSinfo'))
                elif datetime_tag_id[0] in exif_data and gpsinfo_tag_id[0] not in exif_data:
                    move_image(file_path, os.path.join(folder_path, '无GPSinfo'))
                elif datetime_tag_id[0] not in exif_data and gpsinfo_tag_id[0] in exif_data:
                    move_image(file_path, os.path.join(folder_path, '无date'))
                # If it has both, leave it in the original folder
# 调用函数
folder_path = './源文件'  # 这里替换为目标文件夹路径
classify_images(folder_path)
