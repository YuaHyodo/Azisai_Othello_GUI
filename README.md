# Azisai_Othello_GUI
USI-Xエンジン(オセロ)のためのGUIや関連ツール

# 概要(全体)
- USI-Xプロトコル(オセロ)とOnline Othello Protocolに関するツールのリポジトリ

# ファイル毎の概要
## 古いやつ
- main.py: Azisai_Othello_GUI(v1)のメインファイル。Online Othello Protocolを使ったオンライン対局と、USI-Xエンジン同士のオフライン対極に対応。正直使い勝手が悪い。
- client.py: Online Othello Protocolを使ったオンライン対局のためのファイル。
- GUI.py: Azisai_Othello_GUI(v1)のGUIに関するファイル。
- Azisai_Othello_CUI_v1.py: Azisai_Othello_GUI(v1)のGUI無しバージョン。使い勝手が悪い。
- setting.json: Azisai_Othello_GUI(v1)とAzisai_Othello_CUI_v1のための設定ファイル。
## 新しいやつ
- Azisai_Othello_CUI_v2.py: USI-Xエンジン同士で対局するためのプログラム。オンラインでの対局は不可能。

# その他
- ファイル・クラス・関数・変数名、出力されるメッセージ、実装方法、設計思想などに関する意見は受け付けておりません。 (不満があるなら自分で作ってください)
- USI-Xプロトコル(オセロ版)についてはこちらを参照のこと: https://github.com/YuaHyodo/USI-X-protocol_othello_version
- Online Othello Protocolについてはこちらを参照のこと: https://github.com/YuaHyodo/online_othello_protocol
- Online Othello Protocolの簡易的な対局サーバーのリポジトリはこちら: https://github.com/YuaHyodo/Ari-Othello-Server
- USI-Xエンジンが複数置いてあるリポジトリはこちら: https://github.com/YuaHyodo/python-dlothello
- USI-Xプロトコルに関するサンプルプログラムの置き場はこちら: https://github.com/YuaHyodo/USI-X_Othello_Samples

# 注意
- 実行にはsnail_reversi( https://github.com/YuaHyodo/snail_reversi )と、<br>
USI_X_Engine_Bridge( https://github.com/YuaHyodo/USI_X_Engine_Bridge )が必要です。
- snail_reversi・USI_X_Engine_Bridgeをインストールする方法についてはそれぞれのリポジトリで確認してください。

# 搭載済みの機能
- USI-Xエンジンを呼び出し、既定の接続先に接続し、対局を行う機能
- USI-Xエンジンを2つ呼び出し、設定した持ち時間で対局を行う機能
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

- オフライン対局時の設定画面
![Azisai_Othello_GUI_サンプル4](https://user-images.githubusercontent.com/66828980/184886739-6ef5be7e-03a3-4014-960d-0a11add164b1.png)

- オフライン対局時のリザルト画面
![Azisai_Othello_GUI_サンプル5](https://user-images.githubusercontent.com/66828980/184886825-fb6e7cde-334d-481c-9d10-5483004b6cc6.png)


# ライセンス
- Azisai_Othello_GUIは、MITライセンスです。
- 詳細はLICENSEファイルをご確認ください。
