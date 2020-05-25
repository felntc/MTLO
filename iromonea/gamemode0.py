import matplotlib 
matplotlib.use('tkagg') 
from statistics import mode
import time
import cv2
import os
import time
import websocket
import json
from keras.models import load_model
import numpy as np
import pygame
from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input
import PySimpleGUI as sg
import iromonea
import sys

def game(cam,window00):
#  セクション1 - オプションの設定と標準レイアウト
    
    sg.theme('Dark Blue 3')
    pygame.mixer.init()
    players=list(range(1,11))
    time0=list(range(0,61))

    frame1 = sg.Frame("いじらなくてもOK",[[sg.Text('感度', size=(15, 1), ),sg.Spin(players, size=(7, 1),initial_value=5
                                                                     ,key='-sensitive-'),
                               sg.Text('低いほど敏感', size=(15, 1), )],
                         [sg.Text('ライフ', size=(15, 1)),sg.Spin(players, size=(7, 1),initial_value=1
                                                              ,key='-life-'),
                          sg.Text('何回笑っていいか', size=(20, 1))],
                               [sg.Text('忖度レベル', size=(15, 1), ),sg.Spin(players, size=(7, 1),initial_value=1
                                                                     ,key='-sontaku-'),
                               sg.Text('接待用', size=(15, 1), )],
                                   [sg.Text('FPS', size=(15, 1), ),sg.Spin(time0, size=(7, 1),initial_value=20
                                                                     ,key='-fps-'),
                               sg.Text('重い時は下げよう', size=(15, 1), )]
                         ])

    layout0=[
    [sg.Text('入室を二回押して始める')],
    [sg.Text('nicknameを入力'),sg.InputText(default_text='hoge', key='-name-', size=(20, 5))],
    [sg.Text('部屋IDを入力'),sg.InputText(default_text='A', key='-room-', size=(20, 5))],
    [sg.Text('プレイ人数を入力'),sg.Spin(players, size=(7, 7),initial_value=6,key='-player-') ],
    [sg.Text('パスワードを入力'),sg.InputText(default_text='hoge', key='-pass-', size=(20, 5))],
    [sg.Spin(players, size=(7, 7),initial_value=3,key='-clear-'),sg.Text('クリア条件を設定')],
     [sg.Radio('ホスト', "RADIO1",key='-host-'),sg.Radio('ゲスト', "RADIO1", default=True),sg.Text('ホスト:笑わせる側')],
    [sg.Submit('入室')]
]
    
    
    layout = [
    [sg.Text('ゲーム設定')],
    [sg.Spin(time0, key='-min-',initial_value=2, size=(7, 1)),sg.Text('分'),
     sg.Spin(time0, key='-sec-',initial_value=30, size=(7, 1)),sg.Text('秒'),sg.Text('プレイ時間を設定')],
    [sg.Text('詳細設定'), frame1],  
    [sg.Submit('開始')]
]

#モード選択
#フリーモード：表情判定とclear,ログのみ
#ゲームモード：ホストとゲスト

# セクション 2 - ウィンドウの生成
    window0 = sg.Window('入室',layout0)
    counter=0
    pygame.mixer.music.load("main.mp3")
    pygame.mixer.music.play(-1)

    video_capture = cv2.VideoCapture(cam)
# セクション 3 - イベントループ
    while True:
        event, values = window0.read(timeout=10)
        cap=video_capture.read()[1]
        window00['image'](data=cv2.imencode('.png', cap)[1].tobytes())
        window00.finalize()
        #cv2.imshow("camera",cap)
        #cv2.waitKey(1)
        #event, values = window0.read(timeout=10)
        
        if event is None:
            if counter>=1:
                try:#Exit
                    exit={"action":"ExitRoom","data":"A"}
                    ws.send(json.dumps(exit))
                    ws.close()
                    window0.close()
                    iromonea.normal(window00)
                    sys.exit()
                except:
                    ws.close()
            else:
                window0.close()
                video_capture.release()
                #cv2.destroyAllWindows()
                iromonea.normal(window00)
                sys.exit()
               
        elif event == '入室':
            roomid=values['-room-']
            nickname=values['-name-']
            players=values['-player-']
            password=values['-pass-']
            host_state=values['-host-']
            limit=str(values['-clear-']) 
            if counter==0:
            #EnterRoom roomnum,nickname
                ws = websocket.create_connection("wss://7dltq43ti1.execute-api.us-east-1.amazonaws.com/alpha")
                data=values['-room-']+","+values['-name-']
                enter={"action":"EnterRoom","data":data}
                ws.send(json.dumps(enter))
                counter+=1
            else:
            #check-section
            #roomnum,nickname,plyernum,password,limit
                if host_state is True:
                    pygame.mixer.music.load("warai.mp3")
                    pygame.mixer.music.play()
                data=data+","+str(players)+","+password+","+limit
                check={"action":"check","data":data}
                ws.send(json.dumps(check))
                result =  ws.recv()
                if result=="clear":
                    break
                else:
                    #ポップアップ
                    sg.popup("少し待って再実行して下さい")

# セクション 4 - ウィンドウの破棄と終了
    window0.close()
    window1 = sg.Window('設定', layout)
    while True:
        event, values = window1.read(timeout=10)
        if event is None:
            #Exit
            data1=roomid
            check={"action":"ExitRoom","data":data1}
            ws.send(json.dumps(check))
            window1.close()
            video_capture.release()
            #cv2.destroyAllWindows()
            iromonea.normal(window00)
            sys.exit()
        elif event == '開始':
            minit=int(values["-min-"])
            sec=int(values["-sec-"])
            sense=values["-sensitive-"]
            life=values["-life-"]
            sontaku=values["-sontaku-"]
            setfps=int(values["-fps-"])
            time1=float(minit*60+sec)
            pygame.mixer.music.load("roulette.mp3")
            pygame.mixer.music.play() 
            time.sleep(3)
            #start
            start={"action":"Start","data":data}
            ws.send(json.dumps(start))
            while True:
                result =  ws.recv()
                if result=="start":
                    starttime=time.time()
                    pygame.mixer.music.load("start.mp3")
                    pygame.mixer.music.play()
                    break
                else:
                    sg.popup("開始を待っています")
            break
    window1.close()
    if host_state is True:
        host(ws,data,time1,setfps,starttime,cam,window00)
        iromonea.normal(window00)
        sys.exit()
    else:
        #guest.py
        

  # parameters for loading data and images
        detection_model_path = 'trained_models/detection_models/haarcascade_frontalface_default.xml'
        emotion_model_path = 'trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
        emotion_labels = get_labels('fer2013')

    # hyper-parameters for bounding boxes shape
        frame_window = 10
        emotion_offsets = (20, 40)

    # loading models
        face_detection = load_detection_model(detection_model_path)
        emotion_classifier = load_model(emotion_model_path, compile=False)

    # getting input model shapes for inference
        emotion_target_size = emotion_classifier.input_shape[1:3]

    # starting lists for calculating modes
        emotion_window = []

    # starting video streaming
    #cv2.namedWindow('window_frame')
        video_capture = cv2.VideoCapture(cam)
        endtime=starttime+time1
        flag=0
        count=0
        telop_height=50
        video_capture.set(cv2.CAP_PROP_FPS,setfps)
        #print("set:",setfps)
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        #print("fps:",fps)
        happy_meter=[0,"|----|----|----|----|----|----|----|----|----|----|"]
        happy_level=sense
        Life=life*sontaku
        flag_count=Life
        ccounter=0
        log=[]
        name=["defalt"]
        state={"action":"state","data":data}
        break1=0
        while True:
            timer=round(endtime-time.time(),1)
            if break1==1:
                break
            ws.send(json.dumps(state))
            result =  ws.recv()
            """if result =="end":
                pygame.mixer.music.load("win.mp3")
                pygame.mixer.music.play()
                break"""
            if result== "" or "message" in result:
                pass
            else:
                result=result.split(",")
                del result[0]
                for x in result:
                    if x=="end":
                        ccounter="win"
                        pygame.mixer.music.load("win.mp3")
                        pygame.mixer.music.play()
                        time.sleep(4)
                        break1=1
                        break
                    elif x  not in name:
                        name.append(x)
                        res=x+"さん:"+str(round(time1-timer,1))+"秒"
                        #改善の余地あり
                        pygame.mixer.music.load("clear.mp3")
                        pygame.mixer.music.play()
                        log.append(res)
                    
            bgr_image = video_capture.read()[1]
            gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
            rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
            faces = detect_faces(face_detection, gray_image)
            timer=round(endtime-time.time(),1)
    
            for face_coordinates in faces:

                x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
                gray_face = gray_image[y1:y2, x1:x2]
                try:
                    gray_face = cv2.resize(gray_face, (emotion_target_size))
                except:
                    continue

                gray_face = preprocess_input(gray_face, True)
                gray_face = np.expand_dims(gray_face, 0)
                gray_face = np.expand_dims(gray_face, -1)
                emotion_prediction = emotion_classifier.predict(gray_face)
                emotion_probability = np.max(emotion_prediction)
                emotion_label_arg = np.argmax(emotion_prediction)
                emotion_text = emotion_labels[emotion_label_arg]
                emotion_window.append(emotion_text)

                if len(emotion_window) > frame_window:
                    emotion_window.pop(0)
                try:
                    emotion_mode = mode(emotion_window)
                except:
                    continue

                if emotion_text == 'angry':
                    color = emotion_probability * np.asarray((255, 0, 0))
                elif emotion_text == 'sad':
                    color = emotion_probability * np.asarray((0, 0, 255))
                elif emotion_text == 'happy':
                    color = emotion_probability * np.asarray((255, 255, 0))
    
                elif emotion_text == 'surprise':
                    color = emotion_probability * np.asarray((0, 255, 255))
                else:
                    color = emotion_probability * np.asarray((0, 255, 0))
            
                color = color.astype(int)
                color = color.tolist()

                draw_bounding_box(face_coordinates, rgb_image, color)
                draw_text(face_coordinates, rgb_image, emotion_mode,
                      color, 0, -45, 1, 1)
    
            bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)

            cap_width=bgr_image.shape[1]
            cap_height=bgr_image.shape[0]
            happy_meter[0]=int(emotion_window.count('happy')/happy_level*100)
            happy_meter[1]="|----|----|----|----|----|----|----|----|----|----|"
            happy_meter[1]=happy_meter[1].replace("-","#",int(happy_meter[0]/2.5))
            Life_meter="["+"@"*int(Life/sontaku)+"]"

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(bgr_image, "damage{}[%]".format(happy_meter[0]), 
                (10, 50), 
                font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(bgr_image, "{}".format(happy_meter[1]), 
                (10, 100), 
                font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(bgr_image, "Life:{}".format(Life_meter), 
                (10, 150), 
                font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(bgr_image, "{} [OUT]".format(len(name)-1), 
                (cap_width - 300, cap_height -telop_height-60), 
                font, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(bgr_image, "{} [fps]".format(round(fps,1)), 
                (cap_width - 300, cap_height -telop_height-30), 
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(bgr_image, "{:.2f} [sec]".format(timer), 
                (cap_width - 300, cap_height -telop_height), 
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            count += 1
            #cv2.imshow('camera', bgr_image)
            window00['image'](data=cv2.imencode('.png', bgr_image)[1].tobytes())
            window00.finalize()
    
            if emotion_window.count('happy')>happy_level:
                flag+=1
                Life-=1
                if flag==flag_count:
                    pygame.mixer.music.load("clear.mp3")
                    pygame.mixer.music.play() 
                    break
    
            elif cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif timer<=0:
                ccounter+=1
                pygame.mixer.music.load("lose.mp3")
                pygame.mixer.music.play()
                time.sleep(3.5)
                break
        
        if ccounter==0:
            mess={"action":"sendMessage","data":data}
            ws.send(json.dumps(mess))
            
        break1=0

        while flag>=flag_count:
            timer=round(endtime-time.time(),1)
            Life_meter="["+"@"*int(Life/sontaku)+"]"
            bgr_image = video_capture.read()[1]
            bgr_image = cv2.cvtColor(bgr_image, cv2.COLOR_RGB2BGR)
            imgback = bgr_image
            img = cv2.imread('clear.png')
            height=imgback.shape[0]
            width=imgback.shape[1]
            img=cv2.resize(img,(width,height))
            dst=cv2.addWeighted(imgback, 1, img, 0.8, 0)  
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(dst, "damage:{}[%]".format(happy_meter[0]), 
                (10, 50), 
                font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(dst, "{}".format(happy_meter[1]), 
                (10, 100), 
                font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(dst, "Life:{}".format(Life_meter), 
                    (10, 150), 
                font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(dst, "{} [OUT]".format(len(name)-1), 
                (width - 300, height -telop_height-60), 
                font, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(dst, "{} [fps]".format(round(fps,1)), 
                (width - 300, height -telop_height-30), 
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(dst, "{:.2f} [sec]".format(timer), 
                    (width - 300, height -telop_height), 
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            count += 1
            #cv2.imshow('camera',dst)
            window00['image'](data=cv2.imencode('.png', dst)[1].tobytes())
            window00.finalize()
            if break1==1:
                break
            result =  ws.recv()
            ws.send(json.dumps(state))
    
            """if result =="end":
                pygame.mixer.music.load("win.mp3")
                pygame.mixer.music.play() 
                break
            elif result== "" or "message" in result:
                pass"""
            #cv2.waitKey(1) & 0xFF == ord('q')
            if timer<=0:
                pygame.mixer.music.load("lose.mp3")
                pygame.mixer.music.play()
                time.sleep(3.5)
                break
            else:
                result=result.split(",")
                del result[0]
                for x in result:
                    if x=="end":
                        ccounter="win"
                        pygame.mixer.music.load("win.mp3")
                        pygame.mixer.music.play()
                        break1=1
                        break
                    elif x  not in name:
                        name.append(x)
                        res=x+"さん:"+str(round(time1-timer,1))+"秒"
                        pygame.mixer.music.load("clear.mp3")
                        pygame.mixer.music.play()
                        log.append(res)
                    
        my_text=""        
        if len(log)>0:
            my_text=log[0]
            del log[0]
        for x in log:
            my_text=my_text+'\n' +x
        layout=[[sg.Text('結果発表',font=('HG行書体',24),
                         text_color='#ff0000', background_color = '#0000ff')],
        [sg.Text("笑いログ")],
        [sg.Text(my_text)],
        [sg.Submit('OK')]
        ]        
        final = sg.Window("結果",layout)
        while True:
            event, values = final.read()
            if event in (None,"OK"):
                break
    #Exit
        data1=roomid
        exit={"action":"ExitRoom","data":data1}
        ws.send(json.dumps(exit))  
        final.close()
        video_capture.release()
        cv2.destroyAllWindows()
        iromonea.normal(window00)
        
def host(ws,data,time1,setfps,starttime,cam,window00):
    #roomnum,nickname,plyernum,password,limit
    pygame.mixer.music.load("start.mp3")
    pygame.mixer.music.play()
    inter=data.split(",")
    roomid=inter[0]
    endtime=starttime+time1
    players=int(inter[2])
    video_capture = cv2.VideoCapture(cam)
    flag=0
    count=0
    telop_height=50
    video_capture.set(cv2.CAP_PROP_FPS,setfps)
    #print("set:",setfps)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    #print("fps:",fps)
    target_meter=[0,"|----|----|----|----|----|----|----|----|----|----|"]
    ccounter=""
    log=[]
    name=["defalt"]
    state={"action":"state","data":data}
    break1=0
    while True:
        #timer=time-round(count/fps, 2)
        timer=round(endtime-time.time(),1)
        if break1==1:
            break
        ws.send(json.dumps(state))
        result =  ws.recv()
        """if result =="end":
            ccounter="win"
            pygame.mixer.music.load("win.mp3")
            pygame.mixer.music.play()
            break"""
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif timer<10:
            pygame.mixer.music.load("count.mp3")
            pygame.mixer.music.play(-1)
            time.sleep(2)
            break
        elif result== "" or "message" in result:
            pass
        else:
            result=result.split(",")
            del result[0]
            for x in result:
                if x=="end":
                    ccounter="win"
                    pygame.mixer.music.load("win.mp3")
                    pygame.mixer.music.play()
                    break1=1
                    break
                elif x  not in name:
                    flag=1
                    #res=x+"さん:"+str(round(count/fps,1))+"秒"
                    res=x+"さん:"+str(round(time1-timer,1))+"秒"
                    pygame.mixer.music.load("clear.mp3")
                    pygame.mixer.music.play()
                    log.append(res)
                    name.append(x)
                
        bgr_image = video_capture.read()[1]
        cap_width=bgr_image.shape[1]
        cap_height=bgr_image.shape[0]
        target_meter[0]=len(name)
        target_meter[1]="|----|----|----|----|----|----|----|----|----|----|"
        target_meter[1]=target_meter[1].replace("-","#",int((len(name)-1)/players*100/2.5))

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(bgr_image, "TARGET:{}".format(target_meter[1]), 
                (10, 50), 
                font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(bgr_image, "{} [OUT]".format(len(name)-1), 
                (cap_width - 300, cap_height -telop_height-60), 
                font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(bgr_image, "{} [fps]".format(round(fps,1)), 
                (cap_width - 300, cap_height -telop_height-30), 
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)   #time-round(count/fps, 2)
        cv2.putText(bgr_image, "{:.2f} [sec]".format(timer), 
                (cap_width - 300, cap_height -telop_height), 
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        #count += 1
        window00['image'](data=cv2.imencode('.png', bgr_image)[1].tobytes())
        window00.finalize()
        #cv2.imshow('camera', bgr_image)
        intercount=0
        while flag==1:
            #and intercount<=3
            timer=round(endtime-time.time(),1)
            bgr_image = video_capture.read()[1]
            imgback = bgr_image
            img = cv2.imread('hit.png')
            height=imgback.shape[0]
            width=imgback.shape[1]
            target_meter[0]=len(name)
            target_meter[1]="|----|----|----|----|----|----|----|----|----|----|"
            target_meter[1]=target_meter[1].replace("-","#",int((len(name)-1)/players*100/2.5))
            img=cv2.resize(img,(width,height))
            dst=cv2.addWeighted(imgback, 1, img, 0.5, 0)  
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(dst, "TARGET{}".format(target_meter[1]), 
                (10, 100), 
                font, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(dst, "{} [OUT]".format(len(name)-1), 
                (width - 300, height -telop_height-60), 
                font, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.putText(dst, "{} [fps]".format(round(fps,1)), 
                (width - 300, height -telop_height-30), 
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(dst, "{:.2f} [sec]".format(timer), 
                    (width - 300, height -telop_height), 
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            flag=0
            #count += 1
            #intercount+=1
            #cv2.imshow('camera',dst)
            #cv2.waitKey(1)
            window00['image'](data=cv2.imencode('.png', dst)[1].tobytes())
            window00.finalize()
    while timer<10:
        timer=endtime-time.time()
        bgr_image = video_capture.read()[1]
        imgback = bgr_image
        img = cv2.imread('red.png')
        height=imgback.shape[0]
        width=imgback.shape[1]
        target_meter[0]=len(name)
        target_meter[1]="|----|----|----|----|----|----|----|----|----|----|"
        target_meter[1]=target_meter[1].replace("-","#",int((len(name)-1)/players*100/2.5))
        img=cv2.resize(img,(width,height))
        dst=cv2.addWeighted(imgback, 1, img, 0.2, 0)  
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(dst, "TARGET{}".format(target_meter[1]), 
                (10, 100), 
                font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(dst, "{} [OUT]".format(len(name)-1), 
                (width - 300, height -telop_height-60), 
                font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(dst, "{} [fps]".format(round(fps,1)), 
                (width - 300, height -telop_height-30), 
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(dst, "{:.2f} [sec]".format(timer), 
                    (int(width/2), 200), 
                font, 3, (0, 0, 255), 2, cv2.LINE_AA)
        #count += 1
        #cv2.imshow('camera',dst)
        window00['image'](data=cv2.imencode('.png', dst)[1].tobytes())
        window00.finalize()
        if break1==1:
            break
        ws.send(json.dumps(state))
        result =  ws.recv()
    
        """if result =="end":
            ccounter="win"
            pygame.mixer.music.load("win.mp3")
            pygame.mixer.music.play()
            break
        elif result== "" or "message" in result:
            pass"""
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif timer<=0:
            ccounter="lose"
            pygame.mixer.music.load("lose.mp3")
            pygame.mixer.music.play()
            time.sleep(3.5)
            break
        else:
            result=result.split(",")
            del result[0]
            for x in result:
                if x=="end":
                    ccounter="win"
                    pygame.mixer.music.load("win.mp3")
                    pygame.mixer.music.play()
                    time.sleep(4)
                    break1=1
                    break
                elif x  not in name:
                    name.append(x)
                    res=x+"さん:"+str(round(time1-timer,1))+"秒"
                    pygame.mixer.music.load("clear.mp3")
                    pygame.mixer.music.play()
                    log.append(res)
                
    my_text=""        
    if len(log)>0:
        my_text=log[0]
        del log[0]
        for x in log:
            my_text=my_text+'\n' +x
    if ccounter=="win":
        resul="You Win!"
    else:
        resul="LOSE"
    layout=[[sg.Text(resul,font=('HG行書体',50),
                         text_color='#ff0000', background_color = '#0000ff')]
                ,[sg.Text('結果発表',font=('HG行書体',24),
                         text_color='#ff0000', background_color = '#0000ff')],
            [sg.Text("笑いログ")],
            [sg.Text(my_text)],
            [sg.Submit('OK')]
            ]        
    final = sg.Window("結果",layout)
    while True:
        event, values = final.read()
        if event in (None,"OK"):
            break
    #Exit
    data1=roomid
    exit={"action":"ExitRoom","data":data1}
    ws.send(json.dumps(exit))  
    final.close()
    video_capture.release()
    #cv2.destroyAllWindows()
