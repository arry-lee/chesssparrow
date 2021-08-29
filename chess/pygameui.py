import pygame
from pygame.locals import *

class MyControl(object):
    def __init__(self, rect, img_file, img_cx, text, font_info):
        self.status = 0
        self.rect = rect
        self.img_cx = img_cx
        self.text = text
        self.font_info = font_info

        # 设定底图，每一种 status 一张。
        if img_file is None:
            self.__img = None
            self.img_width = 0
        else:
            self.__img = pygame.image.load(img_file)
            self.__image = []

            img_rect = self.__img.get_rect()
            width = int(img_rect.width / img_cx)

            x = 0
            for i in range(self.img_cx):
                self.__image.append(self.__img.subsurface((x, 0), (width, img_rect.height)))
                x += width

            self.img_width = width

        # 设定 Lable 对象
        if text == "":
            self.label = None
        else:
            self.label = Label(rect.left, rect.top, text, font_info)

    def render(self, surface):
        if self.status >= 0:
            if self.__img is not None:
                if self.status < self.img_cx:
                    surface.blit(self.__image[self.status], (self.rect.left, self.rect.top))

            if self.label is not None:
                self.label.render(surface)

    def is_over(self, point):
        if self.status <= 0:
            bflag = False      # disabled
        else:
            bflag = self.rect.collidepoint(point)

        return bflag

    def check_click(self, event):
        if event.type == MOUSEBUTTONDOWN:
            return self.is_over(event.pos)
            
    def hide(self):
        self.status = -1

    def disabled(self):
        self.status = 0

    def enabled(self):
        self.status = 1


class Button(MyControl):
    def __init__(self, btn_name, event_id, rect, img_file, img_cx, text="", font_info=None):
        MyControl.__init__(self, rect, img_file, img_cx, text, font_info)

        self.event_id = event_id
        self.name = btn_name

        # 调整文字的位置为居中
        if self.label is not None:
            x = rect.left + int(rect.width / 2)
            y = rect.top + int(rect.height / 2)
            self.label.set_pos(x, y, 1, 1)

        self.status = 1

    def set_text(self, text):
        self.label.set_text(text)

    def update(self, event):
        if self.check_click(event):
            data = {"from_ui": self.name, "status":self.status}
            ev = pygame.event.Event(self.event_id, data)
            pygame.event.post(ev)

