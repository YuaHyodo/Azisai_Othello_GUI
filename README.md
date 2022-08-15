# Azisai_Othello_GUI
USI-Xエンジン(オセロ)をOnline Othello Protocolでオンライン対局できるようにするためのツール

# 概要
- USI-XエンジンがOnline Othello Protocolで対局できるようになるためのツール
- USI-Xプロトコルに対応していれば、Online Othello Protocolを使ったオンライン対局もできるようになる
- ファイル・クラス・関数・変数名、出力されるメッセージ、実装方法、設計思想などに関する意見は受け付けておりません。 (不満があるなら自分で作ってください)

- USI-Xプロトコル(オセロ版)についてはこちらを参照のこと: https://github.com/YuaHyodo/USI-X-protocol_othello_version

- Online Othello Protocolについてはこちらを参照のこと: https://github.com/YuaHyodo/online_othello_protocol

- Online Othello Protocolの超簡易的な対局サーバーのリポジトリはこちら: https://github.com/YuaHyodo/Ari-Othello-Server

- USI-Xエンジンが複数置いてあるリポジトリはこちら: https://github.com/YuaHyodo/python-dlothello

- USI-Xプロトコルに関するサンプルプログラムの置き場はこちら: https://github.com/YuaHyodo/USI-X_Othello_Samples

# 注意
- 実行にはsnail_reversi( https://github.com/YuaHyodo/snail_reversi )と、<br>
USI_X_Engine_Bridge( https://github.com/YuaHyodo/USI_X_Engine_Bridge )が必要です。
- snail_reversi・USI_X_Engine_Bridgeをインストールする方法についてはそれぞれのリポジトリで確認してください。

# 搭載済みの機能
- USI-Xエンジンを呼び出し、既定の接続先に接続し、対局を行う機能
- 対局中の情報をグラフィカルに表示する機能
- 簡易的な評価値グラフの描画

# 今後の予定・お知らせ等
- 公開オンライン対局サーバーの設置に向けて現在作業中

## サンプル
![Azisai_Othello_GUI_サンプル1](https://user-images.githubusercontent.com/66828980/184169516-7ce0f89a-63d5-4eae-bd3d-e1f46b37bc35.png)

- 接続先などの変更する時の画面<br>
![Azisai_Othello_GUI_サンプル2](https://user-images.githubusercontent.com/66828980/184169718-5db875c5-c661-4c28-8920-820277ec64c4.png)

- 評価値グラフ<br>
![Azisai_Othello_GUI_サンプル3](https://user-images.githubusercontent.com/66828980/184169791-c356488f-95f6-44c6-b8ea-91ea87dff8d6.png)

# ライセンス
- Azisai_Othello_GUIは、MITライセンスです。
- 詳細はLICENSEファイルをご確認ください。
