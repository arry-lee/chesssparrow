"""控制小程序窗口"""

from pygetwindow import getWindowsWithTitle
import pyautogui
import time
from PIL import Image
import cv2 as cv
import numpy as np

import os
import pyautogui
from pygetwindow import getWindowsWithTitle

WECHATAPPLAUNCHERPATH = "D:\\Program Files (x86)\\Tencent\\WeChat\\WechatAppLauncher.exe"

class Mini(object):
	"""模拟微信小程序的行为"""
	def __init__(self,title,launch_appid = None):
		self.title = title
		try:
			self.window = getWindowsWithTitle(self.title)[0]
		except:
			self.open(launch_appid)

		while True:
			try:
				self.window = getWindowsWithTitle(self.title)[0]
				break
			except:
				continue

		self.minimize = self.window.minimize
		self.restore = self.window.restore 
		self.close = self.window.close
		self.move = self.window.moveTo
		self.resize = self.window.resizeTo
		self.activate = self.window.activate
		self.original_width = self.window.width
		self.original_height = self.window.height


	@property
	def width(self):
		return self.window.width

	@property
	def height(self):
		return self.window.height

	@property
	def box(self):
		return self.window.box

	def open(self,launch_appid):	
		print('正在启动' + self.title)
		cmd = '"%s" -launch_appid=%s' % (WECHATAPPLAUNCHERPATH,launch_appid)
		os.system(cmd)
		print('启动成功' + self.title)
		self.is_open = True

	def close(self):
		self.window.close()


	def click(self,x,y):
		pyautogui.click(x,y)



def pic2move(image):
	"""通过找○得到步骤"""	
	board_box =(5,160,320,505)
	vlines = "ABCDEFGHI"
	# 模板找图找到落点---------------------------------
	fp = image.crop(board_box)
	to = pyautogui.locate('src/to.png',fp,confidence=0.8)
	tx,ty = (to.left-16)//34,to.top//34
	TO = vlines[tx],str(9-ty)

	
	# 找圆法找到落点---------------------------------
	fp = fp.convert('L')
	binary = fp.point(lambda i: 255 if i>225 else 0)
	binary = np.asarray(binary)
	# 调参
	board_circle = cv.HoughCircles(binary,cv.HOUGH_GRADIENT,1,10,
				 param1=50,param2=8,minRadius=2,maxRadius=5)
	print(board_circle)
	cv.imshow('',binary)
	# cv.waitKey(0)


	circles = np.uint32(np.around(board_circle))

	cs = []
	for index,i in enumerate(circles[0,:]):
		cv.circle(binary,(i[0],i[1]),5*i[2],255,1)
		cs.append((i[2],i[0]//34,i[1]//34))
	assert len(cs) == 1

	FROM = vlines[cs[0][1]],str(9-cs[0][2])
	
	return ''.join(FROM)+'-'+''.join(TO)


def get_pgn(fp):
	b = []
	board_box =(4,158,319,506)
	next_ = (226, 590)
	checkpoint = (230,590)
	a = getWindowsWithTitle('天天象棋')[0]
	a.moveTo(0,0)
	s = pyautogui.screenshot(region=a.box)
	while True:
		if s.getpixel(checkpoint) == (209,206,203):
			pyautogui.click(next_)
			time.sleep(2)
		else:
			break
		s = pyautogui.screenshot(region=a.box)
		b.append(pic2move(s))

	with open(fp,'w') as f:
		for index, step in enumerate(b):
			if index%2==0: 
				f.write(str(index//2+1)+'. ')
			f.write(step+' ')

			if index%2==1:
				f.write('\n')

	return b

if __name__ == '__main__':
	get_pgn('src/pgn/2.pgn')
