from Board_to_sfen import board_to_sfen
from USI_X_Engine import USI_X_Engine
from GUI_v1 import Simple_GUI as GUI
from threading import Thread
from cliant import Cliant
import creversi as reversi
import time
import json

class main(GUI):
    def __init__(self):
        super().__init__()
        self.setting_file = 'setting.json'
        self.engine = USI_X_Engine()
        self.reset()

    def reset(self):
        with open(self.setting_file, 'r') as f:
            self.setting = json.load(f)
        self.host = self.setting['host']
        self.player_info = self.setting['player_info']
        self.engine.Engine_path = self.setting['engine']
        self.name_area.configure(text=self.engine.Engine_path)
        return

    def graph_test(self):
        import numpy.random as R
        scores = list(range(-30, 60))
        #scores = R.randint(-60, 60, 30)
        self.plot_graph(scores)
        return

    def reset_setting(self):
        d = {'host': '127.0.0.1', 'player_info': ['usix_test', '1234'], 'engine': 'random_kun.bat'}
        with open(self.setting_file, 'w') as f:
            json.dump(d, f)
        try:
            self.setting_window.destroy()
        except:
            pass
        return

    def save_setting(self):
        self.setting['host'] = ''.join(self.host_input.get('1.0', 'end').splitlines())
        self.setting['engine'] = ''.join(self.engine_input.get('1.0', 'end').splitlines())
        self.setting['player_info'][0] = ''.join(self.player_name_input.get('1.0', 'end').splitlines())
        self.setting['player_info'][1] = ''.join(self.password_input.get('1.0', 'end').splitlines())
        with open(self.setting_file, 'w') as f:
            json.dump(self.setting, f)
        self.setting_window.destroy()
        return

    def online_play(self):
        self.stop = False
        while not self.stop:
            self.state_info.configure(text='state: CONNECT')
            self.play_game()
            time.sleep(10)
        self.state_info.configure(text='state: OFFLINE')
        return

    def stop(self):
        self.stop = True
        return

    def setting(self):
        self.make_setting_window(self.setting)
        
    def update_engine_message(self):
        while self.playing:
            if len(self.engine.engine_message_list) >= 1:
                self.message_area.configure(text=self.engine.engine_message_list[-1])
            time.sleep(1)
        return

    def play_game(self):
        board = reversi.Board()
        self.engine.NewGame()
        self.playing = True
        #engine_message_thread = Thread(target=self.update_engine_message)
        #engine_message_thread.start()

        self.cliant = Cliant(host=self.host)
        self.cliant.login(self.player_info[0], self.player_info[1])
        summary = self.cliant.wait()
        
        self.cliant.agree()
        self.update_board(board_to_sfen(board, 1))
        
        color = summary['color']
        self.to_engine_message = 'position ' + summary['position']
        self.my_time = summary['time']['total']
        if color == 'black':
            self.color_area.configure(text='color: Black')
            self.window.update()
            self.engine.command(self.to_engine_message)
            go_message = 'go btime ' + str(self.my_time * 1000) + ' wtime 60000'
            move = self.engine.command(go_message)
            move = self.engine.read('bestmove')
            self.message_area.configure(text=self.engine.engine_message_list[-1])
            
            move = move[9] + move[10]
            board.move_from_str(move)
            m, t = self.cliant.send_move(move, color)
            self.my_time -= t
            self.my_time += summary['time']['inc']
            self.to_engine_message += (' ' + move)

        else:
            self.color_area.configure(text='color: White')
        
        self.time_area.configure(text='time: ' + str(self.my_time))
        self.window.update()
        
        while True:
            self.update_board(board_to_sfen(board, 1))
            #相手の番
            move, t = self.cliant.get_move()
            if move == 'end':
                break
            board.move_from_str(move)
            self.to_engine_message +=  (' ' + move)
            #相手の番終わり
            
            self.update_board(board_to_sfen(board, 1))
            #自分の番
            self.engine.command(self.to_engine_message)
            if color == 'black':
                go_message = 'go btime ' + str(self.my_time) + ' wtime 60000'
            else:
                go_message = 'go btime 60000 wtime ' + str(self.my_time)
            self.engine.command(go_message)
            move = self.engine.read('bestmove')
            self.message_area.configure(text=self.engine.engine_message_list[-1])
            if 'resign' in move:
                pass
            if 'pass' in move:
                pass
            move = move[9] + move[10]
            board.move_from_str(move)
            m, t = self.cliant.send_move(move, color)
            if m == 'end':
                break
            self.my_time -= t
            self.my_time += summary['time']['inc']
            self.to_engine_message += (' ' + move)
            self.time_area.configure(text='time: ' + str(self.my_time))
            self.window.update()
            #自分の番終わり
        self.playing = False
        engine_message_thread.join()
        self.update_board(board_to_sfen(board, 1))
        try:
            self.cliant.logout()
        except:
            pass
        return


if __name__ == '__main__':
    simple_othello_gui = main()
    input()
