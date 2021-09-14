# from mini import Mini, get_pgn
from pgnparser import pgn2gif
# from dhtmlxq import MoveTree
# from pgnparser import board2pic
import os
import glob
base_path = __file__

videos= glob.glob('static/video/*mp4')
count = len(videos)

num = count + 2
print(count)

num = 8
video_path = 'static/video/%d.mp4' % num
pgn_path = 'static/pgn/%d.pgn' % num

# tail_path = os.path.join(video_path,'tail/qique_tail.mp4')

pgn2gif(pgn_path,video_path,flip=False,blind=False,tail=True)

# tail_clip = VideoFileClip(tail_path)

# print(base_path)


# m = Mini('天天象棋')
# count = 8
# # get_pgn('src/pgn/%d.pgn'% count)
# pgn2gif('src/pgn/%d.pgn'% count,'src/video/%d.mp4'% count,flip=False,blind=False)


# pgn2gif('src/pgn/%d.pgn'% 7,'src/video/%d.mp4'% 8,flip=False,blind=False)



# binit, movelists = parse_tree('md.ubb')
# tt = MoveTree(movelists,board=binit)
# tt.compress()
# for v in tt.video_generator():
#     print(v)

