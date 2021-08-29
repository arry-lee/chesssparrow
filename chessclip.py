import cv2 as cv
import os.path


src_path = 'src/video/'
filename = 'studio_video_1626021676028.mp4'
fp = os.path.join(src_path,filename)


out_box = (64,416,1015,1476)

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

def parse_video(fp):
    """解析原始视频"""
    assert os.path.exists(fp)

    vc = cv.VideoCapture(fp)
    fps = vc.get(cv.CAP_PROP_FPS)
    frame_count = vc.get(cv.CAP_PROP_FRAME_COUNT)

    print("[INFO] 视频FPS: {}".format(fps))
    print("[INFO] 视频总帧数: {}".format(frame_count))
    print("[INFO] 视频时长: {}s".format(frame_count/fps))

    offset = 50
    board_box = (out_box[0]-offset,out_box[1]-offset,out_box[2]+offset,out_box[3]+offset)
    x0,y0,x1,y1 = board_box

    start = cv.imread('src/img/start.png')[y0:y1,x0:x1]

    rval = True
    i = 0
    max0 = 0
    maxi = 0
    while rval and i<90:
        rval,frame = vc.read()
        fr = frame[y0-10:y1+10,x0-10:x1+10]
        result = cv.matchTemplate(frame,start,cv.TM_CCOEFF_NORMED)
        _,maxv,_,_ = cv.minMaxLoc(result)
        if maxv >= 0.838: # 找相似度最高的模板阈值
            max0 = maxv
            f = frame[:]
            maxi = i
            print(i,maxv)
            # break
            cv.imshow(str(i),frame)
        i+=1


    print(max0)
    # 初始棋盘的最后一帧
    first_frame = maxi-fps*1 # 初始棋盘的最后一帧
    print(first_frame)
    return first_frame*fps



# print(dir(vc.open))



# 因为每一帧都有差故只能打点

# i = 0
# while rval:
#     rval,frame = vc.read()
#     if i == first_frame+1 or i == first_frame+24:
#         # frame = frame[y0:y1,x0:x1]

#         cv.imshow(str(i),frame)
#         cv.imwrite('src/'+str(i)+'s.png',frame) 

#     if i>first_frame+30:
#         break
#     i+=1

# cv.waitKey(0)    
# cv.destroyAllWindows()

# [30,54] 第O步
# [55,79] 第一步
def frames(vc,first_frame):
    i = 1
    rval = True
    while rval:
        rval,frame = vc.read()
        if rval is True and i>first_frame and (i - first_frame)%24 == 0:
            yield frame
        i+=1

# for i,f in enumerate(frames(vc,first_frame)):
#     cv.imwrite('src/'+str(i)+'s.png',f) 