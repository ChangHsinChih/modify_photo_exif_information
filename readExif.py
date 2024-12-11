from PIL import Image
from PIL.ExifTags import TAGS
from PIL import Image, ExifTags
import piexif
# 打开图像文件

image_path = "./待处理/IMG_20220627_171432.jpg"
image = Image.open(image_path)

# 获取 EXIF 信息
exif_data = image._getexif()
# 解析 EXIF 信息
if exif_data:
    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        print(f"{tag}: {value}")
else:
    print("没有 EXIF 信息\n")

if exif_data:
    # 获取 TAG 名称与 ID 的映射
    datetime_tag_id = [key for key, value in ExifTags.TAGS.items() if value == "DateTimeOriginal"]
    gpsinfo_tag_id = [key for key, value in ExifTags.TAGS.items() if value == "GPSInfo"]
    print("\n")
    print(datetime_tag_id[0],"\n")
    print(gpsinfo_tag_id[0],"\n")
    # print(exif_data)
    if datetime_tag_id and datetime_tag_id[0] in exif_data:
        print("存在 DateTime 标签")
        print(f"DateTime 值: {exif_data[datetime_tag_id[0]]}","\n")
    else:
        print("不存在 DateTime 标签\n")

    if gpsinfo_tag_id and gpsinfo_tag_id[0] in exif_data:
        print("存在 GPSInfo 标签")
        print(f"GPSInfo 值: {exif_data[gpsinfo_tag_id[0]]}","\n")
    else:
        print("不存在 GPSInfo 标签")
else:
    print("没有 EXIF 信息")




