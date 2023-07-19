"""
This file is part of Azisai_Othello_GUI

Copyright (c) 2023 YuaHyodo

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

from USI_X_Engine_Bridge.ver2 import USI_X_Engine_Bridge as USI_X_Engine
from snail_reversi.Board import BLACK, WHITE, DRAW, PASS, Board
import random
import argparse

def gen_random_sfen(num):
    board = Board()
    for i in range(num*2):
        move = random.choice(board.gen_legal_moves())
        board.move_from_usix(move)
    return board.return_sfen()

class AzisaiOthelloCUI2:
    def __init__(self, engine, opt, byoyomi, opening=None, output_file=None, engine_log=[None, None]):
        self.engine_path = engine
        self.opt = opt
        self.byoyomi = byoyomi
        self.opening_file = opening
        self.output_file = output_file
        self.engine_log = engine_log

    def load_opening(self):
        if self.opening_file is None:
            #通常の初期局面開始
            return '---------------------------OX------XO---------------------------B1'
        if 'r_' in self.opening_file and '.' not in self.opening_file:
            #ランダムにN手行動した局面から開始
            return gen_random_sfen(int(self.opening_file.split('_')[1]))
        with open(self.opening_file, 'r') as f:
            r = f.read()
        return random.choice(r.splitlines())

    def setup_engine(self):
        self.engine = []
        for i in range(2):
            self.engine.append(USI_X_Engine(self.engine_path[i], log_file=self.engine_log[i]))
            for k, v in self.opt[i].items():
                self.engine[-1].setoption(k, v)
        return

    def save(self, sfen, moves, winner):
        if self.output_file is None:
            return
        output = 'opening {} winner {} moves'.format(sfen, winner)
        for move in moves:
            output = output + ' ' + move
        k = '\n'#改行
        with open(self.output_file, 'a') as f:
            f.write(output + k)
        return

    def game(self, opening_sfen, black, white):
        moves = []
        board = Board(sfen=opening_sfen)
        opening = 'sfen {} moves'.format(opening_sfen)
        for i in range(60):
            self.engine[black].send('position {}'.format(opening))
            self.engine[black].send('go btime 0 wtime 0 binc 0 winc 0 byoyomi {}'.format(self.byoyomi[black]))
            move = self.engine[black].get_move(score=False)
            if move == 'resign':
                moves.append(move)
                winner = 'W'
                break
            board.move_from_usix(move)
            moves.append(move)
            if (len(moves) > 1 and moves[-1] == moves[-2]) or board.is_gameover():
                winner = board.return_winner()
                if winner == DRAW:
                    winner = 'D'
                elif winner == BLACK:
                    winner = 'B'
                else:
                    winner = 'W'
                break
            opening = opening + ' ' + move
            
            self.engine[white].send('position {}'.format(opening))
            self.engine[white].send('go btime 0 wtime 0 binc 0 winc 0 byoyomi {}'.format(self.byoyomi[white]))
            move = self.engine[white].get_move(score=False)
            if move == 'resign':
                winner = 'B'
                moves.append(move)
                break
            board.move_from_usix(move)
            moves.append(move)
            if (len(moves) > 1 and moves[-1] == moves[-2]) or board.is_gameover():
                winner = board.return_winner()
                if winner == DRAW:
                    winner = 'D'
                elif winner == BLACK:
                    winner = 'B'
                else:
                    winner = 'W'
                break
            opening = opening + ' ' + move
        self.save(opening_sfen, moves, winner)
        return winner

    def main(self, set_num):
        self.setup_engine()
        wins = {'engine1_win': 0, 'engine2_win': 0, 'draw': 0}
        for set_n in range(set_num):
            print('set: {} / {} |'.format(set_n, set_num), wins)
            opening = self.load_opening()#1つの局面に対して表と裏の2回行う
            #表
            [i.newgame() for i in self.engine]
            w = self.game(opening, 0, 1)
            wins[{'B': 'engine1_win', 'W': 'engine2_win', 'D': 'draw'}[w]] += 1
            #裏
            [i.newgame() for i in self.engine]
            w = self.game(opening, 1, 0)
            wins[{'W': 'engine1_win', 'B': 'engine2_win', 'D': 'draw'}[w]] += 1
        [i.stop() for i in self.engine]
        print('result:', wins)
        return wins

p = argparse.ArgumentParser()
p.add_argument('engine1', type=str)
p.add_argument('engine2', type=str)

p.add_argument('--engine_options1', type=str, default='')
p.add_argument('--engine_options2', type=str, default='')

p.add_argument('--set_num', type=int, default=1)
p.add_argument('--byoyomi', type=int, default=3000)
p.add_argument('--byoyomi_1', type=int, default=0)
p.add_argument('--byoyomi_2', type=int, default=0)
p.add_argument('--opening', type=str, default='')
p.add_argument('--output_file', type=str, default='')

p.add_argument('--engine_log1', type=str, default='')
p.add_argument('--engine_log2', type=str, default='')
args = p.parse_args()

opt = [{}, {}]
if args.engine_options1.split(',')[0] != '':
    opt[0] = {i.split(':')[0]: i.split(':')[1] for i in args.engine_options1.split(',')}
if args.engine_options2.split(',')[0] != '':
    opt[1] = {i.split(':')[0]: i.split(':')[1] for i in args.engine_options2.split(',')}

if args.byoyomi_1 > 0 and args.byoyomi_2 > 0:
    byoyomi = [args.byoyomi_1, args.byoyomi_2]
else:
    byoyomi = [args.byoyomi, args.byoyomi]

opening = args.opening if args.opening != '' else None
output_file = args.output_file if args.output_file != '' else None

engine_log = [args.engine_log1 if args.engine_log1 != '' else None,
              args.engine_log2 if args.engine_log2 != '' else None]

cui = AzisaiOthelloCUI2([args.engine1, args.engine2], opt, byoyomi, opening=opening,
                        output_file=output_file, engine_log=engine_log)
cui.main(args.set_num)
