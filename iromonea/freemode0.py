import matplotlib 
matplotlib.use('tkagg') 
from statistics import mode

import cv2
from keras.models import load_model
import numpy as np
import iromonea
import pygame
from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input
import sys

import PySimpleGUI as sg
    
def free(cam,window00):
    pygame.mixer.init() 
    sg.theme('Dark Blue 3')
    players=list(range(1,11))
    frame1 = sg.Frame("いじらなくてもOK",[[sg.Text('感度', size=(15, 1), ),sg.Spin(players, size=(7, 1),initial_value=8
                                                                     ,key='-sensitive-'),
                               sg.Text('低いほど敏感', size=(15, 1), )],
                         [sg.Text('ライフ', size=(15, 1)),sg.Spin(players, size=(7, 1),initial_value=1
                                                              ,key='-life-'),
                          sg.Text('何回笑っていいか', size=(20, 1))],
                               [sg.Text('忖度レベル', size=(15, 1), ),sg.Spin(players, size=(7, 1),initial_value=1
                                                                     ,key='-sontaku-'),
                               sg.Text('接待用', size=(15, 1), )]
                         ])

    layout = [
        [sg.Text('ゲーム設定')],
        [sg.Text('詳細設定'), frame1],  # frame1のレイアウトを入れ子にして入れている
        [sg.Submit('開始')]
    ]

    # セクション 2 - ウィンドウの生成
    window = sg.Window('設定', layout)
    #window00= sg.Window('camera', [[sg.Image(filename='', key='image')], ], location=(0, 0), grab_anywhere=True)
    video_capture = cv2.VideoCapture(cam)
    # セクション 3 - イベントループ
    while True:
        event, values = window.read(timeout=10)
        cap=video_capture.read()[1]
        window00['image'](data=cv2.imencode('.png', cap)[1].tobytes())
        window00.finalize()
        #cv2.imshow("camera",cap)
    
        if event is None:
            #run normal.py
            window.close()
            video_capture.release()
            cv2.destroyAllWindows()
            iromonea.normal(window00)
            sys.exit()

        if event == '開始':
            pygame.mixer.music.load("start.mp3")
            pygame.mixer.music.play() 
            break

    # セクション 4 - ウィンドウの破棄と終了
    window.close()
    sense=values["-sensitive-"]
    life=values["-life-"]
    sontaku=values["-sontaku-"]
    

    # parameters for loading data and images
    #path='pro/python/face_classification/'
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
    flag=0
    count=0
    telop_height=50
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    happy_meter=[0,"|----|----|----|----|----|----|----|----|----|----|"]
    happy_level=sense
    Life=life*sontaku
    flag_count=Life
    log=[]
    while True:
        bgr_image = video_capture.read()[1]
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = detect_faces(face_detection, gray_image)

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
        cv2.putText(bgr_image, "{} [OUT]".format(len(log)), 
                (cap_width - 300, cap_height -telop_height-60), 
                font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(bgr_image, "{} [fps]".format(round(fps,1)), 
                (cap_width - 300, cap_height -telop_height-30), 
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(bgr_image, "{:.2f} [sec]".format(round(count/fps, 2)), 
                (cap_width - 300, cap_height -telop_height), 
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        count += 1
        #cv2.imshow('window_frame', bgr_image)
        window00['image'](data=cv2.imencode('.png', bgr_image)[1].tobytes())
        window00.finalize()
    
        if emotion_window.count('happy')>happy_level:
            x="smile"+"さん:"+str(round(count/fps, ))+"秒"
            log.append(x)
            flag+=1
            Life-=1
            if flag==flag_count:
                pygame.mixer.music.load("clear.mp3")
                pygame.mixer.music.play() 
                break
    
        elif cv2.waitKey(1) & 0xFF == ord('q'):
            break
    layout09=[[sg.Text('コントロールメニュー',font=('HG行書体',24),
                         text_color='#ff0000', background_color = '#0000ff')],
        [sg.Submit('結果を見る')],[sg.Submit('やめる')]
        ]  
    window05 = sg.Window("次の操作",layout09)
    while flag>=flag_count:
        event,values=window05.read(timeout=10)
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
        cv2.putText(dst, "{} [OUT]".format(len(log)), 
                (width - 300, height -telop_height-60), 
                font, 1, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(dst, "{} [fps]".format(round(fps,1)), 
                (width - 300, height -telop_height-30), 
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(dst, "{:.2f} [sec]".format(round(count/fps, 2)), 
                    (width - 300, height -telop_height), 
                font, 1, (0, 0, 255), 2, cv2.LINE_AA)
        count += 1
        window00['image'](data=cv2.imencode('.png', dst)[1].tobytes())
        window00.finalize()
        #cv2.imshow('window_frame',dst)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
         #   break
        if event=="結果を見る":
            break
        elif event==None:
            break
        elif event=="やめる":
            window05.close()
            #window00.close()
            video_capture.release()
            cv2.destroyAllWindows()
            iromonea.normal(window00)
            sys.exit()
    window05.close()
    my_text=""
    if len(log)>0:
        my_text=log[0]
    for x in log:
        my_text=my_text+'\n' +x
    layout=[[sg.Text('結果発表',font=('HG行書体',24),
                         text_color='#ff0000', background_color = '#0000ff')],
        [sg.Text("笑いログ")],
        [sg.Text(my_text)],
        [sg.Submit('OK')],[sg.Submit('もう一度')]
        ]  
    #[sg.Text(log)],
    final = sg.Window("結果",layout)
    while True:
        event, values = final.read()
        if event in (None,"OK"):
            break
        else:
            final.close()
            free(cam,window00)
            sys.exit()
    final.close()
    video_capture.release()
    #cv2.destroyAllWindows()
    #window00.close()
    iromonea.normal(window00)
    


if __name__ == '__main__': 
    free()
