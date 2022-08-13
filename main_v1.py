from USI_X_Engine import USI_X_Engine
from GUI_v1 import Simple_GUI as GUI
from snail_reversi.Board import Board
from threading import Thread
from cliant import Cliant
import time
import json

class main(GUI):
    def __init__(self):
        super().__init__()
        #設定を保存するファイル
        self.setting_file = 'setting.json'
        #エンジンの型を用意
        self.engine = USI_X_Engine()
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
        self.engine.Engine_path = self.setting['engine']
        #エンジンの名前を表示するところを更新
        self.name_area.configure(text=self.engine.Engine_path)
        return

    def graph_test(self):
        #グラフ機能のテスト
        import numpy.random as R
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
        self.engine.NewGame()
        self.playing = True
        #engine_message_thread = Thread(target=self.update_engine_message)
        #engine_message_thread.start()

        #接続・ログイン・対局待ちを行う
        self.cliant = Cliant(host=self.host)
        self.cliant.login(self.player_info[0], self.player_info[1])
        summary = self.cliant.wait()
        
        #承諾し、Boardを表示する
        self.cliant.agree()
        self.update_board(board.return_sfen())

        #自分の手番を取得
        color = summary['color']
        #エンジンに送り付けるpositionコマンドの準備
        self.to_engine_message = 'position ' + summary['position']
        #自分の残り持ち時間を取得
        self.my_time = summary['time']['total']
        #黒番なら行動
        if color == 'black':
            #更新
            self.color_area.configure(text='color: Black')
            self.window.update()
            #positionコマンドをエンジンに送信
            self.engine.command(self.to_engine_message)
            #goコマンドを用意 & エンジンに送信
            go_message = 'go btime ' + str(self.my_time * 1000) + ' wtime 60000'
            self.engine.command(go_message)
            #bestmoveの取得・エンジンからのメッセージを表示
            move = self.engine.read('bestmove')
            self.message_area.configure(text=self.engine.engine_message_list[-1])
            #必要な情報を取り出す
            move = move[9] + move[10]
            #boardに反映
            board.move_from_usix(move)
            #手を送信 & 消費時間を取得
            m, t = self.cliant.send_move(move, color)
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
            move, t = self.cliant.get_move()
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
            #positionコマンドを送信
            self.engine.command(self.to_engine_message)
            #goコマンドを準備 & 送信
            if color == 'black':
                go_message = 'go btime ' + str(self.my_time) + ' wtime 60000'
            else:
                go_message = 'go btime 60000 wtime ' + str(self.my_time)
            self.engine.command(go_message)
            #bestmoveを取得 & windowに反映
            move = self.engine.read('bestmove')
            self.message_area.configure(text=self.engine.engine_message_list[-1])
            #特殊な手の処理を行う
            if 'resign' in move:
                self.cliant.resign()
                break
            elif 'pass' in move:
                #boardに反映
                board.move_from_usix('pass')
                #手を送信
                m, t = self.cliant.send_move('pass', color)
            else:
                #必要な情報のみ取得
                move = move[9] + move[10]
                #boardに反映
                board.move_from_usix(move)
                #手を送信
                m, t = self.cliant.send_move(move, color)
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
            self.cliant.logout()
        except:
            pass
        return


if __name__ == '__main__':
    simple_othello_gui = main()
    input()
