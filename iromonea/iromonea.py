#normal.py-win dist
import tkinter
import PySimpleGUI as sg
import cv2
import freemode0
import gamemode0
import pygame

def initialize():
    window00= sg.Window('camera', [[sg.Image(filename='', key='image')], ], location=(0, 0), grab_anywhere=True)
    normal(window00)

def normal(window00):
    pygame.mixer.init()
    lis=list(range(-1,5))
    frame1 = sg.Frame("遊び方",[[
                          sg.Text('このアプリを起動し、OBSVirtualcameraでZoomなどに繋ごう')],
                      [sg.Text("フリーモードはローカル、ゲームモードはオンラインです" )]
    ])
               
    layout0=[
        [sg.Text("メインメニュー",font=(' 小塚ゴシック Pro B',24),text_color = '#0000ff',
                 background_color='#ffff00',relief=sg.RELIEF_SUNKEN)],
        [sg.Image(filename='title.png')],
        [sg.Spin(lis,key="-camnum-",initial_value=1),sg.Text("カメラ番号を選択")]
        ,[sg.Button('カメラ指定')],
        [sg.Text("詳細"),frame1],
        [sg.Button('ゲームモード'), sg.Button('フリーモード')]
    ]

    #cap = cv2.VideoCapture(0)
    #window= sg.Window('Demo Application - OpenCV Integration', [[sg.Image(filename='', key='image')], ], location=(0, 0), grab_anywhere=True)
    #layout1=[[sg.Image(filename='', key='image')], ]
    #window2= sg.Window('OpenCV', [[sg.Image(filename='', key='image')], ], location=(0, 0), grab_anywhere=True)
    """layout = [
        [sg.TabGroup([[sg.Tab('スタート画面', layout0), sg.Tab('カメラ', layout1)]])],    
        [sg.Button('Read')]
    ]   """
    cap = cv2.VideoCapture(0)
    window=sg.Window("iromonea",layout0)
    #window00= sg.Window('camera', [[sg.Image(filename='', key='image')], ], location=(0, 0), grab_anywhere=True)
    cam=0
    while True:
        event, values = window.read(timeout=20)
        a=cap.read()[1]
        window00['image'](data=cv2.imencode('.png', a)[1].tobytes())
        window00.finalize()
        #cv2.imshow("camera",a)
        if event=="ゲームモード":
            pygame.mixer.music.load("select.mp3")
            pygame.mixer.music.play() 
            window.close()
            gamemode0.game(cam,window00)
        elif event=="フリーモード":
            #sg.popup("フリー")
            pygame.mixer.music.load("select.mp3")
            pygame.mixer.music.play()
            window.close()
            freemode0.free(cam,window00)
        elif event=="カメラ指定":
            cam=int(values["-camnum-"])
            cap.release()
            cv2.destroyAllWindows()
            cap = cv2.VideoCapture(cam)
        elif event==None:
            cap.release()
            cv2.destroyAllWindows()
            break
    window.close()
    window00.close()
    

if __name__ == '__main__': 
    initialize()