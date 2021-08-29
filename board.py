from PIL import Image
import cv2 as cv
import numpy as np
import random
from PIL import Image,ImageDraw,ImageFilter,ImageFont


QIZI_CENTER = (69,56)
BOX_WIDTH = 115
BOX_HEIGHT = 115
board_box = (40,395,1040,1508)



class ChessBoard(object):
	"""" 将棋盘转化为文本
	1.灰度化
	2.找圆
	3.按圆心，半径裁剪
	4.与模板对比得到名字

	"""
	template = []

	def __init__(self,fp):
		if fp !='y.png':
			self.__init__('y.png')

		self.origin =  cv.imread(fp)[355:1548, 0:1080]
		self.gray = cv.cvtColor(self.origin,cv.COLOR_BGR2GRAY)
		board_blur = cv.GaussianBlur(self.gray,(5,5),0)
		self.board_canny = cv.Canny(board_blur,0,266)

		self._qizi = [[None for i in range(9)] for j in range(10)]
		self.board = [['〇' for i in range(9)] for j in range(10)]

		self.color = [[None for i in range(9)] for j in range(10)]

		self._circle() # 第一次
		self._parse()

	def _circle(self):
		"""圈出所有棋子，按其圆心坐标保存
		"""
		self.cover = np.zeros(self.origin.shape)

		board_circle = cv.HoughCircles(self.board_canny,cv.HOUGH_GRADIENT,1,20,
			 param1=50,param2=30,minRadius=30,maxRadius=50)
		circles = np.uint32(np.around(board_circle))

		x0 = np.min(circles[0,:,0])
		y0 = np.min(circles[0,:,1])

		if not ChessBoard.template: # 模板要小
			r = np.max(circles[0,:,2])
		else:
			r = np.max(circles[0,:,2])+4# 被匹配的局部


		w =  (np.max(circles[0,:,0]) - np.min(circles[0,:,0]))//8
		h=  (np.max(circles[0,:,1]) - np.min(circles[0,:,1]))//9

		for index,i in enumerate(circles[0,:]):
			x = x0+(round((i[0]-x0)/w))*w
			# y = y0+(round((i[1]-y0)/h))*h
			y = i[1]

			q = self.origin[y-r:y+r,x-r:x+r]
			# cv.imshow('')
			col = round((i[0]-x0)/w)
			row = round((i[1]-y0)/h)

			co = self.color[row][col]
			rr = r 

			cv.circle(self.cover,(x,y),rr,co,-1)
			# cv.putText(self.cover,str(index),(x,y),cv.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)
			self._qizi[row][col] = q

		# cv.imshow('',self.cover)
		# cv.waitKey(0)

		if not ChessBoard.template: # 只在第一次保存模板
			b = {'红车':(0,0),'红马':(0,1),'红相':(0,2),'红仕':(0,3),'红帅':(0,4),'红炮':(2,1),'红兵':(3,0),
				 '红2车':(0,8),'红2马':(0,7),'红2相':(0,6),'红2仕':(0,5),'红2炮':(2,7),
				 '黑車':(9,0),'黑馬':(9,1),'黑象':(9,2),'黑士':(9,3),'黑将':(9,4),'黑砲':(7,1),'黑卒':(6,0),
				 '黑2車':(9,8),'黑2馬':(9,7),'黑2象':(9,6),'黑2士':(9,5),'黑2砲':(7,7)}
			for k,v in b.items():
				i = v[0]
				j = v[1]
				ChessBoard.template.append((k,self._qizi[i][j]))

	def _parse(self):
		for i in range(10):
			for j in range(9):
				q = self._qizi[i][j]
				if q is not None:
					max0 = 0
					name = ''
					for n,t in ChessBoard.template:
						result = cv.matchTemplate(q,t,cv.TM_CCOEFF_NORMED)
						_,maxv,_,_ = cv.minMaxLoc(result)
						if maxv >= max0: # 找相似度最高的模板
							max0 = maxv
							name = n 
					self.board[i][j] = name[-1]
					self.color[i][j] = (255,0,0) if name[0] == '红' else (255,255,255)

	# def _cover(self):
	# 	self._circle()
		# cv.imwrite('src/img/brw.png',self.cover)

		# cv.imshow('',self.cover)
		# cv.waitKey(0)
		# cv.destroyAllWindows()


	def __str__(self):
		s = ''
		for b in self.board:
			s +=''.join(b)+'\n'
		return s

	def get_cover(self):
		self._circle()
		new_screen = Image.new('RGB',(1920,1080),(0,0,0))
		draw = ImageDraw.Draw(new_screen)
		hlines =  sorted(list(range(484,0,-105))+list(range(593,1080,105)))
		vlines = sorted(list(set(list(range(960,0,-105))+list(range(960,1920,105)))))
		# 参考线
		for i in hlines:
			draw.line((vlines[5],i)+(vlines[13],i),fill='white',width=2)
		for i in vlines[5:14]:
			draw.line((i,hlines[0])+(i,hlines[4]),fill='white',width=2)
		for i in vlines[5:14]:
		    draw.line((i,hlines[5])+(i,hlines[-1]),fill='white',width=2)

		draw.line((vlines[8],hlines[0])+(vlines[10],hlines[2]),fill='white',width=2)
		draw.line((vlines[8],hlines[2])+(vlines[10],hlines[0]),fill='white',width=2)
		draw.line((vlines[8],hlines[-1])+(vlines[10],hlines[-3]),fill='white',width=2)
		draw.line((vlines[8],hlines[-3])+(vlines[10],hlines[-1]),fill='white',width=2)
		
		for i in range(9):
			for j in range(10):
				co = self.color[j][i]
				if co is not None:
					draw.ellipse((vlines[i+5]-100/2,hlines[j]-100/2)+(vlines[i+5]+100/2,hlines[j]+100/2), fill=co, outline=None, width=1)

		screen = Image.new('RGB',(1920,1200),(0,0,0))
		screen.paste(new_screen,(0,60))

		screen.show()
		return screen

def moveparse(curr_board,last_board):
	rows = 'ABCDEFGHIJ'
	diff = 0
	for i in range(10):
		for j in range(9):
			if curr_board[i][j]!= last_board[i][j]:
				diff += 1
				if curr_board[i][j] == '〇':
					last_pos = (rows[i],j)
				else:
					curr_pos = (rows[i],j)
					name = curr_board[i][j]
				if diff == 2:
					break

	return last_pos[0] + str(last_pos[1]) + '-' + curr_pos[0] + str(curr_pos[1])




	# new_screen.paste(board,((new_screen.size[0]-board.size[0])//2,0),mask=board.convert('L').point(lambda i:0 if i==0 else 255))



if __name__ == '__main__':
	# import fire
	# fire.Fire(ChessBoard)
	b = ChessBoard('x.png')
	print(b)
	print(b.color)

	# c.save('src/cover.png')
	# cover()