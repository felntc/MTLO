# iromonea
- 笑わせるホストk人、観客n-k人のゲストに分ける
- 制限時間以内にゲストをi人笑わせれば勝ち、時間が来たら負けのゲーム  
- ホストはネタや話で笑わせる。画面共有するのもあり  
![image](https://user-images.githubusercontent.com/64360965/82986242-79c43e80-a030-11ea-96c9-621453beb439.png)  

# 利用アンケートにご協力ください  
https://forms.gle/Ki7M2oo6E9GcrcpM9

## 概要
- ZoomやGooglemeetなどで、イロモネアを実現するアプリケーションです
- それぞれが必要なツールを揃える必要があります
- 一人でもお試しすることができ、理論上大多数の人数でもプレイできます
- 開発途中なので、技術的な問題が多々あります。おおらかな目でプレイしてください

## 用意するもの
**※(Zoomなどでカメラ出力する場合)** 
- OBSなどの配信ソフト  
https://obsproject.com/ja/download  
- OBS virtualcameraなどのバーチャルカメラ  
win:https://obsproject.com/forum/resources/obs-virtualcam.539/  
win参考サイト:https://level69.net/archives/26918  
Mac:https://github.com/johnboiles/obs-mac-virtualcam/releases  
Mac参考サイト:https://note.com/junky/n/neeeeddf57bde  
注意:MacだとZoomでうまく認識されず、署名を書き換えたりする場合があります(上記参照)

### 画面共有を駆使してバーチャルカメラを使わない方法も可能ですが非推奨です  
(ZoomとGooogleMeet、slackなどで繋ぎまくって一人一サービスで画面共有など)　　

## python環境導入についてはinstallation.mdを参照  
install
  
## 遊び方
- Python環境→iromonea/iromonea.pyを実行する
- exeで実行→releasesからwindows packageをダウンロードし、windowspackage/iromonea/iromonea.exeを実行
  
### 最初に(毎回)やること
1. **まずメインメニューで"カメラ指定"ボタンを押します(この画面になるたび必要)**
![image](https://user-images.githubusercontent.com/64360965/82986397-b6903580-a030-11ea-9f9a-de728598380e.png)
2. ***既に顔が写っていても必ず押してください***(ほとんどの人は0番です)  
※デフォルトのカメラは"1"になっていますが、0がバーチャルカメラの場合もあります。0,1,2...というように確かめてください

### zoomなどの設定
1. アプリを起動する  
1. OBSを起動する  
2. OBSでツール→バーチャルカメラを起動 
![image](https://user-images.githubusercontent.com/64360965/82987669-e50f1000-a032-11ea-9d13-a1fe975be3bc.png)
3. OBSで下のソース→"+"ボタン→ウィンドウキャプチャを選択  
![image](https://user-images.githubusercontent.com/64360965/82987710-fb1cd080-a032-11ea-83ac-0571c6b94164.png)
4. python-cameraを探す  
5. なければshow hidden windowsにチェックして探す  
6. OBSで赤枠で画面の位置を調整する（フルサイズだとzoomなどに収まらないので小さめで）
4. Zoomを起動し、カメラをバーチャルカメラに変更。反転していないか確かめる

### フリーモード
- 一人で笑顔の検出を試してみるモードです。パラメータをいじれます
- ***ここで光のあたり具合やカメラの向きを調整して検出しやすいポジションを見分けると良いでしょう***
### ゲームモード
- 複数人でプレイします。オンライン環境、バーチャルカメラが必要です
![image](https://user-images.githubusercontent.com/64360965/82986799-77161900-a031-11ea-9b27-e0b2f99c191d.png)
1. お名前、パスワードを入力します。
2. グループでプレイ人数と部屋ID、クリア条件を決めておいてください。*共通のもの*を使用します
ホストが複数人であっても大丈夫です
3. 入室を一回押すとログインします
4. **もう一度入室を押してください。** パスワードや人数が同じであれば次に進みます
4. ポップアップが出たら誰かがログインしていないか、設定ミスです。設定ミスの場合は×を押してもう一度初めから...
![image](https://user-images.githubusercontent.com/64360965/82987217-2a7f0d80-a032-11ea-87f9-8059ef3ccfca.png)
5. 制限時間を決め、入力します。*共通のもの*を使用します
5. その他FPSや感知の敏感さなどを決めてください(適当で良い)
6. 開始を押します。全員が開始を押すとスタートします
7. 制限時間内にホストが規定の人数を笑わせたらクリア、他は失敗です

## 注意事項
- **バックエンドにAWSを使用していますが、課金状況によっては取りやめることがあります**
- そのため、永続的な動作は保証できません
- **逆光などの条件ではうまく表情を判別しない時があります**
- うまく検出されない時はカメラの向きや距離、光のあたり具合を調整しましょう
- Mac Catalina /Zoom5.0.2では動作を確認しています
- 動作が重いです。これは作者の設計やコードスキルによるところが大きいと思われます

