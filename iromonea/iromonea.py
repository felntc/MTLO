#normal.py-win dist
import tkinter
import PySimpleGUI as sg
import cv2
import freemode0
import gamemode0
import pygame

def initialize():
    window00= sg.Window('camera', [[sg.Image(filename='', key='image')], ], location=(0, 0), grab_anywhere=True)
    cam=0
    normal(window00,cam)

def normal(window00,cam):
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
        [sg.Spin(lis,key="-camnum-",initial_value=0),sg.Text("カメラ番号を選択")]
        ,[sg.Button('カメラ指定')],
        [sg.Text("詳細"),frame1],
        [sg.Button('ゲームモード'), sg.Button('フリーモード')]
    ]
   
    cap = cv2.VideoCapture(cam)
    window=sg.Window("iromonea",layout0)
    #window00= sg.Window('camera', [[sg.Image(filename='', key='image')], ], location=(0, 0), grab_anywhere=True)
    while True:
        event, values = window.read(timeout=20)
        a=cap.read()[1]
        window00['image'](data=cv2.imencode('.png', a)[1].tobytes())
        window00.finalize()

        if event=="ゲームモード":
            pygame.mixer.music.load("select.mp3")
            pygame.mixer.music.play() 
            window.close()
            gamemode0.game(cam,window00)
        elif event=="フリーモード":
            pygame.mixer.music.load("select.mp3")
            pygame.mixer.music.play()
            window.close()
            freemode0.free(cam,window00)
        elif event=="カメラ指定":
            cam=int(values["-camnum-"])
            sg.popup("カメラ"+str(cam)+"を設定しました")
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