#!/usr/bin/env python
#coding:utf-8
'''
    python图片处理
    @author:fc_lamp
    @blog:http://fc-lamp.blog.163.com/
'''
#该代码片段来自于: http://www.sharejs.com/codes/python/5927
import Image, ImageEnhance, ImageFilter
import sys
import glob
import os
import os.path


def dropShadow( image, offset=(5,5), background=0xffffff,
        shadow=0x444444, border=8, iterations=3):
    """
    把图像放在一个作了高斯模糊的背景上

    image       - 要放在背景上的原始图像
    offset      - 阴影相对图像的偏移，用(x,y)表示，可以为正数或者负数
    background - 背景色
    shadow      - 阴影色
    border      - 图像边框，必须足够用来制作阴影模糊
    iterations - 过滤器处理次数，次数越多越模糊，当然处理过程也越慢
    """

    # 创建背景块
    totalWidth = image.size[0] + abs(offset[0]) + 2*border
    totalHeight = image.size[1] + abs(offset[1]) + 2*border
    back = Image.new(image.mode, (totalWidth, totalHeight), background)

    # 放置阴影块，考虑图像偏移
    shadowLeft = border + max(offset[0], 0)
    shadowTop = border + max(offset[1], 0)
    back.paste(shadow, [shadowLeft, shadowTop, shadowLeft + image.size[0],
        shadowTop + image.size[1]] )

    # 处理阴影的边缘模糊
    n = 0
    while n < iterations:
        back = back.filter(ImageFilter.BLUR)
        n += 1

    # 把图像粘贴到背景上
    imageLeft = border - min(offset[0], 0)
    imageTop = border - min(offset[1], 0)
    back.paste(image, (imageLeft, imageTop))

    return back


def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    else:
        layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)

#等比例压缩图片
def resizeImg(im, **args):
    args_key = {'result':'','dst_w':'','dst_h':'','save_q':75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]

    ori_w,ori_h = im.size
    widthRatio = heightRatio = None
    ratio = 1
    if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
        if arg['dst_w'] and ori_w > arg['dst_w']:
            widthRatio = float(arg['dst_w']) / ori_w #正确获取小数的方式
        if arg['dst_h'] and ori_h > arg['dst_h']:
            heightRatio = float(arg['dst_h']) / ori_h
        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio
        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio
        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h
    print newWidth, newHeight
    im = im.resize((newWidth,newHeight),Image.ANTIALIAS)#.save(arg['result'],quality=arg['save_q'])
    im.save(arg['result'])
    return True

    '''
    Image.ANTIALIAS还有如下值：
    NEAREST: use nearest neighbour
    BILINEAR: linear interpolation in a 2x2 environment
    BICUBIC:cubic spline interpolation in a 4x4 environment
    ANTIALIAS:best down-sizing filter
    '''
#裁剪压缩图片
def clipResizeImg(im, **args):
    args_key = {'result':'','dst_w':'','dst_h':'','save_q':75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]
    ori_w,ori_h = im.size
    dst_scale = float(arg['dst_h']) / arg['dst_w'] #目标高宽比
    ori_scale = float(ori_h) / ori_w #原高宽比
    if ori_scale >= dst_scale:  #过高
        width = ori_w
        height = int(width*dst_scale)
        x = 0
        y = (ori_h - height) / 3
    else:  #过宽
        height = ori_h
        width = int(height*dst_scale)
        x = (ori_w - width) / 2
        y = 0
    #裁剪
    box = (x,y,width+x,height+y)
    #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    #所包围的图像，crop方法与php中的imagecopy方法大为不一样
    im = im.crop(box)
    #im = None
    #压缩
    ratio = float(arg['dst_w']) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    im.resize((newWidth,newHeight),image.ANTIALIAS)#.save(arg['result'],quality=arg['save_q'])
    return True

#水印(这里仅为图片水印)
def waterMark(im,**args):
    args_key = {'result':'','mark':'','pos':''}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]
    #im = Image.open(arg['source'])
    ori_w,ori_h = im.size
    mark_im = Image.open(arg['mark'])
    mark_w,mark_h = mark_im.size
    option ={'leftup':(0,0),
             'rightup':(ori_w-mark_w,0),
             'leftlow':(0,ori_h-mark_h),
             'rightlow':(ori_w-mark_w,ori_h-mark_h)
             }
    im.paste(mark_im,option[arg['pos']],mark_im.convert('RGBA'))
    #im.save(arg['result'])
    return True

def handle_image(source, mark, result, w = 150, h = 150, quality = 35, pos = 'rightlow'):
    im = Image.open(source)
    #mark = Image.open('logo.png')
    #watermark(im, mark, 'tile', 0.5).show()
    #watermark(im, mark, 'scale', 1.0).show()
    #watermark(im, mark, (100, 100), 0.5).show()

    #clipResizeImg(source=source,result=result,dst_w=w,dst_h=h,save_q = quality)
    resizeImg(im, source=source,result=result,dst_w=w,dst_h=h,save_q = quality)
    #waterMark(im,result=result,mark=mark,pos=pos)

    #im.thumbnail( (300,300), Image.ANTIALIAS)

    #dropShadow(im).show()
    #dropShadow(im, background=0xeeeeee,
    #              shadow=0x444444, offset=(0,5)).save(result)

    #im.save(result)


if __name__ == '__main__':
    script_path = os.path.dirname(sys.argv[0])
    files = []
    for format in ["jpg", "png", "gif"]:
        #files.append(glob.glob(os.path.join(script_path, "*." + format)))
        files = files + glob.glob(os.path.join(script_path, "*." + format))

    dest_dir = os.path.join(script_path, "..", "out", "img")
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir, 0644)

    mark = os.path.join(script_path , 'logo.png')
    for f in files:
        if f == mark:
            continue
        dest = os.path.join(dest_dir,  os.path.basename(f))
        handle_image(f, mark, dest)
