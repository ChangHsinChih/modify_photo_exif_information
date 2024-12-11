from PIL import Image

# 打开PNG图片
image = Image.open('待处理\***.png')
image = image.convert('RGB')
# 转换为JPG格式并保存
quality = 100
image.save('***.jpg', 'JPEG', quality=quality)
