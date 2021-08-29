from moviepy.editor import *
# VideoFileClip,TextClip,CompositeVideoClip,ImageClip
from itertools import zip_longest

__author__ = 'arry_lee'
__doc__ = \
"""实现视频自动化剪辑

1.对局自动播放，固定速度为每秒一步棋，总回合数目为 n
2.分割为 2n 个1s片段
3.分析得每个片段的棋谱，s 如 “红方马8进7[将军(叫杀)]”
4.由棋谱得到当前片段字幕文件,f
5.机器配音,得到配音文件 a
6.将每一段变速和配音相同长度
7.合成，字幕，配音，视频
"""


VIDEO_SIZE = (1080,1920)
BOARD_BOX = (11,365,1069,1531)
SRT_BOX = (10,1558,157,1705)



def crop(video, start_time, end_time=None, board_box = BOARD_BOX, background = 'tmp.png'):
	""" 截取，改变大小，加背景"""
	vc = VideoFileClip(video)

	if not end_time:
		end_time = vc.duration

	width = board_box[2] - board_box[0]
	height = board_box[3] - board_box[1]
	width = 1080 * width // height
	height = 1080

	vc = vc.subclip(start_time,end_time).crop(*board_box).resize(width,height)

	ic = ImageClip(background).set_duration(vc.duration)

	cvc = CompositeVideoClip([ic,vc.set_start(0).set_pos('center')])

	return cvc




def prepare(video_path,background,seconds=1):
	""" 预处理
	裁剪加分段
	seconds 每段时长单位s
	"""
	vc = VideoFileClip(video_path).crop(*BOARD_BOX).resize(((1069-11)*1080//(1531-365),1080))
	n = int(vc.duration//seconds)
	ic = ImageClip(background).set_duration(vc.duration)
	cvc = CompositeVideoClip([ic,vc.set_start(0).set_pos('center')])

	vlist = [cvc.subclip(i,i+seconds) for i in range(n)]
	return vlist

def get_frame(vlist):
	for i,v in enumerate(vlist):
		v.save_frame('src/frame%d.png'%(i,))

def add_text(str_, video_clip, pos=SRT_BOX,seconds=1):
	"""
	单个片段加字幕
	"""
	if str_ is None or str_ == '':
		return video_clip

	fontsize = pos[3]-pos[1]

	text_clip = TextClip(str_, fontsize = fontsize, color='white', font="SimHei")
	text_clip = text_clip.set_duration(seconds).set_pos('center')
	video_clip = CompositeVideoClip([video_clip,text_clip])
	return video_clip


def get_txt(srt):
	# 返回字幕列表
	with open(srt,'r',encoding='utf-8') as f:
		return list(l.strip() for l in f )


def finalclip(vlist,slist):
	# 加完字幕再组合
	fl = [add_text(s,v) for s,v in zip_longest(slist,vlist)]
	fc = concatenate_videoclips(fl)
	return fc

def main():
	vlist = prepare("VID_20210712001606.mp4", background='tmp.png')
	# get_frame(vlist)
	slist = get_txt("example.txt")
	fc = finalclip(vlist,slist)
	fc.write_videofile('new.mp4')

if __name__ == '__main__':
	main()


