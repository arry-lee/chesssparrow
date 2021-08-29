





# import cv2 as cv
# import os.path
# from moviepy.editor import *
# import numpy as np

# from board import ChessBoard


# OUT_BOX = (64,416,1015,1476)
# OFFSET = 50
# BOARD_BOX = (11,365,1069,1531)
# w = BOARD_BOX[2]-BOARD_BOX[0]
# h = BOARD_BOX[3]-BOARD_BOX[1]

# def parse_video(fp):
#     """解析原始视频,得到开始时间和结束时间"""
#     fourcc = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
 
#     out = cv.VideoWriter('tmp.mp4',fourcc, 48, (w,h),True)

#     assert os.path.exists(fp)

#     vc = cv.VideoCapture(fp)
#     fps = vc.get(cv.CAP_PROP_FPS)
#     frame_count = vc.get(cv.CAP_PROP_FRAME_COUNT)

#     print("[INFO] 视频FPS: {}".format(fps))
#     print("[INFO] 视频总帧数: {}".format(frame_count))
#     print("[INFO] 视频时长: {}s".format(frame_count/fps))

#     #############################################
#     x0,y0,x1,y1 = BOARD_BOX
#     start = cv.imread('src/img/tmp_start.png')
#     startbox = (110,1655,180,1690)
#     xs0,ys0,xs1,ys1 = startbox

#     end = cv.imread('src/img/tmp_end.png')
#     endbox = ( 414,939,684,990)
#     xe0,ye0,xe1,ye1 = endbox
#     #############################################

#     i = 0
#     start_pos = None
#     end_pos = None
#     rval = True
#     ended = False
#     # board = []
#     while rval:
#         rval,frame = vc.read()
#         if rval:
#             if start_pos is None:
#                 result = cv.matchTemplate(frame[ys0:ys1,xs0:xs1],start,cv.TM_CCOEFF_NORMED)
#                 _,maxv,_,_ = cv.minMaxLoc(result)
#                 if maxv >= 0.33: # 找相似度最高的模板阈值
#                     start_pos = i
#             else:
#                 if not ended:
#                     # board.append(frame[y0:y1,x0:x1])
#                     result = cv.matchTemplate(frame[ye0:ye1,xe0:xe1],end,cv.TM_CCOEFF_NORMED)
#                     _,maxv,_,_ = cv.minMaxLoc(result)
#                     print(i)
#                     if maxv >= 0.33: # 找相似度最高的模板阈值
#                         end_pos = i
#                         ended = True
#                         last_frame = frame[y0:y1,x0:x1]
#                     # 在此处进行图象处理
#                     else:
#                         out.write(frame[y0:y1,x0:x1]) 
#                 else:
#                     result = cv.matchTemplate(frame[ye0:ye1,xe0:xe1],end,cv.TM_CCOEFF_NORMED)
#                     _,maxv,_,_ = cv.minMaxLoc(result)
#                     if maxv >= 0.33:
#                         continue
#                     else:
#                         last_frame = frame
#                         break
#         i+=1

#     start_time = start_pos/fps
#     end_time = end_pos/fps

#     out.release()
#     return last_frame

# def xqcrop(video, board_box = BOARD_BOX, background = 'src/img/tmp.png'):
#     """ 截取，改变大小，加背景"""

#     width = board_box[2] - board_box[0]
#     height = board_box[3] - board_box[1]
#     width = 1080 * width // height
#     height = 1080

#     vc = VideoFileClip(video).resize((width,height))

#     ic = ImageClip(background).set_duration(vc.duration)

#     cvc = CompositeVideoClip([ic,vc.set_start(0).set_pos('center')])

#     return cvc




# if __name__ == '__main__':

#     f = 'Screenshots-20210715-101105-1080x1920.mp4'
#     last = parse_video(f)
#     cv.imwrite('src/tmpcover.png',last)

#     b = ChessBoard('src/tmpcover.png')
#     print(b)
#     print(b.color)
#     cover = b.get_cover()
#     cover.save('src/cover.png')

#     v = xqcrop('tmp.mp4')

#     v.write_videofile('test1.mp4') # 压缩之后只有1.4Mb，而原始的图片有2.4mb nice