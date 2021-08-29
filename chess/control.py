import json

from chess import *

class Chessboard():

    def __init__(self):
        # 初始化
        board = [0] * 9
        for i in range(9):
            board[i] = [0] * 10
        self.chessboard = board
        # 初始化棋盘
        # 黑棋
        # x为横坐标,y为纵坐标,图像的左上角为坐标原点
        self.chessboard[0][3] = Bing(0, 3, red = False) 
        self.chessboard[2][3] = Bing(2, 3, red = False) 
        self.chessboard[4][3] = Bing(4, 3, red = False) 
        self.chessboard[6][3] = Bing(6, 3, red = False) 
        self.chessboard[8][3] = Bing(8, 3, red = False) 
        self.chessboard[1][2] = Pao(1, 2, red = False) 
        self.chessboard[7][2] = Pao(7, 2, red = False) 
        self.chessboard[0][0] = Che(0, 0, red = False) 
        self.chessboard[8][0] = Che(8, 0, red = False) 
        self.chessboard[1][0] = Ma(1, 0, red = False) 
        self.chessboard[7][0] = Ma(7, 0, red = False) 
        self.chessboard[2][0] = Xiang(2, 0, red = False) 
        self.chessboard[6][0] = Xiang(6, 0, red = False) 
        self.chessboard[3][0] = Shi(3, 0, red = False) 
        self.chessboard[5][0] = Shi(5, 0, red = False) 
        self.chessboard[4][0] = Shuai(4, 0, red = False) 

        # 红棋
        self.chessboard[0][6] = Bing(0, 6) 
        self.chessboard[2][6] = Bing(2, 6) 
        self.chessboard[4][6] = Bing(4, 6) 
        self.chessboard[6][6] = Bing(6, 6) 
        self.chessboard[8][6] = Bing(8, 6) 
        self.chessboard[1][7] = Pao(1, 7) 
        self.chessboard[7][7] = Pao(7, 7) 
        self.chessboard[0][9] = Che(0, 9) 
        self.chessboard[8][9] = Che(8, 9) 
        self.chessboard[1][9] = Ma(1, 9) 
        self.chessboard[7][9] = Ma(7, 9) 
        self.chessboard[2][9] = Xiang(2, 9) 
        self.chessboard[6][9] = Xiang(6, 9) 
        self.chessboard[3][9] = Shi(3, 9) 
        self.chessboard[5][9] = Shi(5, 9) 
        self.chessboard[4][9] = Shuai(4, 9) 

        self.red_move = True
        self.black_move = False

        # 将军的标志
        self.jiangjun = False
        # 记录走子
        self.memory = []

    # 判断坐标是否合法
    def check(self, position):
        x,y = position
        if x < 0 or y < 0:
            return False
        if x > 8 or y > 9:
            return False
        return True

    def move(self, start_position, end_position):
        
        x,y = start_position
        ex,ey = end_position


        if not self.check(start_position):
            return False
        if not self.check(end_position):
            return False

        # 要走的位置没棋子
        if self.chessboard[x][y] == 0:
            return False

        if self.chessboard[x][y].move(start_position, 
                                        end_position, self.chessboard):
            # 添加走棋规则,一人一步,红方先走
            # 一开始我把它放在上边,结果没判断它能不能移动就更改状态了
            if self.red_move and not self.chessboard[x][y].red:
                return False 
            if self.black_move and self.chessboard[x][y].red:
                return False 
            self.red_move = not self.red_move
            self.black_move = not self.black_move

            temp = self.chessboard[x][y]
            tempe = self.chessboard[ex][ey]
            self.chessboard[ex][ey] = self.chessboard[x][y]
            self.chessboard[x][y] = 0

            # 添加判断,走棋方走棋后是否被将军,是则不能走棋,回滚
            if self.is_jiang(temp.red, self.chessboard):
                self.chessboard[x][y] = temp
                self.chessboard[ex][ey] = tempe
                self.red_move = not self.red_move
                self.black_move = not self.black_move
                print('被将军')
                return False
                
            # 添加判断,走棋方走棋后是否将对面军,是则更改将军标志
            if self.is_jiang((not temp.red), self.chessboard):
                self.jiangjun = True
                print('将军')

            # 如果将军标志为真判断输赢
            if self.jiangjun:
                pass
                if self.is_win((not temp.red) , self.chessboard):
                    pass
                    self.jiangjun = False
                    print('应将成功')
                else:
                    print('yingle')
                    print(temp.red)
        else:
            return False
            
        # 保存走子
        self.history(start_position,end_position)
        return True

    def set_selected(self, position):
        x,y = position
        self.chessboard[x][y].set_selected(True)
    def rm_selected(self, position):
        x,y = position
        self.chessboard[x][y].set_selected(False)

    # 判断死棋
    # 判断胜利
    # red 为应将方
    # 应该成功返回True
    def is_win(self, red, chessboard):
        pass
        # 没有想到好方法,只能遍历己方所有棋子的所有走法,看能否应将
        # 存储己方所有棋子
        chesses = []
        # 应将成功标志
        yy = False

        for i in chessboard:
            for y in i:
                if y == 0: continue
                if y.red == red: chesses.append(y)

        for i in chesses:
            # 所有的走法
            a = []
            a = i.try_move(i.position(), chessboard)
            for y in a:
                if i.can_move(i.position(), y, chessboard):
                    pass
                    a,b = i.position()
                    ea, eb = y

                    temp = chessboard[a][b]
                    tempe = chessboard[ea][eb]

                    # 改变棋子的位置属性,棋盘中棋子位置
                    i.set_position(y)
                    chessboard[ea][eb] = temp
                    chessboard[a][b] = 0
        
                    if not self.is_jiang(red, chessboard):
                        yy = True
                        # 应将成功

                    # 回滚
                    i.set_position((a,b))
                    chessboard[a][b] = temp
                    chessboard[ea][eb] = tempe
                    # if yy: break
        return yy
                
                    

    # 判断将军,这里注意,每一步走棋都可能会将军,无论是本方还是对方
    # 本方走棋可能导致本方被将军,所以也要判断一下
    # red 为要测试是否被将军的那一方
    # chessboard 为棋盘
    # 被将军返回True
    def is_jiang(self, red, chessboard):
        pass
        # 只需要判断走棋后,本方棋子下一步能不能走到对方将的位置
        # 将两个位置输入到对应棋子的move函数判断
        # 也可以判断将中心的三个点是不是兵,将周围的马位是否有马等

        # 我要判断将的三个位置,然后遍历对方的马,炮,車
        a = []
        b = []
        for i in chessboard:
            for y in i:
                pass
                if y == 0: continue
                if y.name == '帅' or y.name == '将' and y.red == red:
                    a.append(y)
                    continue
                if y.name == '炮' and y.red == (not red):
                    b.append(y)
                    continue
                if y.name == '马' and y.red == (not red):
                    b.append(y)
                    continue
                if y.name == '車' and y.red == (not red):
                    b.append(y)
                    continue
        pass
        x,y = a[0].position()
        if self.check((x,y+1)) and not chessboard[x][y+1] == 0:
            if chessboard[x][y+1].can_move((x,y+1), (x,y), chessboard):
                return True
        if self.check((x,y-1)) and not chessboard[x][y-1] == 0:
            if chessboard[x][y-1].can_move((x,y-1), (x,y), chessboard):
                return True
        if self.check((x+1,y)) and not chessboard[x+1][y] == 0:
            if chessboard[x+1][y].can_move((x+1,y), (x,y), chessboard):
                return True
        if self.check((x-1,y)) and not chessboard[x-1][y] == 0:
            if chessboard[x-1][y].can_move((x-1,y), (x,y), chessboard):
                return True
        
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        for i in b:
            # 这里一开始调用的move,
            # 结果将棋子自身属性位置改变成了对方将的位置
            # 但是棋子在棋盘上的位置没变,所以移动吃子没有问题
            # 所以第一次正常,之后的就都有问题了
            print(i.position(), i.name)
            if i.can_move(i.position(), (x,y), chessboard): 
                return True

        return False

    # 保存历史记录用来悔棋
    def history(self,start_position, end_position):
        pass
        # 保存移动前的位置
        # 移动后的位置
        # 如果移动后的位置有棋子,保存棋子
        # 可选保存棋子名称

        # 以上所有保存在元组中,所有元组保存在列表中
        # [(x,y),(x,y)]
        c = []
        c.append(start_position)
        c.append(end_position)
        self.memory.append(c)
       
    # 保存记录
    def save(self):
        with open('memory','w') as f:
            json.dump(self.memory, f)
        

    # 重新开始游戏
    def restart_chess(self):
        pass

    # 设置对弈模式,人人,人机,AI会有的
    def setting_mode(self):
        pass
