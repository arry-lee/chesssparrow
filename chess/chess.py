class Chess():
    """
    棋子的基类
    """

    def __init__(self, x, y, red=True, selected=False):
        #棋子是否选中
        self.selected = selected 
        # 黑方或者红方,红方为True
        self.red = red
        self.x = x
        self.y = y
        # 是否在自己的地盘
        self.bool_myplace = self.is_myplace(self.y)
        
        self.name = '棋'

   
    #棋子的图片
    def picture(self):
        if self.red:
            return '红'+self.name + '.png'
        else:
            return '黑'+self.name + '.png'

    # 楚河汉界,判断是否在自己地盘
    # 在返回 True
    def is_myplace(self, y):
        if self.red and y > 4:
            return True
        elif not self.red and y < 5:
            return True
        return False

    # 返回棋子的颜色
    def is_red(self):
        red = self.red
        return red

    #返回棋子的位置==列表的索引
    def position(self):
        pos = (self.x,self.y)
        #返回元组
        return pos

    # 设置棋子位置
    def set_position(self, pos):
        self.x, self.y = pos

    # 棋子移动
    def move(self, start_position, end_position, chessboard):
        # 棋子能否移动
        # 更新棋子状态
        if self.can_move(start_position, end_position, chessboard):
            # 棋子位置,选中,是否在自己的地盘
            self.x = end_position[0]
            self.y = end_position[1]
            self.selected = False
            self.bool_myplace = self.is_myplace(self.x)
            # 先不更新chessboard,因为这是棋子,不要加进棋盘
            return True
        return False
            

    #棋子的走法及相应的规则
    # dx, dy为相对于之前位置的位移量
    def rule(self, dx, dy):
        return False

    #棋子是否能够移动到相应位置
    # chessboard是棋盘的数组
    # position为元组,chessboard为列表
    def can_move(self, start_position, end_position, chessboard):
        # 先调用rule看看能不能这么走,不能直接返回false
        # 判断落点有无棋子,是否己方,能否吃子
        # 判断能否到达落点
        #能移动则返回True
        return True

    # 判断落点有无棋子
    # 有返回True
    def position_has_chess(self, position, chessboard):
        ax = position[0]
        ay = position[1]

        if chessboard[ax][ay] == 0:
            # 对应点无棋子
            return False
        return True

    # 判断棋子是否是己方的
    # 是则返回True
    # red 己方棋子的颜色
    # chess 要判断的棋子对象
    # 是同一方的棋子返回True
    def chess_is_my(self, red, chess):
        black = chess.is_red()
        
        if red == black:
            # 棋子颜色相同,是己方的棋子
            return True
        return False

    # 能否移动到落点
    def move_position(self, start_position, end_position, chessboard):
        return False

    # 计算起点和终点直线之间的棋子,只适用于炮和車
    def count_chess(self, start_position, end_position ,chessboard):
        x = start_position[0]
        y = start_position[1]
        ex = end_position[0]
        ey = end_position[1]

        dx = end_position[0] - x
        dy = end_position[1] - y

        # 方向
        sx = dx/abs(dx) if dx != 0 else 0
        sy = dy/abs(dy) if dy != 0 else 0
        
        num = 0
        while x != ex or y != ey:
            x += sx
            y += sy
            x = int(x)
            y = int(y)
            if not chessboard[x][y] == 0:
                num += 1
        return num




            

class Bing(Chess):
    # 如果使用父类的构造函数,这里会自动调用不需要重写
    def __init__(self, x, y, red=True, selected=False):
        super().__init__(x, y, red, selected)
        self.name = '兵' if self.red else '卒'


    # 兵的规则要改一下,要考虑上下两方的坐标
    # 改了一下不知道对不对
    def rule(self, dx, dy):
        # 把它想成坐标系
        if not abs(dx) + abs(dy) == 1:
            return False

        # self.bool_myplace = self.is_myplace(self.y)
        # 判断兵是否到达对面
        if self.bool_myplace:
            # 未到
            if self.red and dy == -1:
                return True
            if not self.red and dy == 1:
                return True
            return False
        else:
            if self.red and dy == 1:
                return False
            if not self.red and dy == -1:
                return False
            return True
         
    def can_move(self, start_position, end_position, chessboard):
        x,y = end_position
        dx = end_position[0] - start_position[0]
        dy = end_position[1] - start_position[1]
        if self.rule(dx, dy):
            if not self.position_has_chess(end_position, chessboard):
                return True
            else:
                # 是否本方棋子
                if self.chess_is_my(self.red, chessboard[x][y]):
                    return False
                else:
                    # 吃子
                    return True
        else:
            return False

    # 检查是否越界,越界则返回False
    def checkp(self, pos):
        x,y = pos
        if x < 0 or y < 0 or x > 8 or y > 9:
            return False
        return True
    # 返回棋子能够移动的所有位置
    # position 棋子位置, chessboard棋盘二维列表
    # 返回列表,列表元素为元组
    def try_move(self, position, chessboard):
        pass
        x,y = position
        a = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        b = []

        for i in a:
            if not self.checkp(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        
        return b


class Ma(Chess):
    # 如果使用父类的构造函数,这里会自动调用不需要重写
    def __init__(self, x, y, red=True, selected=False):
        super().__init__(x, y, red, selected)
        self.name = '马'


    def rule(self, dx, dy):
        if dx == 0 or dy == 0:
            return False
        if abs(dx) + abs(dy) == 3:
            return True
         
    def can_move(self, start_position, end_position, chessboard):
        dx = end_position[0] - start_position[0]
        dy = end_position[1] - start_position[1]
        x = end_position[0]
        y = end_position[1]
        if self.rule(dx, dy):
            # 移动
            if not self.position_has_chess(end_position, chessboard):
                if self.mati(start_position, dx, dy, chessboard):
                    return False
                return True
            else:
                # 吃子
                # 是否本方棋子
                if self.chess_is_my(self.red, chessboard[x][y]):
                    return False
                else:
                    # 吃子
                    if self.mati(start_position, dx, dy, chessboard):
                        return False
                    return True
        else:
            return False
    # 是否绊马蹄
    # 是 返回 True
    def mati(self, start_position, dx, dy, chessboard):
        x,y = start_position
        if abs(dx) == 1:
            y = y + dy/2
            y = int(y)
            if chessboard[x][y] == 0:
                return False
            else:
                return True
        if abs(dy) == 1:
            x = x + dx/2
            x = int(x)
            if chessboard[x][y] == 0:
                return False
            else:
                return True

    # 检查是否越界,越界则返回False
    def checkp(self, pos):
        x,y = pos
        if x < 0 or y < 0 or x > 8 or y > 9:
            return False
        return True
    # 返回棋子能够移动的所有位置
    # position 棋子位置, chessboard棋盘二维列表
    # 返回列表,列表元素为元组
    def try_move(self, position, chessboard):
        x,y = position
        a = [(x+1,y+2),(x+2,y+1),(x-1,y+2),(x-2,y+1),
                (x-1,y-2),(x-2,y-1),(x+1,y-2),(x+2,y-1)
            ]
        b = []

        for i in a:
            if not self.checkp(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b


class Pao(Chess):
    # 如果使用父类的构造函数,这里会自动调用不需要重写
    def __init__(self, x, y, red=True, selected=False):
        super().__init__(x, y, red, selected)
        self.name = '炮'


    def rule(self, dx, dy):
        if not (dx == 0 and dy == 0):
            if dx == 0 or dy == 0:
                return True
        return False
         
    def can_move(self, start_position, end_position, chessboard):
        dx = end_position[0] - start_position[0]
        dy = end_position[1] - start_position[1]
        x = end_position[0]
        y = end_position[1]
        if self.rule(dx, dy):
            # 炮移动
            num = self.count_chess(start_position, end_position, chessboard)
            if not num:
                return True
            # 炮吃子
            if num == 2 and self.position_has_chess(end_position, chessboard):
                if not self.chess_is_my(self.red, chessboard[x][y]):
                    return True
            return False

        else:
            return False

    # 检查是否越界,越界则返回False
    def checkp(self, pos):
        x,y = pos
        if x < 0 or y < 0 or x > 8 or y > 9:
            return False
        return True
    # 返回棋子能够移动的所有位置
    # position 棋子位置, chessboard棋盘二维列表
    # 返回列表,列表元素为元组
    def try_move(self, position, chessboard):
        x,y = position
        a = [(x+1,y),(x+2,y),(x+3,y),(x+4,y),(x+5,y),(x+6,y),(x+7,y),(x+8,y),
                (x-1,y),(x-2,y),(x-3,y),(x-4,y),(x-5,y),(x-6,y),(x-7,y),(x-8,y),
                (x,y+1),(x,y+2),(x,y+3),(x,y+4),(x,y+5),(x,y+6),(x,y+7),(x,y+8),(x,y+9),
                (x,y-1),(x,y-2),(x,y-3),(x,y-4),(x,y-5),(x,y-6),(x,y-7),(x,y-8),(x,y-9)
            ]
        b = []

        for i in a:
            if not self.checkp(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b

class Shi(Chess):
    # 如果使用父类的构造函数,这里会自动调用不需要重写
    def __init__(self, x, y, red=True, selected=False):
        super().__init__(x, y, red, selected)
        self.name = '仕' if self.red else '士'

    def rule(self, dx, dy):
        if abs(dx) == 1 and abs(dy) == 1:
            return True
        return False
 
    def can_move(self, start_position, end_position, chessboard):
        dx = end_position[0] - start_position[0]
        dy = end_position[1] - start_position[1]
        x, y = end_position
        if self.rule(dx, dy):
            # 移动
            if not self.position_has_chess(end_position, chessboard):
                if not self.is_out_range(x, y):
                    return False
                return True
            else:
                # 吃子
                # 是否本方棋子
                if self.chess_is_my(self.red, chessboard[x][y]):
                    return False
                else:
                    # 吃子
                    if not self.is_out_range(x, y):
                        return False
                    return True
        else:
            return False

    # 判断是否过界
    # 过界 返回 False
    def is_out_range(self, x, y):
        if self.red and 2 < x < 6 and 6 < y < 10:
            return True
        if not self.red and 2 < x < 6 and -1 < y < 3:
            return True
        return False


    # 检查是否越界,越界则返回False
    def checkp(self, pos):
        x,y = pos
        if x < 0 or y < 0 or x > 8 or y > 9:
            return False
        return True
    # 返回棋子能够移动的所有位置
    # position 棋子位置, chessboard棋盘二维列表
    # 返回列表,列表元素为元组
    def try_move(self, position, chessboard):
        x,y = position
        a = [(x+1,y+1),(x-1,y+1),(x-1,y-1),(x+1,y-1)]
        b = []

        for i in a:
            if not self.checkp(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b


class Xiang(Chess): # 如果使用父类的构造函数,这里会自动调用不需要重写
    def __init__(self, x, y, red=True, selected=False):
        super().__init__(x, y, red, selected)
        self.name = '相' if self.red else '象'


    def rule(self, dx, dy):
        if abs(dx) == 2 and abs(dy) == 2:
            return True
        return False
 
    def can_move(self, start_position, end_position, chessboard):
        x, y = end_position
        dx = end_position[0] - start_position[0]
        dy = end_position[1] - start_position[1]
        if self.rule(dx, dy):
            # 移动
            if not self.position_has_chess(end_position, chessboard):
                if self.xiangti(start_position, dx, dy, chessboard):
                    return False
                if not self.is_out_range(y):
                    return False
                return True
            else:
                # 吃子
                # 是否本方棋子
                if self.chess_is_my(self.red, chessboard[x][y]):
                    return False
                else:
                    # 吃子
                    if self.xiangti(start_position, dx, dy, chessboard):
                        return False
                    if not self.is_out_range(y):
                        return False
                    return True
        else:
            return False
    # 是否绊象蹄
    # 是 返回 True
    def xiangti(self, start_position, dx, dy, chessboard):
        x, y = start_position
        x += dx/2
        y += dy/2
        x = int(x)
        y = int(y)
        if chessboard[x][y] == 0:
            return False
        return True

    # 判断是否过界
    # 过界 返回 False
    def is_out_range(self, y):
        if self.red and y < 5:
            # out range
            return False
        if not self.red and y > 4:
            return False
        return True

    # 检查是否越界,越界则返回False
    def checkp(self, pos):
        x,y = pos
        if x < 0 or y < 0 or x > 8 or y > 9:
            return False
        return True
    # 返回棋子能够移动的所有位置
    # position 棋子位置, chessboard棋盘二维列表
    # 返回列表,列表元素为元组
    def try_move(self, position, chessboard):
        x,y = position
        a = [(x+2,y+2),(x-2,y+2),(x-2,y-2),(x+2,y-2)]
        b = []

        for i in a:
            if not self.checkp(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b


class Shuai(Chess):
    # 如果使用父类的构造函数,这里会自动调用不需要重写
    def __init__(self, x, y, red=True, selected=False):
        super().__init__(x, y, red, selected)
        self.name = '帅' if self.red else '将'


    def rule(self, dx, dy):
        if abs(dx) + abs(dy) == 1:
            return True
        return False
 
    def can_move(self, start_position, end_position, chessboard):
        dx = end_position[0] - start_position[0]
        dy = end_position[1] - start_position[1]
        x, y = end_position
        if self.rule(dx, dy):
            # 移动
            if not self.position_has_chess(end_position, chessboard):
                if not self.is_out_range(x, y):
                    return False
                return True
            else:
                # 吃子
                # 是否本方棋子
                if self.chess_is_my(self.red, chessboard[x][y]):
                    return False
                else:
                    # 吃子
                    if not self.is_out_range(x, y):
                        return False
                    return True
        else:
            return False

    # 判断是否过界
    # 过界 返回 False
    def is_out_range(self, x, y):
        if self.red and 2 < x < 6 and 6 < y < 10:
            return True
        if not self.red and 2 < x < 6 and -1 < y < 3:
            return True
        return False


    # 检查是否越界,越界则返回False
    def checkp(self, pos):
        x,y = pos
        if x < 0 or y < 0 or x > 8 or y > 9:
            return False
        return True
    # 返回棋子能够移动的所有位置
    # position 棋子位置, chessboard棋盘二维列表
    # 返回列表,列表元素为元组
    def try_move(self, position, chessboard):
        x,y = position
        a = [(x+1,y),(x-1,y),(x,y-1),(x,y+1)]
        b = []

        for i in a:
            if not self.checkp(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b


class Che(Chess):
    # 如果使用父类的构造函数,这里会自动调用不需要重写
    def __init__(self, x, y, red=True, selected=False):
        super().__init__(x, y, red, selected)
        self.name = '车'

    def rule(self, dx, dy):
        if not (dx == 0 and dy == 0):
            if dx == 0 or dy == 0:
                return True
        return False
         
    def can_move(self, start_position, end_position, chessboard):
        dx = end_position[0] - start_position[0]
        dy = end_position[1] - start_position[1]
        x = end_position[0]
        y = end_position[1]
        if self.rule(dx, dy):
            # 移动
            num = self.count_chess(start_position, end_position, chessboard)
            if not num:
                return True
            # 吃子
            if num == 1 and self.position_has_chess(end_position, chessboard):
                if not self.chess_is_my(self.red, chessboard[x][y]):
                    return True
            return False
        else:
            return False

    # 检查是否越界,越界则返回False
    def checkp(self, pos):
        x,y = pos
        if x < 0 or y < 0 or x > 8 or y > 9:
            return False
        return True
    # 返回棋子能够移动的所有位置
    # position 棋子位置, chessboard棋盘二维列表
    # 返回列表,列表元素为元组
    def try_move(self, position, chessboard):
        x,y = position
        a = [(x+1,y),(x+2,y),(x+3,y),(x+4,y),(x+5,y),(x+6,y),(x+7,y),(x+8,y),
                (x-1,y),(x-2,y),(x-3,y),(x-4,y),(x-5,y),(x-6,y),(x-7,y),(x-8,y),
                (x,y+1),(x,y+2),(x,y+3),(x,y+4),(x,y+5),(x,y+6),(x,y+7),(x,y+8),(x,y+9),
                (x,y-1),(x,y-2),(x,y-3),(x,y-4),(x,y-5),(x,y-6),(x,y-7),(x,y-8),(x,y-9)
            ]
        b = []

        for i in a:
            if not self.checkp(i):
                continue
            if self.can_move(position, i, chessboard):
                b.append(i)
        return b
