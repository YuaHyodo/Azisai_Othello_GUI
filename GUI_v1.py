"""
This file is part of Azisai_Othello_GUI

Copyright (c) 2022 YuaHyodo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
リポジトリ: https://github.com/YuaHyodo/Azisai_Othello_GUI
"""

from copy import deepcopy
from tkinter import*

class Simple_GUI:
    def __init__(self):
        #色とかを設定する
        self.area_A_bg = 'blue'
        self.area_A_button_color = ['gray', 'black']
        self.info_area1_bg_color = ['black', 'darkblue', 'yellow', 'purple']
        self.info_area1_fg_color = ['gold', 'black', 'yellow']
        self.info_area2_bg = 'skyblue'
        self.graph_color = 'orange'
        #windowを初期化する
        self.init_window()

    def init_window(self):
        #タイトル・サイズ等を決める
        self.title = 'Azisai_Othello_GUI(v1)'
        self.size = '500x500'
        #windowを作り、サイズ・タイトルを設定する
        self.window = Tk()
        self.window.title(self.title)
        self.window.geometry(self.size)

        #windowを4つのエリアに区切る
        #それぞれのエリアに対応するFrameを作る
        self.area_A = Frame(self.window)#, width=500, height=20, bg=self.area_A_bg)
        self.Board_area = Frame(self.window)#, width=300, height=300)
        self.info_area1 = Frame(self.window)#, width=200, height=300)
        self.info_area2 = Frame(self.window)#, width=300, height=280)

        #各種エリアをリセットする
        self.init_area_A()
        self.init_Board_area()
        self.init_info_area1()
        self.init_info_area2()

        #サイズを決めて、配置する
        self.area_A.place(x=0, y=0, width=500, height=30)
        self.Board_area.place(x=0, y=30, width=320, height=320)
        self.info_area1.place(x=320, y=30, width=180, height=320)
        self.info_area2.place(x=0, y=350, width=500, height=150)

        #更新を反映する
        self.window.update()
        return

    def init_area_A(self):
        """
        上にあるやつ
        """
        #それぞれのButtonのサイズを決める
        W = int(500 / 4)
        H = 30

        #接続・対局をするButton
        self.online_button = Button(self.area_A,
                                        text='connect',
                                        bg=self.area_A_button_color[0],
                                        fg=self.area_A_button_color[1],
                                        command=self.online_play)#,
                                        #width=W, height=H)

        #ストップするButton
        self.stop_button = Button(self.area_A,
                                        text='stop',
                                        bg=self.area_A_button_color[0],
                                        fg=self.area_A_button_color[1],
                                        command=self.stop)#,
                                        #width=W, height=H)

        #設定画面を開くButton
        self.setting_button = Button(self.area_A,
                                        text='setting',
                                        bg=self.area_A_button_color[0],
                                        fg=self.area_A_button_color[1],
                                        command=self.setting)#,
                                        #width=W, height=H)

        #今の状態を表す部分
        self.state_info = Label(self.area_A, text='state: OFFLINE',
                                        bg=self.area_A_button_color[0],
                                        fg=self.area_A_button_color[1])
        
        #配置する
        self.online_button.place(x=0, y=0, width=W, height=H)
        self.stop_button.place(x=W, y=0, width=W, height=H)
        self.setting_button.place(x=W * 2, y=0, width=W, height=H)
        self.state_info.place(x=W * 3, y=0, width=W, height=H)
        return

    def init_Board_area(self):
        """
        Boardを表示するエリア
        """
        #1マスの大きさを決める
        W = 40
        H = 40
        #管理用のlist
        self.sq = []
        #Othello sfen viewerのコードを流用
        D = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        for i in range(8):
            rank = []
            for j in range(8):
                #Buttonである必要はない
                rank.append(Button(self.Board_area, text=D[j] + str(i + 1),
                                 fg = 'red', bd=2, bg='green',
                                 relief='ridge'))
            self.sq.append(rank)
        #配置する
        for i in range(8):
            for j in range(8):
                #self.sq[i][j].grid(column=j, row=i)
                self.sq[i][j].place(x=j * W, y=i * H, width=W, height=H)
        return

    def init_info_area1(self):
        """
        エンジンの情報と、手版・持ち時間の情報を表示するエリア
        """
        
        #エンジンの名前を表示する場所
        self.name_area = Label(self.info_area1, text='engine_name',
                                   bg=self.info_area1_bg_color[1], fg=self.info_area1_fg_color[0],
                                   relief='ridge')

        #残り持ち時間を表示する場所
        self.time_area = Label(self.info_area1, text='time: 0',
                                 bg=self.info_area1_bg_color[3], fg=self.info_area1_fg_color[2],
                                 relief='ridge')

        #手番を表示する場所
        self.color_area = Label(self.info_area1, text='color: None',
                                  bg=self.info_area1_bg_color[3], fg=self.info_area1_fg_color[2],
                                 relief='ridge')

        #エンジンメッセージを表示する場所
        self.message_area = Label(self.info_area1, text='engine_message',
                                  bg=self.info_area1_bg_color[2], fg=self.info_area1_fg_color[1],
                                  relief='ridge')
        
        #配置
        self.time_area.place(x=0, y=0, width=90, height=30)
        self.color_area.place(x=90, y=0, width=90, height=30)
        self.name_area.place(x=0, y=30, width=180, height=30)
        self.message_area.place(x=0, y=60, width=180, height=260)
        return

    def init_info_area2(self):
        """
        評価値グラフを表示する場所
        """
        #グラフを描画する場所を用意し、真ん中に線を引く
        self.graph_area = Canvas(self.info_area2, bg=self.info_area2_bg)
        self.graph_area.create_rectangle(0, 74, 500, 76, fill='darkblue')
        #配置
        self.graph_area.place(x=0, y=0, width=500, height=150)
        return

    def plot_graph(self, values):
        """
        評価値のリストを渡すと、グラフを描いてくれる
        どんなスケールのグラフでも描ける
        """
        #手数を取得
        moves = len(values)
        #最小値・最大値を取得
        max_value = max(values)
        min_value = min(values)
        #横幅を決める
        W = (500 / moves)
        for i in range(moves):
            #高さを計算
            H = int(50 * (values[i] / max([abs(max_value), abs(min_value)])))
            #描画
            if H >= 75:
                self.graph_area.create_rectangle((W * i), H, (W * (i + 1)), 75, fill=self.graph_color)
            else:
                self.graph_area.create_rectangle((W * i), 75, (W * (i + 1)), (75 - H), fill=self.graph_color)
        #更新
        self.window.update()
        return

    def online_play(self):
        #online_buttonが押されたときに動く関数
        pass

    def stop(self):
        #stop_buttonが押されたときに動く関数
        pass

    def setting(self):
        #setting_buttonが押されたときに動く関数
        pass

    def reset_setting(self):
        #setting_windowのreset_setting_buttonが押されたときに動く関数
        pass

    def save_setting(self):
        #setting_windowのsave_buttonが押されたときに動く関数
        pass

    def update_board(self, sfen):
        """
        Board_areaをsfenを使って更新する
        """
        color_d = {'O': 'white', 'X': 'black', '-': 'green'}
        for i in range(8):
            for j in range(8):
                #色を変える
                self.sq[i][j].configure(bg=color_d[sfen[(i * 8) + j]])
        #更新
        self.window.update()
        return

    def make_setting_window(self, change):
        """
        setting_windowを作る。
        setting_windowでは設定を変えられる
        """
        #windowを作り、タイトル・サイズを設定する
        self.setting_window = Tk()
        self.setting_window.title('Azisai_Othello_GUI_Setting')
        self.setting_window.geometry('300x300')

        #今の設定をコピー
        self.after_change_setting = change.copy()

        #接続先を設定する場所
        self.text1 = Label(self.setting_window, text='host')
        self.host_input = Text(self.setting_window)

        #対局するエンジンを設定する場所
        self.text2 = Label(self.setting_window, text='engine')
        self.engine_input = Text(self.setting_window)

        #アカウント名を設定する場所
        self.text3 = Label(self.setting_window, text='player_name')
        self.player_name_input = Text(self.setting_window)

        #パスワードを設定する場所
        self.text4 = Label(self.setting_window, text='password')
        self.password_input = Text(self.setting_window)

        #設定をデフォルトに戻すbutton
        self.reset_setting_button = Button(self.setting_window, text='reset',
                                                bg='red', fg='black', relief='ridge', command=self.reset_setting)

        #設定を保存するbutton
        self.save_button = Button(self.setting_window, text='save', bg='white', fg='black',
                                      relief='ridge', command=self.save_setting)

        #設置
        self.text1.place(x=10, y=10, width=100, height=20)
        self.host_input.place(x=10, y=30, width=100, height=20)
        
        self.text2.place(x=190, y=10, width=100, height=20)
        self.engine_input.place(x=190, y=30, width=100, height=20)

        self.text3.place(x=10, y=60, width=100, height=20)
        self.player_name_input.place(x=10, y=80, width=100, height=20)

        self.text4.place(x=190, y=60, width=100, height=20)
        self.password_input.place(x=190, y=80, width=100, height=20)

        self.reset_setting_button.place(x=10, y=270, width=100, height=20)
        self.save_button.place(x=190, y=270, width=100, height=20)
        return

if __name__ == '__main__':
    gui = Simple_GUI()
