from PIL import Image,ImageDraw,ImageFilter,ImageFont
from random import randrange
from pgnparser import txt2board


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



# screen_size = (1080,1920)


# out_box = (64,416,1015,1476)
# screen = Image.open('src/img/test.png')
# out = screen.crop(out_box)
# assert out.size == (951, 1060)

# offset = 50
# board_box = (out_box[0]-offset,out_box[1]-offset,out_box[2]+offset,out_box[3]+offset)
# board = screen.crop(board_box)
# print(board_box)
# # board.show()
# print(board.size)
# assert board.size == (1051, 1160)

# board = Image.open('src/img/brw.png')
# board = board.resize((board.size[0]*1080//board.size[1],1080))
# # board.show()
# print(board.size)

# name_box = (170,1600,170+300,1600+65)
# name = screen.crop(name_box)

# touxiang_box = (11,1559,11+146,1559+146)
# touxiang = screen.crop(touxiang_box).resize((105*2,105*2))
# touxiang_box = (11,1559,11+146,1559+146)
# touxiang = Image.open('xuni.jpg').resize((105*2,105*2))

# opp_name_box = (170,250,170+300,250+65)
# opp_name = screen.crop(opp_name_box)

# opp_touxiang_box = (11,209,11+146,209+146)
# opp_touxiang = screen.crop(opp_touxiang_box).resize((105*2,105*2))
# opp_touxiang = Image.open('optx.png').resize((105*2,105*2))


hetunhui = (57,55,51)


new_screen = Image.new('RGB',(1920,1080),'#5c2223')
# new_screen = Image.open('boadwood.png').filter(ImageFilter.SMOOTH_MORE)

draw = ImageDraw.Draw(new_screen)
hlines =  sorted(list(range(484,0,-105))+list(range(593,1080,105)))
vlines = sorted(list(set(list(range(960,0,-105))+list(range(960,1920,105)))))
v= [0]+vlines[:]
h=[0]+hlines[:]
# for i in v:
# 	for j in h:
# 		draw.rectangle((i,j)+(i+115,j+155),fill=(randrange(100,200),randrange(0,100),randrange(0,100)))


# 参考线
for i in hlines:
	draw.line((vlines[5],i)+(vlines[13],i),fill='white',width=2)

for i in vlines[5:14]:
	draw.line((i,hlines[0])+(i,hlines[4]),fill='white',width=2)

for i in vlines[5:14]:
    draw.line((i,hlines[5])+(i,hlines[-1]),fill='white',width=2)

draw.line((vlines[5],hlines[4])+(vlines[5],hlines[5]),fill='white',width=2)
draw.line((vlines[13],hlines[4])+(vlines[13],hlines[5]),fill='white',width=2)


draw.line((vlines[8],hlines[0])+(vlines[10],hlines[2]),fill='white',width=2)
draw.line((vlines[8],hlines[2])+(vlines[10],hlines[0]),fill='white',width=2)

draw.line((vlines[8],hlines[-1])+(vlines[10],hlines[-3]),fill='white',width=2)
draw.line((vlines[8],hlines[-3])+(vlines[10],hlines[-1]),fill='white',width=2)


# draw.line((vlines[5]-105//2,0)+(vlines[5]-105//2,1080),fill='white',width=1)
# draw.line((vlines[13]+105//2,0)+(vlines[13]+105//2,1080),fill='white',width=1)

# new_screen.paste(board,((new_screen.size[0]-board.size[0])//2,0),mask=board.convert('L').point(lambda i:0 if i==0 else 255))

# tx = circle_corner(touxiang,105)

# new_screen.paste(opp_name,(vlines[1],hlines[2]),mask=opp_name.convert('L').point(lambda i:255 if i>200 else 0))
# new_screen.paste(opp_touxiang,(vlines[2]-105//2,hlines[0]),mask=tx) # 带上mask粘贴，黑色部分不可见
# draw.rounded_rectangle((vlines[2]-105//2,hlines[0])+(vlines[4]-105//2,hlines[2]),radius=105,width=12,outline=(150,60,40))

# new_screen.paste(name,(vlines[1],hlines[-2]),mask=name.convert('L').point(lambda i:255 if i>200 else 0))
# new_screen.paste(touxiang,(vlines[2]-105//2,hlines[-4]),mask=tx)

# draw.rounded_rectangle((vlines[2]-105//2,hlines[-4])+(vlines[4]-105//2,hlines[-2]),radius=105,width=12,outline=(60,60,60))

# use a truetype font
fontsize = 80
font = ImageFont.truetype("src/font/李旭科书法.ttf", fontsize,encoding='gb')
board = [[(v,h) for v in vlines[5:5+9]] for h in hlines[0:10]]
print(board)








s = """
車馬象士将士象馬車
〇〇〇〇〇〇〇〇〇
〇砲〇〇〇〇〇砲〇
卒〇卒〇卒〇卒〇卒
〇〇〇〇〇〇〇〇〇
〇〇〇〇〇〇〇〇〇
兵〇兵〇兵〇兵〇兵
〇炮〇〇〇〇〇炮〇
〇〇〇〇〇〇〇〇〇
车马相仕帅仕相马车
"""
b = txt2board(s)
for i in range(9):
    for j in range(10):
        v,h = board[j][i]
        p = b[j][i]
        if p in '车马相仕帅炮兵':
            color = '#5c2223'
        else:
            color = '#2b1216'
        if p == '車':
            p = '车'
        elif p == '馬':
            p = '马'
        elif p == '砲':
            p = '炮'

        if p != '〇':
            draw.rounded_rectangle((v-100//2,h-100//2)+(v+100//2,h+100//2),radius=50,width=3,fill='#ccccd6')# ,outline=(60,60,60)
            draw.rounded_rectangle((v-90//2,h-90//2)+(v+90//2,h+90//2),radius=45,width=2,outline=color)# ,outline=(60,60,60)

            draw.text((v-fontsize//2,h-fontsize//2), p , font=font,fill=color)


que = Image.open('src/qique.png')
mask = que.convert('L').point(lambda i:0 if i<255 else 255)

new_screen.paste(que,(100,0),mask=mask)

new_screen.show()

# new_screen.save('tmp.png')

# prepare("src/studio_video_1626021676028.mp4", background='tmp.png')