from moviepy.editor import *
from PIL import Image,ImageDraw,ImageFont
import numpy as np
from pgnparser import txt2board

def board2pic(b,players = None,bg_color=(118,37,47), 
			  background=None, fr=None, to=None, choices=None,
			  comment=None,rotate=False,blind=False):
	frames = []
	new_screen = Image.new('RGB',(1920,1080),bg_color)
	frames.append(new_screen.copy())

	if background is not None:
		try:
			new_screen = Image.open(background)
		except Exception as e:
			pass

	if background:
		boardpic = Image.open('src/img_chessboard_11.png')
		w,h = boardpic.size
		new_screen.paste(boardpic,(1920//2-w//2+3,0))


	draw = ImageDraw.Draw(new_screen)
	hlines =  sorted(list(range(484,0,-105))+list(range(593,1080,105)))
	vlines = sorted(list(set(list(range(960,0,-105))+list(range(960,1920,105)))))

	if not background:
		# 参考线
		# 大棋盘框
		


		for i in hlines:
			draw.line((vlines[5],i)+(vlines[13],i),fill='white',width=3)
			# frames.append(new_screen.copy())

		for i in vlines[5:14]:
			if i == vlines[5] or i == vlines[13]:
				draw.line((i,hlines[0])+(i,hlines[-1]),fill='white',width=3)
			draw.line((i,hlines[0])+(i,hlines[4]),fill='white',width=3)
			draw.line((i,hlines[5])+(i,hlines[-1]),fill='white',width=3)
			# frames.append(new_screen.copy())

		draw.line((vlines[8],hlines[0])+(vlines[10],hlines[2]),fill='white',width=2)
		# frames.append(new_screen.copy())
		draw.line((vlines[8],hlines[2])+(vlines[10],hlines[0]),fill='white',width=2)
		# frames.append(new_screen.copy())
		draw.line((vlines[8],hlines[-1])+(vlines[10],hlines[-3]),fill='white',width=2)
		# frames.append(new_screen.copy())
		draw.line((vlines[8],hlines[-3])+(vlines[10],hlines[-1]),fill='white',width=2)
		# frames.append(new_screen.copy())

		def snow(x,y,d=8,l=16):
			draw.line((x+d,y+d)+(x+d,y+d+l),width=1)
			draw.line((x+d,y+d)+(x+d+l,y+d),width=1)

			draw.line((x-d+1,y-d+1)+(x-d+1,y-d+1-l),width=1)
			draw.line((x-d+1,y-d+1)+(x-d+1-l,y-d+1),width=1)

			draw.line((x-d+1,y+d)+(x-d+1,y+d+l),width=1)
			draw.line((x-d+1,y+d)+(x-d+1-l,y+d),width=1)

			draw.line((x+d,y-d+1)+(x+d,y-d+1-l),width=1)
			draw.line((x+d,y-d+1)+(x+d+l,y-d+1),width=1)

		def lsnow(x,y,d=8,l=16):
			draw.line((x-d+1,y-d+1)+(x-d+1,y-d+1-l),width=1)
			draw.line((x-d+1,y-d+1)+(x-d+1-l,y-d+1),width=1)

			draw.line((x-d+1,y+d)+(x-d+1,y+d+l),width=1)
			draw.line((x-d+1,y+d)+(x-d+1-l,y+d),width=1)

		def rsnow(x,y,d=8,l=16):
			draw.line((x+d,y+d)+(x+d,y+d+l),width=1)
			draw.line((x+d,y+d)+(x+d+l,y+d),width=1)

			draw.line((x+d,y-d+1)+(x+d,y-d+1-l),width=1)
			draw.line((x+d,y-d+1)+(x+d+l,y-d+1),width=1)

		rsnow(vlines[5],hlines[3])
		# frames.append(new_screen.copy())
		snow(vlines[7],hlines[3])
		# frames.append(new_screen.copy())
		snow(vlines[9],hlines[3])
		# frames.append(new_screen.copy())
		snow(vlines[11],hlines[3])
		# frames.append(new_screen.copy())
		lsnow(vlines[13],hlines[3])
		# frames.append(new_screen.copy())
		snow(vlines[6],hlines[2])
		# frames.append(new_screen.copy())
		snow(vlines[12],hlines[2])
		# frames.append(new_screen.copy())

		rsnow(vlines[5],hlines[-4])
		# frames.append(new_screen.copy())
		snow(vlines[7],hlines[-4])
		# frames.append(new_screen.copy())
		snow(vlines[9],hlines[-4])
		# frames.append(new_screen.copy())
		snow(vlines[11],hlines[-4])
		# frames.append(new_screen.copy())
		lsnow(vlines[13],hlines[-4])
		# frames.append(new_screen.copy())
		snow(vlines[6],hlines[-3])
		# frames.append(new_screen.copy())
		snow(vlines[12],hlines[-3])
		# frames.append(new_screen.copy())



		fontsize = 70
		font = ImageFont.truetype("src/font/李旭科书法.ttf", fontsize,encoding='gb')
		draw.text((vlines[6],hlines[4]+18), '楚河〇〇〇〇〇汉界' , font=font)
		# frames.append(new_screen.copy())
		
		draw.rectangle((vlines[5]-15,hlines[0]-15)+(vlines[13]+15,hlines[-1]+15),width=4,outline='white')
		# frames.append(new_screen.copy())
		draw.rectangle((vlines[5]-60,hlines[0]-60)+(vlines[13]+60,hlines[-1]+60),width=1)		
		frames.append(new_screen.copy())
		frames.append(new_screen.copy())
		frames.append(new_screen.copy())
	# 绘制对弈双方信息


	# 头像框
	hvhe_font_size = 40
	hvhe_font = ImageFont.truetype("src/font/msyh.ttc", hvhe_font_size,encoding='gb')

	if players is not None: # 如果没有对局双方信息
		red_tou = Image.open('src/wang_tian_yi.jpg').resize((220,220))
		black_tou = Image.open('src/zheng_wei_tong.jpg').resize((220,220))
		delta = 0
		xdelta = 10
		new_screen.paste(black_tou,(vlines[1]+xdelta,hlines[6]+delta),mask=circle_corner(black_tou,110))
		draw.text((vlines[1]+xdelta,hlines[5]), '郑惟桐' , font=font, fill=(138,40,30),stroke_width=3,stroke_fill='white')
		draw.text((vlines[2]-35+xdelta,hlines[4]+18), 'VS' , font=font, fill='white')
		new_screen.paste(red_tou,(vlines[1]+xdelta,hlines[1]-delta),mask=circle_corner(red_tou,110))
		draw.text((vlines[1]+xdelta,hlines[4]-70), '王天一' , font=font, fill='black',stroke_width=3,stroke_fill='white')




	board = [[(v,h) for v in vlines[5:5+9]] for h in hlines[0:10]]

	comment_font_size = 30
	comment_font = ImageFont.truetype("src/font/FZKT.TTF", comment_font_size,encoding='gb')
	zimu_fontsize = 24
	zimu_font = ImageFont.truetype("src/font/msyh.ttc", zimu_fontsize,encoding='gb')


	# 绘制棋子
	for i in [4,3,5,2,6,1,7,0,8]:
		for j in range(10):
			v,h = board[j][i]
			p = b[j][i]

			if p in '車馬相仕帅炮兵':
				color = '#82111f'
				bg_color = 'white'
			else:
				color = 'white'
				bg_color = 'black'
			if p != '〇':
				if blind == True:
					chess = Image.open('src/img/chess/〇.png')
				else:
					chessman_folder='src/img/chess/'
					chess = Image.open(chessman_folder + p + '.png')
				w = 120
				chess = chess.resize((w,w))
				if rotate is True and not _isred(p):
					chess = chess.rotate(180)
				new_screen.paste(chess,(v-w//2,h-w//2)+(v+w//2,h+w//2),mask=chess)
		frames.append(new_screen.copy())
	frames.append(new_screen.copy())
	frames.append(new_screen.copy())
	top_l = Image.open('src/img/download/DH_bg_top_l.png').convert('RGBA')
	new_screen.paste(top_l,(0,0),mask=top_l)
	frames.append(new_screen.copy())
	top_r = Image.open('src/img/download/DH_bg_top_r.png').convert('RGBA')
	new_screen.paste(top_r,(1920-top_r.width,0),mask=top_r)
	frames.append(new_screen.copy())
	top_lu = Image.open('src/img/download/DH_bg_top_lu.png').convert('RGBA')
	new_screen.paste(top_lu,(1920-top_lu.width-200,0),mask=top_lu)
	frames.append(new_screen.copy())
	down_l = Image.open('src/img/download/DH_bg_down_l.png').convert('RGBA')
	new_screen.paste(down_l,(0,1080-down_l.height),mask=down_l)
	frames.append(new_screen.copy())
	down_r = Image.open('src/img/download/DH_bg_down_r.png').convert('RGBA')
	new_screen.paste(down_r,(1920-down_r.width,1080-down_r.height),mask=down_r)
	frames.append(new_screen.copy())
	frames.append(new_screen.copy())
	frames.append(new_screen.copy())	
	frames.append(new_screen.copy())
	frames.append(new_screen.copy())


	return frames

# 棋盘绘制 1s
s = \
"""
车马象士将士象马车
〇〇〇〇〇〇〇〇〇
〇炮〇〇〇〇〇炮〇
卒〇卒〇卒〇卒〇卒
〇〇〇〇〇〇〇〇〇
〇〇〇〇〇〇〇〇〇
兵〇兵〇兵〇兵〇兵
〇砲〇〇〇〇〇砲〇
〇〇〇〇〇〇〇〇〇
車馬相仕帅仕相馬車
"""
frames = board2pic(txt2board(s))

images_list = [np.array(f) for f in frames]
le = len(images_list)
durations = [2/le]*le
clip = ImageSequenceClip(images_list,durations=durations)

clip.write_videofile('header.mp4',fps=10)
