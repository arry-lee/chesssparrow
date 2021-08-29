import os

import pygame
from pygame.locals import *

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)


main_dir = os.path.split(os.path.abspath(__file__))[0]
# 资源文件路径
data_dir = os.path.join(main_dir, 'source')

def load_image(name):
    "loads an image, prepares it for play"
    filename = os.path.join(data_dir, name)
    try:
        surface = pygame.image.load(filename)
        # print(surface)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(filename, pygame.get_error()))
    # surface = pygame.transform.scale(surface, (int(surface.get_rect()[2]*0.9), int(surface.get_rect()[3]*0.9)))
    print(surface.get_rect())
    return surface.convert_alpha(), surface.get_rect()


size = (1280,720)
screen_w, screen_h = 1280,720
half_w, half_h = 640,360

p = 70
mp = 109*720//1080
print(mp)

print(p)
hs =  sorted(list(range(half_h-mp//2,0,-p))+list(range(half_h+mp//2,720,p)))
ws = sorted(list(set(list(range(1280//2,0,-p))+list(range(1280//2,1280,p)))))


pygame.init()
screen = pygame.display.set_mode((1280,720))
screen.fill((118,37,47))
background, _ = load_image('bg.png')
screen.blit(background, (0, 0))


pygame.draw.aaline(screen, GREEN, [0, 0], size, 1)
pygame.draw.aaline(screen,GREEN, (screen_w,0), (0,screen_h), 1)





for h in hs:
	pygame.draw.aaline(screen, GREEN,(0,h), (screen_w,h), 1)

for w in ws:
	pygame.draw.aaline(screen, GREEN,(w,0), (w,screen_h), 1)


pygame.draw.rect(screen,WHITE,[ws[5],hs[0],ws[13]-ws[5],hs[-1]-hs[0]],width=1)

pygame.draw.rect(screen,WHITE,[ws[5]-15,hs[0]-15,ws[13]-ws[5]+30,hs[-1]-hs[0]+30],width=4)


for i in hs:
    pygame.draw.line(screen,WHITE,(ws[5],i),(ws[13],i),width=3)

for i in ws[5:14]:
    pygame.draw.line(screen,WHITE,(i,hs[0]),(i,hs[4]),width=3)

for i in ws[5:14]:
    pygame.draw.line(screen,WHITE,(i,hs[5]),(i,hs[-1]),width=3)


pygame.draw.line(screen,WHITE,(ws[5],hs[4]),(ws[5],hs[5]),width=3)
pygame.draw.line(screen,WHITE,(ws[13],hs[4]),(ws[13],hs[5]),width=3)

pygame.draw.line(screen,WHITE,(ws[8],hs[0]),(ws[10],hs[2]),width=2)
pygame.draw.line(screen,WHITE,(ws[8],hs[2]),(ws[10],hs[0]),width=2)

pygame.draw.line(screen,WHITE,(ws[8],hs[-1]),(ws[10],hs[-3]),width=2)
pygame.draw.line(screen,WHITE,(ws[8],hs[-3]),(ws[10],hs[-1]),width=2)







pygame.display.set_caption('棋雀象棋')

try:
    while 1:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.unicode == "q":
                break
        pygame.display.flip()
finally:
    pygame.quit()