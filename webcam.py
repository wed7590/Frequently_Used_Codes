import cv2
import threading
import datetime
import time

def image_save0(frame):
    # print('Frame count:', int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    cv2.imwrite(datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + '_image0.jpg', frame)

def image_save1(frame):
    # print('Frame count:', int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
    cv2.imwrite(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+ '_image1.jpg', frame)

def streaming():
    sec_time = 60
    fps = 30

    # 기본이 0번, 만약 비디오가 2개이면 1번 cap이라는 변수에 넣어서 핸들링함.
    cap0 = cv2.VideoCapture(0)
    cap0.set(cv2.CAP_PROP_FRAME_WIDTH, 2590)
    cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, 1940)
    # cap0.set(cv2.CAP_PROP_FPS, framerate)
    cap1 = cv2.VideoCapture(1)
    cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 2590)
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1940)
    # cap0.set(cv2.CAP_PROP_FPS, framerate)
    # 2048 / 1536 까지 지원?

    print('cap0 width : %d, height : %d' % (cap0.get(3), cap0.get(4)))
    print('cap0 FPS : %d' % (cap0.get(cv2.CAP_PROP_FPS)))
    print('cap1 width : %d, height : %d' % (cap1.get(3), cap1.get(4)))
    print('cap1 FPS : %d' % (cap1.get(cv2.CAP_PROP_FPS)))

    start = time.time()
    i = 0

    # 측정 프레임 수
    num_frames = 120
    print("Capturing {0} frames".format(num_frames))

    while(True):
        ret0, frame0 = cap0.read()    # Read 결과와 frame

        # 1ms 동안 키입력 대기
        keycode = cv2.waitKey(1)

        if(ret0) :
            gray = cv2.cvtColor(frame0,  cv2.COLOR_BGR2GRAY)    # 입력 받은 화면 Gray로 변환

            cv2.imshow('frame_color0', frame0)    # 컬러 화면 출력
            
            if i % (sec_time * int(fps)) == 0:
                
                image_save0(frame0)
            
            # cv2.imshow('frame_gray', gray)    # Gray 화면 출력
            if keycode == ord('q'):
                break
    
        ret1, frame1 = cap1.read()    # Read 결과와 frame
        if(ret1) :
            gray = cv2.cvtColor(frame1,  cv2.COLOR_BGR2GRAY)    # 입력 받은 화면 Gray로 변환

            cv2.imshow('frame_color1', frame1)    # 컬러 화면 출력
            if i % (sec_time * int(fps)) == 0:
                
                image_save1(frame1)
        
            # cv2.imshow('frame_gray', gray)    # Gray 화면 출력
            if keycode == ord('q'):
                break
        
        # FPS 측정
        if i % num_frames == 0:
            end = time.time()
            seconds = end - start
            fps = num_frames / seconds
            print("Estimated FPS : {0}".format(fps))

            start = time.time()

        # enter 키 입력시 image save
        if keycode == 13:
            image_save0(frame0)
            image_save1(frame1)
        
        i += 1

    cap0.release()
    cap1.release()
    cv2.destroyAllWindows()

if __name__ == "__main__" :
    streaming()

