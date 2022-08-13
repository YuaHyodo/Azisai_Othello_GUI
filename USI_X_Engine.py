"""
USI-X対応エンジンを自分のプログラムで動かす際などにつかう

とりあえず動けばいい
"""
import subprocess as sp

class USI_X_Engine():
    def __init__(self):
        self.Engine_path = ''#エンジンファイルのパス
        self.options = []#ここにsetoptionコマンドを入れておけば自動でセットする
        self.print_info = True#infoコマンドの情報を表示するか？

    def command(self, word):#コマンドを送る
        self.engine.stdin.write(word + '\n')
        return

    def read(self, word):#コマンドを読む
        while True:
            line = self.engine.stdout.readline()
            if word in line:
                print(line)
                self.engine_message_list.append(line)
                break
            if 'info' in line and self.print_info:
                print(line)
                self.engine_message_list.append(line)
        return line

    def setup(self):#エンジンの起動とかをする
        self.engine_message_list = []
        self.engine = sp.Popen(self.Engine_path, stdin=sp.PIPE, stdout=sp.PIPE,
                          universal_newlines=True, bufsize=1)
        self.command('usi')
        self.read('usiok')
        for i in range(len(self.options)):#エンジンを設定する
            self.command(self.options[i])
        return

    def NewGame(self):#セットアップ等々をする
        self.setup()
        self.command('isready')
        self.read('readyok')
        self.command('usinewgame')
        return

    def go(self, sfen, moves, time_num, use_sfen=False):#メイン
        """
        sfen: sfenがはいる。sfenを使わないならuse_sfenをFalseのままにして
        moves: USI-Xオセロ版のmoveで表された手順
        time_num: 制限時間(秒)
        """
        m = ''
        for move in moves:
            m += ' '
            m += move
        if use_sfen:
            self.command('position sfen ' + sfen + ' moves' + m)
        else:
            self.command('position startpos moves' + m)
        
        to_engine = 'go btime 1000 wtime 1000 byoyomi ' + str(time_num * 1000)
        self.command(to_engine)
        from_engine = self.read('bestmove')
        if 'resign' in from_engine:
            return 'resign'
        elif 'pass' in from_engine:
            return 'pass'
        move = from_engine[9] + from_engine[10]
        return move

    def Kill(self):#止める
        self.command('quit')
        return

if __name__ == '__main__':
    pass
