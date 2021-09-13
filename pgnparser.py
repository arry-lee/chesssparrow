from collections import defaultdict
from PIL import Image,ImageDraw,ImageFont
import cv2 as cv
import numpy as np
from moviepy.editor import *
import math

from dhtmlxq import *
from idraw import circle_corner, draw_arrow


RED_CHESSMAN   = "車馬相仕帅砲兵"
BLACK_CHESSMAN = "车马象士将炮兵"


def pgn_reader(fp):
	"""读取pgn文件，返回字典信息与ICCS步骤"""
	info = dict()
	steps = list()
	with open(fp,'r') as pgn:
		for line in pgn:
			if line[0] == '[':
				k,v = line[1:-2].split(' ',1)
				info[k] = v[1:-1]

			elif '==' in line:
				break
			elif len(line)<6:
				break
			else:
				try:
					n,r,b = line.strip().split()
					# print(line)
					steps.append((int(n[0]),r,b))
				except:
					n,r = line.strip().split()
					steps.append((int(n[0]),r,None))
	return info,steps


def fen2txt(fen):
	"""读取fen文件，返回局面字符串"""
	fen = fen.split()[0]
	trans = {'k':'将','a':'士','b':'象','n':'马','r':'车','p':'卒','c':'炮',
			 'K':'帅','A':'仕','B':'相','N':'馬','R':'車','P':'兵','C':'砲',}
	board = []
	for l in fen.split('/'):
		line = ''
		for x in l:
			if x.isdigit():
				line += '〇'*int(x)
			else:
				line += trans[x]
		board.append(line)

	return '\n'.join(board)


def txt2board(txt):
	"""将局面字符串转化为二维棋盘数组"""
	board = [['〇' for i in range(9)] for j in range(10)]
	for i, line in enumerate(txt.split()):
		for j, piece in enumerate(line.strip()):
			board[i][j] = piece
	return board


def fen2board(fen):
	return txt2board(fen2txt(fen))


def board2txt(board):
	"""将二维棋盘数组转化为局面字符串"""
	return '\n'.join(''.join(line) for line in board)


def board2dict(board):
	"""将二维棋盘数组转化为字典"""
	board_dict = defaultdict(list)
	for i in range(10):
		for  j in range(9):
			if board[i][j] != '〇':
				board_dict[board[i][j]].append((i,j))
	return board_dict


def parse_step(step,board):
	"""按照step演变棋盘board,返回该步的信息,包括起始位置，结束位置，是否吃子"""
	if step[0] in '01*':
		return
	s = 'ABCDEFGHI'
	fc,fr = s.index(step[0]), 9 - int(step[1])
	tc,tr = s.index(step[3]), 9 - int(step[4])

	board[tr][tc] = board[fr][fc]
	board[fr][fc] = '〇'
	return (fc,fr),(tc,tr)


def _isred(chessman):
	return chessman in RED_CHESSMAN

def _chinese_num(num):
	# 大写数字
	return "〇一二三四五六七八九"[num]

def _simplify_chess(chessman):
	if chessman == '馬':
		return '马'
	elif chessman == '車':
		return '车'
	elif chessman == '砲':
		return '炮'
	else:
		return chessman


def iccs2chs(step,board):
	"""将 ICCS 坐标格式转换为中文纵线格式"""
	if step[0] in '01*':
		return
	s = 'ABCDEFGHI'
	fc,fr = s.index(step[0]), int(step[1])
	tc,tr = s.index(step[3]), int(step[4])

	chessman = board[9-fr][fc]
	
	if _isred(chessman):
		position = 9 - fc
	else:
		position = fc + 1

	dx = tc - fc # 横坐标变化
	dy = tr - fr # 纵坐标变化

	####################################################
	if dy > 0:
		direction = '进' if _isred(chessman) else '退'
		if chessman in '士象仕相马馬':
			destination = 9-tc if _isred(chessman) else tc + 1
		else:
			destination = dy

	elif dy == 0:
		direction = '平'
		destination = 9-tc if _isred(chessman) else tc + 1

	else:
		direction = '退' if _isred(chessman) else '进'
		if chessman in '士象仕相马馬':
			destination =  9-tc if _isred(chessman) else tc + 1
		else:
			destination = -dy

	if _isred(chessman):
		destination = _chinese_num(destination)
		position = _chinese_num(position)
	else:
		destination = str(destination)
		position = str(position)


	# 前后检测-------------------------------------
	boarddict = board2dict(board)
	every = boarddict.get(chessman)
	# print(chessman)
	every.sort()
	if len(every) == 2 and chessman not in '仕士象相':
		if every[0][1] == every[1][1]: #共线
			if 9-fr == every[0][0]:
				if _isred(chessman):
					cp = '前'+ _simplify_chess(chessman)
				else:
					cp = '后'+ _simplify_chess(chessman)

			elif 9-fr == every[1][0]:
				if _isred(chessman):
					cp = '后'+ _simplify_chess(chessman)
				else:
					cp = '前'+ _simplify_chess(chessman)
			else:
				pass

			return cp + direction + str(destination)

	elif len(every)>2: # 处理多兵的情况,及其少见，先pass
		pass


	return _simplify_chess(chessman) + str(position) + direction + str(destination)


def flip_board(board):
	nb = []
	for l in reversed(board):
		nb.append(list(reversed(l)))
	return nb


def board2pic(b,players = None,bg_color=(118,37,47), 
			  background=None, fr=None, to=None, choices=None,
			  comment=None,rotate=False,flip=False,blind=False):
	if flip is True:
		b = flip_board(b)

	new_screen = Image.new('RGB',(1920,1080),bg_color)
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

		for i in vlines[5:14]:
			draw.line((i,hlines[0])+(i,hlines[4]),fill='white',width=3)

		for i in vlines[5:14]:
			draw.line((i,hlines[5])+(i,hlines[-1]),fill='white',width=3)



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

		snow(vlines[7],hlines[3])
		snow(vlines[9],hlines[3])
		snow(vlines[11],hlines[3])
		lsnow(vlines[13],hlines[3])
		snow(vlines[6],hlines[2])
		snow(vlines[12],hlines[2])

		rsnow(vlines[5],hlines[-4])
		snow(vlines[7],hlines[-4])
		snow(vlines[9],hlines[-4])
		snow(vlines[11],hlines[-4])
		lsnow(vlines[13],hlines[-4])
		snow(vlines[6],hlines[-3])
		snow(vlines[12],hlines[-3])

		draw.line((vlines[5],hlines[4])+(vlines[5],hlines[5]),fill='white',width=3)
		draw.line((vlines[13],hlines[4])+(vlines[13],hlines[5]),fill='white',width=3)

		draw.line((vlines[8],hlines[0])+(vlines[10],hlines[2]),fill='white',width=2)
		draw.line((vlines[8],hlines[2])+(vlines[10],hlines[0]),fill='white',width=2)

		draw.line((vlines[8],hlines[-1])+(vlines[10],hlines[-3]),fill='white',width=2)
		draw.line((vlines[8],hlines[-3])+(vlines[10],hlines[-1]),fill='white',width=2)

		fontsize = 70
		font = ImageFont.truetype("src/font/李旭科书法.ttf", fontsize,encoding='gb')
		draw.text((vlines[6],hlines[4]+18), '楚河〇〇〇〇〇汉界' , font=font)

		
		draw.rectangle((vlines[5]-15,hlines[0]-15)+(vlines[13]+15,hlines[-1]+15),width=4,outline='white')
		t = new_screen.crop((vlines[5]-60,hlines[0]-60,vlines[13]+60,hlines[-1]+60))
		
		t.save('qp.png')

		draw.rectangle((vlines[5]-60,hlines[0]-60)+(vlines[13]+60,hlines[-1]+60),width=1)
		

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
	# 绘制棋子动线
	if fr and to:
		if not flip:
			fv,fh = board[fr[1]][fr[0]]
			tv,th = board[to[1]][to[0]]
		else:
			fv,fh = board[9-fr[1]][8-fr[0]]
			tv,th = board[9-to[1]][8-to[0]]

		draw.ellipse((tv-100//2,th-100//2)+(tv+100//2,th+100//2),width=8,outline='#20a162')
		draw.ellipse((fv-30//2,fh-30//2)+(fv+30//2,fh+30//2),width=3,fill='#20a162')
		# 引导线
		draw.line((fv,fh)+(tv,th),width=5,fill='#20a162')

	# 绘制棋子
	for i in range(9):
		for j in range(10):
			v,h = board[j][i]
			p = b[j][i]

			if p in '車馬相仕帅炮兵':
				color = '#82111f'
				bg_color = 'white'
			else:
				color = 'white'
				bg_color = 'black'

			# if p == '車':
			#     p = '车'
			# elif p == '馬':
			#     p = '马'
			# elif p == '砲':
			#     p = '炮'
			if p != '〇':
				# pass
				# draw.arc((v-100//2,h-100//2)+(v+100//2,h+100//2), start=0, end=360, fill=bg_color, width=0)
				# draw.ellipse((v-100//2,h-100//2)+(v+100//2,h+100//2),fill=bg_color)
				# draw.ellipse((v-88//2,h-88//2)+(v+88//2,h+88//2),width=3,outline=color)
				# draw.text((v-fontsize//2,h-fontsize//2), p , font=font,fill=color)

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

	if choices is not None:
		for i, choice in enumerate(choices):
			fr,to = parse_move(choice)

			if not flip:
				fv,fh = board[fr[1]][fr[0]]
				tv,th = board[to[1]][to[0]]
			else:
				fv,fh = board[9-fr[1]][8-fr[0]]
				tv,th = board[9-to[1]][8-to[0]]
			
			draw_arrow(draw,(fv,fh),(tv,th),fill='#20a162')

			# box = draw.textbbox((tv//2+fv//2,th//2+fh//2),str(i+1),font=zimu_font,anchor='mm')
			# draw.rectangle(box,width=3,outline='#20a162')

		for i, choice in enumerate(choices):
			fr,to = parse_move(choice)

			if not flip:
				fv,fh = board[fr[1]][fr[0]]
				tv,th = board[to[1]][to[0]]
			else:
				fv,fh = board[9-fr[1]][8-fr[0]]
				tv,th = board[9-to[1]][8-to[0]]

			x1,y1 = fv,fh
			x2,y2 = tv,th 
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

			p = (x2 - 60*math.cos(roate),y2 - 60*math.sin(roate))
			box = (tv//2+fv//2-zimu_fontsize//2,th//2+fh//2-zimu_fontsize//2,tv//2+fv//2+zimu_fontsize//2,th//2+fh//2+zimu_fontsize//2)
			draw.text(p,str(i+1),font=zimu_font,anchor='mm',fill='white')
			
	# 绘制前景
	# que = Image.open('src/que.png')
	# new_screen.paste(que,(vlines[16],0))

	top_l = Image.open('src/img/download/DH_bg_top_l.png').convert('RGBA')
	new_screen.paste(top_l,(0,0),mask=top_l)
	top_r = Image.open('src/img/download/DH_bg_top_r.png').convert('RGBA')
	new_screen.paste(top_r,(1920-top_r.width,0),mask=top_r)

	top_lu = Image.open('src/img/download/DH_bg_top_lu.png').convert('RGBA')
	new_screen.paste(top_lu,(1920-top_lu.width-200,0),mask=top_lu)

	down_l = Image.open('src/img/download/DH_bg_down_l.png').convert('RGBA')
	new_screen.paste(down_l,(0,1080-down_l.height),mask=down_l)

	down_r = Image.open('src/img/download/DH_bg_down_r.png').convert('RGBA')
	new_screen.paste(down_r,(1920-down_r.width,1080-down_r.height),mask=down_r)

	draw.text((1510,1035),'棋雀',font=comment_font)
	# 绘制评论
	if comment:
		# draw.text((vlines[3],th-comment_font_size//2),comment,font=comment_font)
		draw.text((vlines[9],hlines[8]),comment,font=zimu_font,anchor='mb',fill='white',stroke_width=3,stroke_fill='black')

	# hvhe = Image.open('src/img/download/DH_round_slot.png').convert('RGBA')
	# new_screen.paste(hvhe,(vlines[15],1080//2-hvhe.height//2),mask=hvhe)

	# hvhe1 = Image.open('src/img/download/DH_step_slot.png').convert('RGBA')
	# new_screen.paste(hvhe1,(vlines[15]+hvhe.width,1080//2-hvhe.height//2),mask=hvhe1)

	
	# draw.text((vlines[9],hlines[8]),'炮二平五',font=zimu_font,anchor='mb',fill='white',stroke_width=3,stroke_fill='black')
	# draw.text((vlines[9],hlines[1]),'马8进7',font=zimu_font,anchor='mt',fill='white',stroke_width=3,stroke_fill='black')


	return new_screen


def pgn2gif(pgn,out_file,flip=False,blind=False):
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
	board = txt2board(s)

	info,steps = pgn_reader(pgn)
	print(steps)

	frame = [board2pic(board,flip=flip,blind=blind)]
	for s in steps:

		cmt = iccs2chs(s[1],board) #招法

		fr,to = parse_step(s[1],board)
		frame.append(board2pic(board,fr=fr,to=to,comment=cmt,flip=flip,blind=blind))

		if s[2] is not None:
			cmt = iccs2chs(s[2],board)
			fr,to = parse_step(s[2],board)
			# print(board2txt(board))
			frame.append(board2pic(board,fr=fr,to=to,comment=cmt,flip=flip,blind=blind))

	frame.append(board2pic(board,flip=flip,blind=blind))

	# cv 写视频文件大
	# fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
	# out = cv.VideoWriter(out_file,fourcc, 1, (1920,1080),True)
	# for f in frame:
	# 	out.write(cv.cvtColor(np.array(f),cv.COLOR_RGB2BGR))
	# out.release()

	images_list = [np.array(f) for f in frame]
	le = len(images_list)
	if le>=47:			
		if le%2 == 0:
			durations = [47/(le-1)]*le
		else:
			durations = [47/le]*le
		ad = AudioFileClip('E:/00IT/P/chesssparrow/src/bgm/bgm.mp3',fps = 44100).set_start(0).set_duration(47)
	else:
		durations = [1]*le
		ad = AudioFileClip('E:/00IT/P/chesssparrow/src/bgm/bgm.mp3',fps = 44100).set_start(0).set_duration(le)
	clip = ImageSequenceClip(images_list,durations=durations)
	a = clip.set_audio(ad)
	a.write_videofile(out_file,fps=10)

	return frame


def pgn2txt(pgn,flip=False):
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
	fs = \
	"""
	車馬相仕帅仕相馬車
	〇〇〇〇〇〇〇〇〇
	〇砲〇〇〇〇〇砲〇
	兵〇兵〇兵〇兵〇兵
	〇〇〇〇〇〇〇〇〇
	〇〇〇〇〇〇〇〇〇
	卒〇卒〇卒〇卒〇卒
	〇炮〇〇〇〇〇炮〇
	〇〇〇〇〇〇〇〇〇
	车马象士将士象马车
	"""	
	if flip is True:
		board = txt2board(fs)
	else:
		board = txt2board(s)


	info,steps = pgn_reader(pgn)
	print(steps)

	frame = [board2txt(board)]
	for s in steps:

		cmt = iccs2chs(s[1],board) #招法

		fr,to = parse_step(s[1],board)
		frame.append(board2txt(board))

		if s[2] is not None:
			cmt = iccs2chs(s[2],board)
			fr,to = parse_step(s[2],board)
			# print(board2txt(board))
			frame.append(board2txt(board))
	return frame


def ubb2gif(ubb,out_file):
	binit, movelists = parse_tree(ubb)
	tt = MoveTree(movelists,board=binit)
	tt.compress()

	i = 0
	fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
	out = cv.VideoWriter(out_file,fourcc, 1, (1920,1080),True)
		
	

	for video in tt.video_generator():
		print('正在处理第%d个片段'% i )
		print(video)
		i = i + 1	
		for board,comment,choices,move in video:
			if len(choices)<=1:
				choices = None
			if move:
				fr,to = parse_move(move)
			else:
				fr,to = None,None
			
			frame = board2pic(board,comment=comment,fr=fr,to=to,choices=choices)
			out.write(cv.cvtColor(np.array(frame),cv.COLOR_RGBA2BGRA))

	out.release()
	return frame






class Board(object):
	def __init__(self,fen):
		if len(fen)>60:
			self.board = txt2board(fen)
		else:
			self.board = fen2board(fen)
		self.direction = 1

	def flip(self):
		self.direction = - self.direction
		new_board = []
		for l in reversed(self.board):
			new_board.append(list(reversed(l)))
		self.board = new_board

	def to_string(self):
		return '\n'.join(''.join(line) for line in board)

	def __str__(self):
		return self.to_string()


	def to_image(self,bg_color=(118,37,47), size=(1920,1080)):
		board_image = Image.new('RGB',size,bg_color)
		draw = ImageDraw.Draw(board_image)
		hlines =  sorted(list(range(484,0,-105))+list(range(593,1080,105)))
		vlines = sorted(list(set(list(range(960,0,-105))+list(range(960,1920,105)))))

		for i in hlines:
			draw.line((vlines[5],i)+(vlines[13],i),fill='white',width=3)

		for i in vlines[5:14]:
			draw.line((i,hlines[0])+(i,hlines[4]),fill='white',width=3)

		for i in vlines[5:14]:
			draw.line((i,hlines[5])+(i,hlines[-1]),fill='white',width=3)

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

		snow(vlines[7],hlines[3])
		snow(vlines[9],hlines[3])
		snow(vlines[11],hlines[3])
		lsnow(vlines[13],hlines[3])
		snow(vlines[6],hlines[2])
		snow(vlines[12],hlines[2])

		rsnow(vlines[5],hlines[-4])
		snow(vlines[7],hlines[-4])
		snow(vlines[9],hlines[-4])
		snow(vlines[11],hlines[-4])
		lsnow(vlines[13],hlines[-4])
		snow(vlines[6],hlines[-3])
		snow(vlines[12],hlines[-3])

		draw.line((vlines[5],hlines[4])+(vlines[5],hlines[5]),fill='white',width=3)
		draw.line((vlines[13],hlines[4])+(vlines[13],hlines[5]),fill='white',width=3)

		draw.line((vlines[8],hlines[0])+(vlines[10],hlines[2]),fill='white',width=2)
		draw.line((vlines[8],hlines[2])+(vlines[10],hlines[0]),fill='white',width=2)

		draw.line((vlines[8],hlines[-1])+(vlines[10],hlines[-3]),fill='white',width=2)
		draw.line((vlines[8],hlines[-3])+(vlines[10],hlines[-1]),fill='white',width=2)

		fontsize = 70
		font = ImageFont.truetype("src/font/李旭科书法.ttf", fontsize,encoding='gb')
		draw.text((vlines[6],hlines[4]+18), '楚河〇〇〇〇〇汉界' , font=font)

		
		draw.rectangle((vlines[5]-15,hlines[0]-15)+(vlines[13]+15,hlines[-1]+15),width=4,outline='white')
		draw.rectangle((vlines[5]-60,hlines[0]-60)+(vlines[13]+60,hlines[-1]+60),width=1)
			
		board = [[(v,h) for v in vlines[5:5+9]] for h in hlines[0:10]]

		for i in range(9):
			for j in range(10):
				v,h = board[j][i]
				p = self.board[j][i]

				if p in '車馬相仕帅炮兵':
					color = '#82111f'
					bg_color = 'white'
				else:
					color = 'white'
					bg_color = 'black'

				if p != '〇':
					chessman_folder='src/img/chess/'
					chess = Image.open(chessman_folder + p + '.png')
					w = 120
					chess = chess.resize((w,w))
					board_image.paste(chess,(v-w//2,h-w//2)+(v+w//2,h+w//2),mask=chess)

		# top_l = Image.open('src/img/download/DH_bg_top_l.png').convert('RGBA')
		# board_image.paste(top_l,(0,0),mask=top_l)
		# top_r = Image.open('src/img/download/DH_bg_top_r.png').convert('RGBA')
		# board_image.paste(top_r,(1920-top_r.width,0),mask=top_r)

		# top_lu = Image.open('src/img/download/DH_bg_top_lu.png').convert('RGBA')
		# board_image.paste(top_lu,(1920-top_lu.width-200,0),mask=top_lu)

		# down_l = Image.open('src/img/download/DH_bg_down_l.png').convert('RGBA')
		# board_image.paste(down_l,(0,1080-down_l.height),mask=down_l)

		# down_r = Image.open('src/img/download/DH_bg_down_r.png').convert('RGBA')
		# board_image.paste(down_r,(1920-down_r.width,1080-down_r.height),mask=down_r)

		return board_image

	def show(self):
		self.board_image = self.to_image()
		self.board_image.show()


if __name__ == '__main__':
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

	b = Board(s)
	b.flip()
	b.show()
	# ubb2gif('md.ubb','md.mp4')
	# b = '7999999949999999699977999985523140994299509999999999991738475899'
	# print(binit2board(b))
	# board2pic(binit2board(b)).show()

	# board2pic(txt2board(s),background=False,players=None,choices=['0003','0006','0012','0050','5343','3343','4243','4443']).show()
	# from bili import comment

	# import time
	# frame =pgn2txt('src/pgn/5.pgn')
	# frame.reverse()

	# for f in frame[1:]:
	# 	comment(f,video=)
	# 	print(f)
	# 	time.sleep(1)

	# with open('src/pgn/wty.txt','w',encoding='utf-8') as f:
	# 	for t in frame:
	# 		f.write(t)
	# 		f.write('\n\n')

	# lst = pgn2gif('src/pgn/4.pgn','src/video/4.mp4',flip=False)
	# images_list = [np.array(f) for f in lst]
	# beat_times = np.array([   0,   520,   984,  1460,  1925,  2389,  2854,  3309,  3782,  4247,
	#   4711,  5175,  5626,  6104,  6947,  7280,  7486,  7961,  8415,  8880,
	#   9343,  9808, 10284, 10736, 11199, 11666, 12130, 12592, 13057, 13504,
	#  13988, 14701, 14916, 15393, 16242, 16701, 17040, 17233, 17704, 18435,
	#  18634, 19107, 19945, 20025, 20489, 20935, 21807, 22141, 22357, 22791,
	#  23276, 24006, 24203, 24942, 25145, 25598, 26062, 26512, 27002, 27722,
	#  27931, 28653, 28860, 29572, 29788, 30240, 30704, 31171, 31902, 32111,
	#  32575, 33301, 33490, 33968, 34421, 34886, 35352, 35815, 36290, 36998,
	#  37211, 37671, 38148, 38601, 39077, 39529, 39994, 40458, 40875, 41399,
	#  41853, 42704, 42782, 43199, 43709, 44427, 44660, 45135, 45600, 46064])/1000

	# print(beat_times)
	# start = 0
	# end = 1 
	# duration = []
	# while end < len(beat_times):

	# 	if beat_times[end] - beat_times[start] > 0.4:
	# 		duration.append((beat_times[end]-beat_times[start]))
	# 		start = end 
	# 		end = start + 1
	# 	else:
	# 		end = end + 1

	# print(len(duration))

	# le = len(images_list)

	# durations = [47/le]*le

	# # print(len(duration))

	

	# ad = AudioFileClip('E:/00IT/P/棋雀/src/bgm/bgm.mp3',fps = 44100).set_start(0).set_duration(47)
	# clip = ImageSequenceClip(images_list,durations=durations)
	
	# a = clip.set_audio(ad)
	# a.write_videofile('test2.mp4',fps=5)
