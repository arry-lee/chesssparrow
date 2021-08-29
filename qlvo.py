from mini import Mini
import pyautogui
import time

a = Mini('天天象棋')
a.move(0,0)

# print(pyautogui.position())
# a.click(29,593)

while True:
	h = pyautogui.screenshot(region=(0,0, a.width, a.height//2))
	x = pyautogui.locate('src/qiangzuo.png',h,confidence=0.8)
	print(x)
	if x:
		pyautogui.click(x.left+x.width//2,x.top+x.height//2)
		time.sleep(0.5)
		pyautogui.click(111,402) # 确认,抢座
		break