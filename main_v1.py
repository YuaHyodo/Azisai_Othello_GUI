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

from USI_X_Engine_Bridge import USI_X_Engine_Bridge as USI_X_Engine
from snail_reversi.Board import BLACK, WHITE, DRAW
from GUI_v1 import Simple_GUI as GUI
from snail_reversi.Board import Board
from threading import Thread
from client import Client
import time
import json

class main(GUI):
    def __init__(self):
        super().__init__()
        #設定を保存するファイル
        self.setting_file = 'setting.json'
        #設定を読み込む
        self.reset()
        

    def reset(self):
        #ファイルを開く
        with open(self.setting_file, 'r') as f:
            self.setting = json.load(f)
        #接続先
        self.host = self.setting['host']
        #[アカウント名, パスワード]
        self.player_info = self.setting['player_info']
        #USI-Xエンジン
        self.Engine_path = self.setting['engine']
        #エンジンの名前を表示するところを更新
        self.name_area.configure(text=self.Engine_path)
        return

    def graph_test(self):
        #グラフ機能のテスト
        scores = list(range(-30, 60))
        #scores = R.randint(-60, 60, 30)
        self.plot_graph(scores)
        return

    def reset_setting(self):
        #設定の初期化
        d = {'host': '127.0.0.1', 'player_info': ['usix_test', '1234'], 'engine': 'random_kun.bat'}
        with open(self.setting_file, 'w') as f:
            json.dump(d, f)
        try:
            self.setting_window.destroy()
        except:
            pass
        return

    def save_setting(self):
        #設定の保存
        #各種値を取得
        self.setting['host'] = ''.join(self.host_input.get('1.0', 'end').splitlines())
        self.setting['engine'] = ''.join(self.engine_input.get('1.0', 'end').splitlines())
        self.setting['player_info'][0] = ''.join(self.player_name_input.get('1.0', 'end').splitlines())
        self.setting['player_info'][1] = ''.join(self.password_input.get('1.0', 'end').splitlines())
        #ファイルに保存
        with open(self.setting_file, 'w') as f:
            json.dump(self.setting, f)
        #設定ウィンドウを閉じる
        self.setting_window.destroy()
        #エンジンの名前を表示するところを更新
        self.name_area.configure(text=self.setting['engine'])
        return

    def online_play(self):
        #止められるまで続ける
        self.stop = False
        while not self.stop:
            #状態を更新
            self.state_info.configure(text='state: CONNECT')
            #ゲームをプレイ
            self.play_game()
            time.sleep(10)
        #状態を更新
        self.state_info.configure(text='state: OFFLINE')
        return

    def offline_play(self):
        #self.make_offline_game_setting_window()
        board = Board()
        moves= []
        position_message = 'startpos moves'
        self.engine1 = USI_X_Engine(self.offline_game_engine['black'])
        self.engine2 = USI_X_Engine(self.offline_game_engine['white'])
        self.engine1.NewGame()
        self.engine2.NewGame()
        
        while True:
            
            if board.is_gameover() or (len(moves) > 1 and moves[-2] == moves[-1]):
                winner = board.return_winner()
                break
            
            self.update_board(board.return_sfen())
            self.color_area.configure(text='color: Black')
            self.time_area.configure(text='time: ' + str(self.offline_game_setting_dict['btime'] / 1000))
            time1 = time.time()
            move = self.engine1.think(position_message,
                               btime=self.offline_game_setting_dict['btime'],
                               wtime=self.offline_game_setting_dict['wtime'],
                               binc=self.offline_game_setting_dict['binc'], winc=self.offline_game_setting_dict['winc'],
                               byoyomi=self.offline_game_setting_dict['bbyoyomi'])
            self.message_area.configure(text=self.engine1.engine_message_list[-1])
            if 'resign' in move:
                winner = Board.WHITE
                break
            board.move_from_usix(move)
            moves += [move]
            position_message += (' ' + move)
            self.offline_game_setting_dict['btime'] -= int((time.time() - time1) * 1000)
            self.offline_game_setting_dict['btime'] += self.offline_game_setting_dict['binc']

            if board.is_gameover() or (len(moves) > 1 and moves[-2] == moves[-1]):
                winner = board.return_winner()
                break
            
            self.update_board(board.return_sfen())
            self.color_area.configure(text='color: White')
            self.time_area.configure(text='time: ' + str(self.offline_game_setting_dict['wtime'] / 1000))
            time1 = time.time()
            move = self.engine2.think(position_message,
                               btime=self.offline_game_setting_dict['btime'],
                               wtime=self.offline_game_setting_dict['wtime'],
                               binc=self.offline_game_setting_dict['binc'], winc=self.offline_game_setting_dict['winc'],
                               byoyomi=self.offline_game_setting_dict['wbyoyomi'])
            self.message_area.configure(text=self.engine2.engine_message_list[-1])
            if 'resign' in move:
                winner = Board.BLACK
                break
            board.move_from_usix(move)
            moves += [move]
            position_message += (' ' + move)
            self.offline_game_setting_dict['wtime'] -= int((time.time() - time1) * 1000)
            self.offline_game_setting_dict['wtime'] += self.offline_game_setting_dict['winc']
        
        self.update_board(board.return_sfen())
        self.show_result({BLACK: 'Black', WHITE: 'White', DRAW: 'Draw'}[winner])
        return

    def stop(self):
        #「止める」が押されたときに動く関数
        self.stop = True
        return

    def setting(self):
        #「設定」が押されたときに動く関数
        self.make_setting_window(self.setting)
        return
        
    def update_engine_message(self):
        #これはいらない
        while self.playing:
            if len(self.engine.engine_message_list) >= 1:
                self.message_area.configure(text=self.engine.engine_message_list[-1])
            time.sleep(1)
        return

    def play_game(self):
        #いろいろ初期化
        board = Board()
        #エンジンを読み込む
        self.engine = USI_X_Engine(self.Engine_path)
        self.engine.NewGame()
        self.playing = True
        #engine_message_thread = Thread(target=self.update_engine_message)
        #engine_message_thread.start()

        #接続・ログイン・対局待ちを行う
        self.client = Client(host=self.host)
        self.client.login(self.player_info[0], self.player_info[1])
        summary = self.client.wait()
        
        #承諾し、Boardを表示する
        self.client.agree()
        self.update_board(board.return_sfen())

        #自分の手番を取得
        color = summary['color']
        #エンジンに送り付けるpositionコマンドの準備
        self.to_engine_message = summary['position']
        #自分の残り持ち時間を取得
        self.my_time = summary['time']['total']
        #黒番なら行動
        if color == 'black':
            #更新
            self.color_area.configure(text='color: Black')
            self.window.update()
            #コマンドを用意 & エンジンに送信
            move = self.engine.think(self.to_engine_message, btime=self.my_time * 1000, wtime=60000,
                                     binc=summary['time']['inc'] * 1000, winc=summary['time']['inc'] * 1000, byoyomi=0)
            self.message_area.configure(text=self.engine.engine_message_list[-1])
            #boardに反映
            board.move_from_usix(move)
            #手を送信 & 消費時間を取得
            m, t = self.client.send_move(move, color)
            #持ち時間の管理
            self.my_time -= t
            self.my_time += summary['time']['inc']
            #positionコマンドを更新
            self.to_engine_message += (' ' + move)

        else:
            #白番では行動しない
            #更新は行う
            self.color_area.configure(text='color: White')
        
        #時間を表示 & windowの更新
        self.time_area.configure(text='time: ' + str(self.my_time))
        self.window.update()

        #メインループ・対局が終わるまで
        while True:
            #windowを更新
            self.update_board(board.return_sfen())
            
            #相手の番
            #相手の手を取得
            move, t = self.client.get_move()
            #終局したか？
            if move == 'end':
                #終局したらループから抜ける
                break
            #相手の手を反映
            board.move_from_usix(move)
            self.to_engine_message +=  (' ' + move)
            #相手の番終わり

            # windowを更新
            self.update_board(board.return_sfen())

            #自分の番
            #goコマンドを準備 & 送信
            if color == 'black':
                btime = self.my_time * 1000
                wtime = 60000
            else:
                btime = 60000
                wtime = self.my_time * 1000
            move = self.engine.think(self.to_engine_message, btime=btime, wtime=wtime,
                                               binc=summary['time']['inc'] * 1000, winc=summary['time']['inc'] * 1000, byoyomi=0)
            #windowに反映
            self.message_area.configure(text=self.engine.engine_message_list[-1])
            #特殊な手の処理を行う
            if 'resign' in move:
                self.client.resign()
                break
            elif 'pass' in move:
                #boardに反映
                board.move_from_usix('pass')
                #手を送信
                m, t = self.client.send_move('pass', color)
            else:
                #boardに反映
                board.move_from_usix(move)
                #手を送信
                m, t = self.client.send_move(move, color)
            #終局したか？
            if m == 'end':
                #終局したらループから抜ける
                break
            #時間の管理
            self.my_time -= t
            self.my_time += summary['time']['inc']
            #positionコマンドを更新
            self.to_engine_message += (' ' + move)
            #windowをアップデート
            self.time_area.configure(text='time: ' + str(self.my_time))
            self.window.update()
            #自分の番終わり

        self.playing = False
        #engine_message_thread.join()
        #windowを更新
        self.update_board(board.return_sfen())
        #ログアウトを試す
        try:
            self.client.logout()
        except:
            pass
        return


if __name__ == '__main__':
    simple_othello_gui = main()
    simple_othello_gui.window.mainloop()
    #input()
