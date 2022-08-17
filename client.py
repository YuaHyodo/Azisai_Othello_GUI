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

from threading import Thread
import socket
import time

k = '\n'

class Cliant:
    def __init__(self, host, port=4081):
        self.host = host
        self.port=port
        self.buf_size = 1024
        self.keep_connect = False

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.keep_connact = True
        keep_connect_thread = Thread(target=self.keep_connect)
        keep_connect_thread.start()
        return

    def keep_connect(self):
        while self.keep_connect:
            self.send('')
            time.sleep(10)
        

    def send(self, message):
        if k not in message:
            message += k
        self.socket.send(message.encode('utf-8'))
        return

    def recv(self):
        message = self.socket.recv(self.buf_size).decode('utf-8')
        return str(message)

    def login(self, name, password):
        self.connect()
        self.send('LOGIN ' + name + ' ' + password)
        while True:
            message = self.recv()
            if 'LOGIN' in message:
                break
        if 'incorrect' in message:
            raise ValueError('LOGIN failed')
        return

    def logout(self):
        self.send('LOGOUT')
        self.keep_connect = False
        self.keep_connect_thread.join()
        self.socket.close()
        return

    def agree(self):
        self.send('AGREE')
        while True:
            m = self.recv()
            if 'START' in m:
                break
            if 'REJECT' in m:
                break
        return

    def resign(self):
        self.send('RESIGN')
        while True:
            m = self.recv()
            if '#' in m:
                break
        return

    def wait(self):
        while True:
            message = self.recv()
            if 'Game_Summary' in message:
                break
        return self.Parse_summary(message)

    def Parse_summary(self, summary):
        lines = summary.splitlines()
        output = {'position': 'startpos moves', 'time': {'total': 0, 'inc': 0}, 'color': 0}
        for L in lines:
            if 'Your_Turn:' in L:
                if '+' in L:
                    output['color'] = 'black'
                else:
                    output['color'] = 'white'
            if 'Total_Time:' in L:
                output['time']['total'] = int(L[11:])
            if 'Increment:' in L:
                output['time']['inc'] = int(L[10:])
        return output

    def get_move(self):
        end = ['#ILLEGAL_MOVE', '#RESIGN', '#TIME_UP', '#DOUBLE_PASS', '#ABNORMAL', '#WIN', '#DRAW', '#LOSE']
        t = 0
        while True:
            m = self.recv()
            for e in end:
                if e in m:
                    m = 'end'
                    break
            if m == 'end':
                break
            if 'PASS' in m:
                m = 'pass'
                break
            if ',T' in m:
                t = int(m[5:])
                m = m[1:3]
                break
        return m, t

    def send_move(self, usix_move, c):
        color = {'black': '+', 'white': '-'}[c]
        if usix_move == 'pass':
            self.send('PASS')
        else:
            self.send(color + usix_move)
        m, t = self.get_move()
        is_end =  (m == 'end')
        return is_end, t
