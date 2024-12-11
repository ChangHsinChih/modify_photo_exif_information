# modify_photo_exif_information
pngTojpg.py文件用于将png图片转换为jpg文件，因为png可能无法存储exif信息。  
class.py文件用于将照片进行分类，无exif信息；无date和GPSinfo；无GPSinfo和无GPSinfo四类。  
addExif.py文件用于给照片添加拍摄时间和GPS位置信息，如果照片本身含有时间或者GPS会跳过，添加未有的信息，支持文件夹操作。