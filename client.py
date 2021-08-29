from mini import Mini, get_pgn
from pgnparser import pgn2gif
from dhtmlxq import MoveTree
from pgnparser import board2pic

# m = Mini('天天象棋')
# count = 8
# get_pgn('src/pgn/%d.pgn'% count)
# pgn2gif('src/pgn/%d.pgn'% count,'src/video/%d.mp4'% count,flip=False,blind=False)


# pgn2gif('src/pgn/%d.pgn'% 7,'src/video/%d.mp4'% 8,flip=False,blind=False)



binit, movelists = parse_tree('md.ubb')
tt = MoveTree(movelists,board=binit)
tt.compress()
for v in tt.video_generator():
    print(v)

