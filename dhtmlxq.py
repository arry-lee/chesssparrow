"""用于解析DHtmlXQ UBB格式文件的工具
"""

import re
from collections import defaultdict
from collections.abc import Iterable
from copy import deepcopy

__author__ = 'arry_lee@qq.com'


PAT_BINIT = re.compile(r'\[DhtmlXQ_binit\](?P<binit>\d{64})\[/DhtmlXQ_binit\]')
PAT_COMMENT = re.compile(r'\[DhtmlXQ_comment(?P<a>\d+)_(?P<b>\d+)\](?P<comment>.*)\[/DhtmlXQ_comment(?P=a)_(?P=b)\]')
PAT_COMMENT0 = re.compile(r'\[DhtmlXQ_comment(?P<a>\d+)\](?P<comment>.*)\[/DhtmlXQ_comment(?P=a)\]')
PAT_MOVE = re.compile(r'\[DhtmlXQ_move_(?P<a>\d+)_(?P<b>\d+)_(?P<c>\d+)\](?P<move>\d+)\[/DhtmlXQ_move_(?P=a)_(?P=b)_(?P=c)\]')
PAT_MOVELIST = re.compile(r'\[DhtmlXQ_movelist\](?P<move>\d+)\[/DhtmlXQ_movelist\]')

def board2txt(board):
    """将二维棋盘数组转化为局面字符串"""
    return '\n'.join(''.join(line) for line in board)

def _move2list(move):
    return list(move[i:i+4] for i in range(len(move)) if i%4==0)

def _binit2board(binit):
    board = [['〇' for i in range(9)] for j in range(10)]
    s = "車馬相仕帅仕相馬車砲砲兵兵兵兵兵车马象士将士象马车炮炮卒卒卒卒卒"
    for i in range(32):
        x = int(binit[2*i+1])
        y = int(binit[2*i])
        if y!=9:
            board[x][y] = s[i]
    return board

def parse_tree(fp):
    """解析ubb文件

    """
    tree = defaultdict(list)
    with open(fp, encoding='utf-8') as f:
        for line in f:
            matched = PAT_MOVE.match(line)
            if matched:
                a = int(matched['a'])
                b = int(matched['b'])
                c = int(matched['c'])
                m = _move2list(matched['move'])
                tree[c] = tree[a][:b-1] + m

            elif PAT_MOVELIST.match(line):
                tree[0] =_move2list(PAT_MOVELIST.match(line)['move'])

            elif PAT_COMMENT0.match(line):
                comment = PAT_COMMENT0.match(line)
                a = int(comment['a'])
                c = comment['comment']
                if a == 0: # 整局评论
                    a = 1
                tree[0][a-1] = (tree[0][a-1],c)

            elif PAT_COMMENT.match(line):
                comment = PAT_COMMENT.match(line)
                a = int(comment['a'])
                b = int(comment['b'])
                c = comment['comment']
                tree[a][b-1] = (tree[a][b-1],c)

            elif PAT_BINIT.match(line):
                binit = PAT_BINIT.match(line)['binit']

    movelists = [x for x in tree.values()]
    return _binit2board(binit), movelists




def parse_move(move,board=None):
    """按照move演变棋盘board,返回该步的信息,包括起始位置，结束位置，是否吃子"""
    fc,fr = int(move[0]), int(move[1])
    tc,tr = int(move[2]), int(move[3])
    if board is not None:
        board[tr][tc] = board[fr][fc]
        board[fr][fc] = '〇'
    return (fc,fr),(tc,tr)




class MoveNode:
    def __init__(self, choices=False,comment=None,board=None,move=None):
        self.next = dict() #包含其他节点
        self.choices = choices # 当前局面的可以走的选项
        self.comment = comment # 当前局面的评论
        self.board = board # 走完这一步的局面
        self.video = [] # 视频片段
        self.move = move # 这一步的内容


    def __str__(self):
        return board2txt(self.board)




class MoveTree(set):
    """ 按前缀树的原理将每一步都视为一个节点，保存走完这一步的局面与评论
    """
    def __init__(self, movelists=None,board=None):
        self.root = MoveNode(board=board)

        if isinstance(movelists,Iterable):
            for movelist in iter(movelists):
                self.insert(movelist)
        else:
            raise TypeError('movelists must be iterable or str')
        self.mark()


    def insert(self,movelist):
        cur = self.root
        for move in movelist:
            if isinstance(move,str):
                move,comment = move, None
            elif isinstance(move,tuple):
                move,comment = move

            if cur.next.get(move,None) is None:
                tmp_board = deepcopy(cur.board)
                parse_move(move,tmp_board)
                cur.next[move] = MoveNode(comment=comment,board=tmp_board,move=move)
            cur = cur.next[move]
        cur.choices = 0



    def mark(self):
        def _mark(root):
            cur = root
            children = cur.next
            cur.choices = list(children.keys())
            for c in cur.next:
                _mark(cur.next[c])
        _mark(self.root)


    def __iter__(self):
        def print_movelists(node, move):
            if len(node.choices)==0:
                yield move
            for key, value in node.next.items():
                yield from print_movelists(value, move + key)
        yield from print_movelists(self.root,'')

    def __len__(self):
        return len([i for i in self])

    def __str__(self):
        return '<MoveTree:' + ' '.join(self) +'>'


    def compress(self):
        def _compress(root):
            # 将没有分支的部分压缩到同一节点,每个节点自带一个视频片段 
            start = cur = root
            tmp = []  
            while True:
                if len(cur.choices) == 1:
                    tmp.append((cur.board,cur.comment,cur.choices,cur.move))

                    key = list(start.next.keys())[0]
                    next_node = list(cur.next.values())[0]

                    if next_node.next:
                        start.next[key] = list(next_node.next.values())[0]              
                    else:
                        start.next = dict()
                    cur = next_node
                        

                elif len(cur.choices) > 1:
                    tmp.append((cur.board,cur.comment,cur.choices,cur.move))
                    start.video = deepcopy(tmp)
                    for key, node in start.next.items():
                        _compress(node)
                    break

                elif len(cur.choices) == 0:
                    tmp.append((cur.board,cur.comment,cur.choices,cur.move))
                    start.video = deepcopy(tmp)
                    break
        _compress(self.root)


    def video_generator(self):
        def helper(node):
            if node.video:
                yield node.video
            for key, value in node.next.items():
                yield from helper(value)  

        yield from helper(self.root)


# if __name__ == '__main__':
#     binit, movelists = parse_tree('md.ubb')
#     tt = MoveTree(movelists,board=binit)
#     tt.compress()

#     for v in tt.video_generator():
#         print(v)

    
