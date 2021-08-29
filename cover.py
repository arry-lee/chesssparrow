from PIL import Image,ImageDraw,ImageFont
import numpy as np
from moviepy.editor import *


# 想做一个python的特效库

def typein(title,outfp,duration,font="src/font/李旭科书法.ttf",fontsize=80):
	"""文字键入的效果"""
	font = ImageFont.truetype(font, fontsize,encoding='gb')
	length = len(title)
	a = Image.new('RGB',(length*fontsize,fontsize),'white')
	draw = ImageDraw.Draw(a)

	cps = length//duration
	# 一字一帧
	p = int(duration*1000//length)

	def makeframe(t):
		"""第1000"""
		# 0 - x -> 0
		# x - 2x -> 1

		# duration - > length-1
		if t<duration:
			draw.text((int(t*1000//p)*fontsize,0),title[int(t*1000//p)],font=font,fill='black')
			return np.array(a)
		else:
			return np.array(a)

	vc = VideoClip(makeframe,duration=duration+1)
	vc.write_gif(outfp,fps=cps)



def fadein(title,outfp,duration,font="src/font/李旭科书法.ttf",fontsize=80):
	font = ImageFont.truetype(font, fontsize,encoding='gb')
	length = len(title)
	a = Image.new('RGB',(length*fontsize,fontsize),'white')
	draw = ImageDraw.Draw(a)
	draw.text((0,0),title,font=font,fill='black')

	pps = length*fontsize//(duration)
	# 一字一帧
	p = int(duration//length)

	def makeframe(t):
		t = int(t*pps)
		x = np.array(a)
		x[:,t:] = (255,255,255)
		return x
	vc = VideoClip(makeframe,duration=duration)
	vc.write_gif(outfp,fps=24)


# fadein("你好",'n.gif',1)
def cover(font="src/font/李旭科书法.ttf",fontsize=80):
	font = ImageFont.truetype(font, fontsize,encoding='gb')
	img = Image.open('src/img/大师风范.jpg')
	w,h = img.size
	n = img.resize((w*1080//h,1080))
	# img.show()
	# print(w,h)
	color = n.getpixel((10,10))
	# cover = Image.new('RGB',(1920,1080),color)
	cover = Image.open('src/img/boadwood.png')
	cover.paste(n,(100,0))
	
	draw = ImageDraw.Draw(cover)
	draw.text((760,240),'第六局棋 七夕',font=font,fill='white')
	draw.text((960,380),'你要那对象有何用',font=font,fill='white')
	draw.text((960,540),'隐藏成就,兵不血刃达成！',font=font,fill='black')

	cover.save('cover.png')
	return cover
# 好的封面要包含哪些元素


# def add_cover(video,cover):


# import re

# p = re.compile(r'/.*png')

# a = set()

# with open('log.log',encoding='utf-8') as f:
# 	for line in f:
# 		g = p.search(line)
# 		if g:
# 			a.add(g[0])

# print(len(a))
# for x in a:
# 	print(x)

# import requests

# def download(url):
# 	fn = url.split('/')[-1]
# 	a = requests.get(url)
# 	if a.ok:
# 		with open(fn,'wb') as f:
# 			f.write(a.content)

# i = len(a)
# for p in a:
# 	download(p)
# 	print(i)
# 	i = i-1

def ccrop():
	im = Image.open('ChessManAtlas_heibai.png')
	print(im.size)

	im.crop((0,0,80,80)).save('src/img/heibai/兵.png')
	im.crop((80,0,160,80)).save('src/img/heibai/炮.png')
	im.crop((160,0,240,80)).save('src/img/heibai/馬.png')
	im.crop((240,0,320,80)).save('src/img/heibai/車.png')
	im.crop((320,0,400,80)).save('src/img/heibai/相.png')
	im.crop((400,0,480,80)).save('src/img/heibai/仕.png')
	im.crop((480,0,560,80)).save('src/img/heibai/帅.png')
	im.crop((560,0,640,80)).save('src/img/heibai/〇.png')

	im.crop((0,80,80,160)).save('src/img/heibai/卒.png')
	im.crop((80,80,160,160)).save('src/img/heibai/砲.png')
	im.crop((160,80,240,160)).save('src/img/heibai/马.png')
	im.crop((240,80,320,160)).save('src/img/heibai/车.png')
	im.crop((320,80,400,160)).save('src/img/heibai/象.png')
	im.crop((400,80,480,160)).save('src/img/heibai/士.png')
	im.crop((480,80,560,160)).save('src/img/heibai/将.png')
	im.crop((560,80,640,160)).save('src/img/heibai/〇1.png')

# print(a.size)
# b = im.crop((80,0,160,80))
# print(b.size)





