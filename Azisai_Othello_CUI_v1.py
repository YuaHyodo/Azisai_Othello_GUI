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
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEME5NT. IN NO EVENT SHALL THE
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
from snail_reversi.Board import Board
from threading import Thread
from client import Client
import time
import json

class main:
    def __init__(self):
        self.setting_file = 'setting.json'
        self.setting()

    def load_setting(self):
        with open(self.setting_file, 'r') as f:
            self.setting = json.load(f)
        self.host = self.setting['host']
        self.player_info = self.setting['player_info']
        self.Engine_path = self.setting['engine']
        return

    def setting(self):
        if input('load_setting_file(y / n):') == 'y':
            self.load_setting()
            return
        self.Engine_path = input('Engine Path:')
        self.host = input('host:')
        self.player_info = [input('username:'), input('password:')]
        return

    def online_play(self):
        board = Board()
        self.engine = USI_X_Engine(self.Engine_path)
        self.engine_info_get = True
        self.engine.NewGame()

        self.client = Client(host=self.host)
        self.client.login(self.player_info[0], self.player_info[1])
        summary = self.client.wait()

        self.client.agree()
        color = summary['color']

        self.to_engine_message = summary['position']

        self.my_time = summary['time']['total']

        if color == 'black':

            move = self.engine.think(self.to_engine_message, btime=self.my_time * 1000, wtime=60000,
                                     binc=summary['time']['inc'] * 1000, winc=summary['time']['inc'] * 1000, byoyomi=0)

            board.move_from_usix(move)

            m, t = self.client.send_move(move, color)

            self.my_time -= t
            self.my_time += summary['time']['inc']

            self.to_engine_message += (' ' + move)

        while True:
            move, t = self.client.get_move()

            if move == 'end':
                break

            board.move_from_usix(move)
            self.to_engine_message +=  (' ' + move)

            if color == 'black':
                btime = self.my_time * 1000
                wtime = 60000
            else:
                btime = 60000
                wtime = self.my_time * 1000
            move = self.engine.think(self.to_engine_message, btime=btime, wtime=wtime,
                                               binc=summary['time']['inc'] * 1000, winc=summary['time']['inc'] * 1000, byoyomi=0)

            if 'resign' in move:
                self.client.resign()
                break
            elif 'pass' in move:
                board.move_from_usix('pass')
                m, t = self.client.send_move('pass', color)
            else:
                board.move_from_usix(move)
                m, t = self.client.send_move(move, color)
                
            if m == 'end':
                break
            
            self.my_time -= t
            self.my_time += summary['time']['inc']

            self.to_engine_message += (' ' + move)

        try:
            self.client.logout()
        except:
            pass
        return

    def offline_play(self):
        self.offline_game_setting_dict = {}
        engine1_path = input('engine1:')
        engine2_path = input('engine2:')
        self.engine1 = USI_X_Engine(engine1_path)
        self.engine2 = USI_X_Engine(engine2_path)
        self.engine1.info_get = True
        self.engine2.info_get = True
        
        self.offline_game_setting_dict['btime'] = int(input('btime:'))
        self.offline_game_setting_dict['wtime'] = int(input('wtime:'))
        self.offline_game_setting_dict['binc'] = int(input('binc:'))
        self.offline_game_setting_dict['winc'] = int(input('winc:'))
        self.offline_game_setting_dict['bbyoyomi'] = int(input('bbyoyomi:'))
        self.offline_game_setting_dict['wbyoyomi'] = int(input('wbyoyomi:'))

        games = int(input('games:'))
        wins = {'black': 0, 'draw': 0, 'white': 0}
        for i in range(games):
            self.engine1.NewGame()
            self.engine2.NewGame()
            board = Board()
            moves = []
            position_message = 'startpos moves'
            print(i, '/', games)
            print('wins:', wins)
            while True:
                if board.is_gameover() or (len(moves) > 1 and moves[-2] == moves[-1]):
                    winner = board.return_winner()
                    break
                
                time1 = time.time()
                move = self.engine1.think(position_message,
                               btime=self.offline_game_setting_dict['btime'],
                               wtime=self.offline_game_setting_dict['wtime'],
                               binc=self.offline_game_setting_dict['binc'], winc=self.offline_game_setting_dict['winc'],
                               byoyomi=self.offline_game_setting_dict['bbyoyomi'])
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
                
                time1 = time.time()
                move = self.engine2.think(position_message,
                               btime=self.offline_game_setting_dict['btime'],
                               wtime=self.offline_game_setting_dict['wtime'],
                               binc=self.offline_game_setting_dict['binc'], winc=self.offline_game_setting_dict['winc'],
                               byoyomi=self.offline_game_setting_dict['wbyoyomi'])
                if 'resign' in move:
                    winner = Board.BLACK
                    break
                board.move_from_usix(move)
                moves += [move]
                position_message += (' ' + move)
                self.offline_game_setting_dict['wtime'] -= int((time.time() - time1) * 1000)
                self.offline_game_setting_dict['wtime'] += self.offline_game_setting_dict['winc']
            wins[{BLACK: 'black', WHITE: 'white', DRAW: 'draw'}[winner]] += 1
        print('')
        print('result')
        print('black:', engine1_path)
        print('white:', engine2_path)
        print('wins:', wins)
        return

if __name__ == '__main__':
    cui = main()
    while True:
        command = input('command:')
        if 'online' in command:
            games = int(input('games:'))
            for i in range(games):
                cui.online_play()
        if 'offline' in command:
            cui.offline_play()
        if 'setting' in command:
            cui.setting()
        if 'quit' in command:
            break
