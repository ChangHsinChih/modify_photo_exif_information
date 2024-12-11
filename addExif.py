import os
from PIL import Image
from PIL.ExifTags import TAGS
from PIL import Image, ExifTags
import piexif

#修改时间信息函数
def modify_exif_date(image_path, output_path,time):
    """
    Add EXIF metadata to an image.
    
    :param image_path: Path to the input image
    :param output_path: Path to save the modified image
    :param exif_data: Dictionary of EXIF tags and their values
    """
    # Open the original image
    image = Image.open(image_path)
    # Create exif bytes from the provided dictionary
    exif_dict = {
        "0th": {
            piexif.ImageIFD.DateTime: time,
        },
        "Exif": {
            piexif.ExifIFD.DateTimeOriginal: time,
            piexif.ExifIFD.DateTimeDigitized: time,
            piexif.ExifIFD.OffsetTime: b"+08:00",
            piexif.ExifIFD.OffsetTimeOriginal: b"+08:00",
                },
        "GPS": {
            piexif.GPSIFD.GPSLatitudeRef: b"N",
            piexif.GPSIFD.GPSLatitude: ((40, 1), (0, 1), (0, 1)),  # 40° 0' 0''
            piexif.GPSIFD.GPSLongitudeRef: b"E",
            piexif.GPSIFD.GPSLongitude: ((116, 1), (0, 1), (0, 1)),  # 116° 0' 0''
        },
        "1st": {},
        "thumbnail": None
    }
    
    # Convert the dictionary to bytes
    exif_bytes = piexif.dump(exif_dict)
    
    # Insert EXIF data into the image
    image.save(output_path, 'JPEG', quality=100,exif=exif_bytes)
    print(f"DateTime信息已更新：{time}")
    print(f"添加DateTime的图片已保存到： {output_path}")

#修改GPS信息函数
def modify_exif_gps(image_path, output_path, gps_string):
    """
    修改图片的GPS信息，支持"经度,纬度"格式的输入
    
    :param image_path: 原始图片路径
    :param gps_string: GPS坐标字符串，格式如"118.796306,31.943365"
    :param output_path: 输出图片路径，如果为None则覆盖原文件
    """
    # 解析GPS坐标
    try:
        longitude, latitude = map(float, gps_string.split(','))
    except ValueError:
        raise ValueError("GPS坐标格式错误，请使用'经度,纬度'格式")
    
    # 转换经纬度为度分秒格式
    def decimal_to_dms(decimal):
        is_positive = decimal >= 0
        decimal = abs(decimal)
        degrees = int(decimal)
        minutes = int((decimal - degrees) * 60)
        seconds = int(((decimal - degrees) * 60 - minutes) * 60 * 1000)
        return (
            (degrees, 1),
            (minutes, 1),
            (seconds, 1000)
        ), 'N' if is_positive else 'S' if latitude < 0 else 'E' if longitude > 0 else 'W'

    # 转换纬度
    lat_dms, lat_ref = decimal_to_dms(latitude)
    
    # 转换经度
    lon_dms, lon_ref = decimal_to_dms(longitude)
    
    # 创建GPS信息字典
    gps_ifd = {
        piexif.GPSIFD.GPSLatitude: lat_dms,
        piexif.GPSIFD.GPSLatitudeRef: lat_ref.encode(),
        piexif.GPSIFD.GPSLongitude: lon_dms,
        piexif.GPSIFD.GPSLongitudeRef: lon_ref.encode()
    }
    
    # 打开图片
    img = Image.open(image_path)


    # 获取原有的 EXIF 信息
    exif_dict = piexif.load(img.info['exif'])
    
    # 获取或设置 GPS 信息
    gps_info = exif_dict.get('GPS', {})
    
    # 更新 GPS 信息
    exif_dict['GPS'] = gps_ifd
    
    # 将exif信息转换为字节
    exif_bytes = piexif.dump(exif_dict)
    
    # 保存图片
    output = output_path
    img.save(output, 'JPEG', quality=100, exif=exif_bytes)
    print(f"GPS信息已更新：经度 {longitude}, 纬度 {latitude}")
    print(f"添加GPSInfo的图片已保存到： {output_path}","\n")

#批量处理文件夹内的图片
def process_images_in_folder(folder_path,  time, gps):
    for filename in os.listdir(folder_path):
        input_image_path = os.path.join(folder_path, filename)
        output_dir = "./已处理"
        output_image = os.path.join(output_dir, os.path.basename(input_image_path))
        if os.path.isfile(input_image_path):
            
            single_image_modify(input_image=input_image_path, 
                                output_image=output_image, 
                                time=time, 
                                gps=gps)

#单张图片处理   
def single_image_modify(input_image,output_image,time,gps):
    #需要修改的信息
    # time = b"2024:11:16 12:00:00"
    # gps = "118.798733,31.944514"  #南航：118.798733,31.944514  
    print("正在处理图片：",input_image)
    # 获取 EXIF 信息
    image = Image.open(input_image)
    exif_data = image._getexif()

    #判断照片是否有EXIF信息
    if exif_data:
        # 获取 TAG 名称与 ID 的映射
        datetime_tag_id = [key for key, value in ExifTags.TAGS.items() if value == "DateTimeOriginal"]
        gpsinfo_tag_id = [key for key, value in ExifTags.TAGS.items() if value == "GPSInfo"]
        print(f"datimID:{datetime_tag_id[0]}","\n")
        print(f"gpsInfoID:{gpsinfo_tag_id[0]}","\n")
        # print(exif_data)
        if datetime_tag_id and datetime_tag_id[0] in exif_data:
            print("存在 DateTime 标签")
            print(f"DateTime 值: {exif_data[datetime_tag_id[0]]}","\n")
        else:
            print("不存在 DateTime 标签\n")
            modify_exif_date(input_image, output_image, time)

        if datetime_tag_id and datetime_tag_id[0] in exif_data:
            if gpsinfo_tag_id and gpsinfo_tag_id[0] in exif_data:
                print("存在 GPSInfo 标签")
                print(f"GPSInfo 值: {exif_data[gpsinfo_tag_id[0]]}","\n")
            else:
                print("不存在 GPSInfo 标签")
                modify_exif_gps(input_image, output_image, gps)
        else:
            if gpsinfo_tag_id and gpsinfo_tag_id[0] in exif_data:
                print("存在 GPSInfo 标签")
                print(f"GPSInfo 值: {exif_data[gpsinfo_tag_id[0]]}","\n")
            else:
                print("不存在 GPSInfo 标签")
                modify_exif_gps(output_image, output_image, gps)
    else:
        print("没有 EXIF 信息,执行添加EXif程序···\n")
        modify_exif_date(input_image, output_image, time)
        modify_exif_gps(output_image, output_image, gps)
    print(input_image,"已处理完成")

def remove_all_exif(input_image, output_image):
    # 打开图像
    image = Image.open(input_image)
    # 移除 EXIF 信息（保存时不添加 EXIF 数据）
    image.save(output_image, "jpeg")
# Example usage
if __name__ == "__main__":
    input_image = "./img/IMG_20230503_162235.jpg"
    # output_dir1 = "./中间"
    # output_image_1 = os.path.join(output_dir1, os.path.basename(input_image))
    output_dir = "./已处理"
    output_image = os.path.join(output_dir, os.path.basename(input_image))
    folder_path = "./待处理"
    #需要修改的信息
    time = b"2023:05:03 12:00:00"
    gps = "116.74303,36.803186"  #南航：118.798733,31.944514  #御景城 116.74303,36.803186 #大清河116.759408,36.781846

    # remove_all_exif(input_image, output_image)
    # single_image_modify(output_image,output_image,time,gps)
    process_images_in_folder(folder_path, time, gps)
