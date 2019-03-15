# -*- coding: utf-8 -*-
# @Time    : 2019/3/15 0015 23:29
# @Author  : __Yanfeng
# @Site    : 
# @File    : storage.py
# @Software: PyCharm
from io import BytesIO

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ImageDraw, ImageFont


class WatermarkStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        """重写save方法,在储存图片的时候对图片加水印"""
        if 'image' in content.content_type:
            image = self.watermark_with_text(content, 'LeeBlog.com', 'red')
            content = self.convert_image_to_file(image, name)
        return super(WatermarkStorage, self).save(name, content, max_length=max_length)

    @staticmethod
    def convert_image_to_file(image, name):
        tmp = BytesIO()
        image.save(tmp, format='PNG')
        file_size = tmp.tell()
        return InMemoryUploadedFile(tmp, None, name, 'image/png', file_size, None)

    @staticmethod
    def watermark_with_text(file_obj, text, color, fontfamily=None):
        image = Image.open(file_obj).convert("RGBA")
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        if fontfamily:
            font = ImageFont.truetype(fontfamily, int(height / 20))
        else:
            font = None
        textWidth, textHeight = draw.textsize(text, font)
        x = (width - textWidth - margin) / 2  # 计算横坐标的位置
        y = (height - textHeight - margin)  # 计算纵坐标的位置
        draw.text((x, y), text, color, font)
        return image
