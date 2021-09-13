"""图像绘制的自定义函数"""

import math
from PIL import Image, ImageDraw

def circle_corner(img, radii):  #把原图片变成圆角，这个函数是从网上找的，原址 https://www.pyget.cn/p/185266
	"""
	圆角处理
	:param img: 源图象。
	:param radii: 半径，如：30。
	:return: 返回蒙版。
	"""
	# 画圆（用于分离4个角）
	circle = Image.new('1', (radii * 2, radii * 2), 0)  # 创建一个黑色背景的画布
	draw = ImageDraw.Draw(circle)
	draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 画白色圆形
	# 原图
	img = img.convert("RGBA")
	w, h = img.size
	# 画4个角（将整圆分离为4个部分）
	alpha = Image.new('1', img.size, 255)
	alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
	alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
	alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
	alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角
	# alpha.show()
	# img.putalpha(alpha)  # 白色区域透明可见，黑色区域不可见
	return alpha

def draw_arrow(draw,fr,to,fill,arrow_length=60,arrow_width=30):
	# draw.line((x1,y1)+(x2,y2))
	x1,y1 = fr
	x2,y2 = to 
	pi = math.pi

	length = math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))

	if x1!=x2:
		if y1==y2:
			if x2>x1:
				roate = 0
			else:
				roate = pi
		else:
			roate = math.atan((y2-y1)/(x2-x1))
	else:
		if y2>y1:
			roate = pi/2
		else:
			roate = -pi/2

	p = (x2 - arrow_length*math.cos(roate),y2 - arrow_length*math.sin(roate))
	p1 = (p[0] + arrow_width//2*math.cos(roate+pi/2),p[1] + arrow_width//2*math.sin(roate+pi/2))
	p11 = (p[0] + arrow_width//4*math.cos(roate+pi/2),p[1] + arrow_width//4*math.sin(roate+pi/2))

	p2 = (p[0] + arrow_width//2*math.cos(roate-pi/2),p[1] + arrow_width//2*math.sin(roate-pi/2))
	p22 = (p[0] + arrow_width//4*math.cos(roate-pi/2),p[1] + arrow_width//4*math.sin(roate-pi/2))
	draw.polygon([fr,p11,p1,to,p2,p22],fill= fill)
	draw.point(fr)