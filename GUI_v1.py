from copy import deepcopy
from tkinter import*

class Simple_GUI:
    def __init__(self):
        self.area_A_bg = 'blue'
        self.area_A_button_color = ['gray', 'black']
        self.info_area1_bg_color = ['black', 'darkblue', 'yellow', 'purple']
        self.info_area1_fg_color = ['gold', 'black', 'yellow']
        self.info_area2_bg = 'skyblue'
        self.graph_color = 'orange'
        self.init_window()

    def init_window(self):
        self.title = 'Azisai_Othello_GUI(v1)'
        self.size = '500x500'
        self.window = Tk()
        self.window.title(self.title)
        self.window.geometry(self.size)

        self.area_A = Frame(self.window)#, width=500, height=20, bg=self.area_A_bg)
        self.Board_area = Frame(self.window)#, width=300, height=300)
        self.info_area1 = Frame(self.window)#, width=200, height=300)
        self.info_area2 = Frame(self.window)#, width=300, height=280)

        self.init_area_A()
        self.init_Board_area()
        self.init_info_area1()
        self.init_info_area2()
        """
        self.area_A.grid(column=0, row=0)
        self.Board_area.grid(column=0, row=1)
        self.info_area1.grid(column=1, row=1)
        """
        self.area_A.place(x=0, y=0, width=500, height=30)
        self.Board_area.place(x=0, y=30, width=320, height=320)
        self.info_area1.place(x=320, y=30, width=180, height=320)
        self.info_area2.place(x=0, y=350, width=500, height=150)
        self.window.update()
        return

    def init_area_A(self):
        """
        上にあるやつ
        """
        W = int(500 / 4)
        H = 30
        self.online_button = Button(self.area_A,
                                        text='connect',
                                        bg=self.area_A_button_color[0],
                                        fg=self.area_A_button_color[1],
                                        command=self.online_play)#,
                                        #width=W, height=H)
        self.stop_button = Button(self.area_A,
                                        text='stop',
                                        bg=self.area_A_button_color[0],
                                        fg=self.area_A_button_color[1],
                                        command=self.stop)#,
                                        #width=W, height=H)
        self.setting_button = Button(self.area_A,
                                        text='setting',
                                        bg=self.area_A_button_color[0],
                                        fg=self.area_A_button_color[1],
                                        command=self.setting)#,
                                        #width=W, height=H)
        self.state_info = Label(self.area_A, text='state: OFFLINE',
                                        bg=self.area_A_button_color[0],
                                        fg=self.area_A_button_color[1])
        #self.online_button.grid(column=0, row=0)
        #self.stop_button.grid(column=1, row=0)
        #self.setting_button.grid(column=2, row=0)
        self.online_button.place(x=0, y=0, width=W, height=H)
        self.stop_button.place(x=W, y=0, width=W, height=H)
        self.setting_button.place(x=W * 2, y=0, width=W, height=H)
        self.state_info.place(x=W * 3, y=0, width=W, height=H)
        return

    def init_Board_area(self):
        W = 40
        H = 40
        self.sq = []
        D = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        for i in range(8):
            rank = []
            for j in range(8):
                rank.append(Button(self.Board_area, text=D[j] + str(i + 1),
                                 fg = 'red', bd=2, bg='green',
                                 relief='ridge'))#, width=W, height=H))
            self.sq.append(rank)
        for i in range(8):
            for j in range(8):
                #self.sq[i][j].grid(column=j, row=i)
                self.sq[i][j].place(x=j * W, y=i * H, width=W, height=H)
        return

    def init_info_area1(self):
        #エンジンの情報を表示
        self.name_area = Label(self.info_area1, text='engine_name',
                                   bg=self.info_area1_bg_color[1], fg=self.info_area1_fg_color[0],
                                   relief='ridge')
        self.time_area = Label(self.info_area1, text='time: 0',
                                 bg=self.info_area1_bg_color[3], fg=self.info_area1_fg_color[2],
                                 relief='ridge')
        self.color_area = Label(self.info_area1, text='color: None',
                                  bg=self.info_area1_bg_color[3], fg=self.info_area1_fg_color[2],
                                 relief='ridge')
        self.message_area = Label(self.info_area1, text='engine_message',
                                  bg=self.info_area1_bg_color[2], fg=self.info_area1_fg_color[1],
                                  relief='ridge')
        #self.name_area.grid(column=0, row=0)
        #self.message_area.grid(column=0, row=1)
        self.time_area.place(x=0, y=0, width=90, height=30)
        self.color_area.place(x=90, y=0, width=90, height=30)
        self.name_area.place(x=0, y=30, width=180, height=30)
        self.message_area.place(x=0, y=60, width=180, height=260)
        return

    def init_info_area2(self):
        self.graph_area = Canvas(self.info_area2, bg=self.info_area2_bg)
        self.graph_area.create_rectangle(0, 74, 500, 76, fill='darkblue')
        self.graph_area.place(x=0, y=0, width=500, height=150)
        return

    def plot_graph(self, values):
        moves = len(values)
        max_value = max(values)
        min_value = min(values)
        W = (500 / moves)
        for i in range(moves):
            H = int(50 * (values[i] / max([abs(max_value), abs(min_value)])))
            if H >= 75:
                self.graph_area.create_rectangle((W * i), H, (W * (i + 1)), 75, fill=self.graph_color)
            else:
                self.graph_area.create_rectangle((W * i), 75, (W * (i + 1)), (75 - H), fill=self.graph_color)
        self.window.update()
        return

    def online_play(self):
        pass

    def stop(self):
        pass

    def setting(self):
        pass

    def reset_setting(self):
        pass

    def save_setting(self):
        pass

    def update_board(self, sfen):
        color_d = {'O': 'white', 'X': 'black', '-': 'green'}
        for i in range(8):
            for j in range(8):
                self.sq[i][j].configure(bg=color_d[sfen[(i * 8) + j]])
        return

    def make_setting_window(self, change):
        self.setting_window = Tk()
        self.setting_window.title('Azisai_Othello_GUI_Setting')
        self.setting_window.geometry('300x300')
        self.after_change_setting = change.copy()
        
        self.text1 = Label(self.setting_window, text='host')
        self.host_input = Text(self.setting_window)

        self.text2 = Label(self.setting_window, text='engine')
        self.engine_input = Text(self.setting_window)

        self.text3 = Label(self.setting_window, text='player_name')
        self.player_name_input = Text(self.setting_window)

        self.text4 = Label(self.setting_window, text='password')
        self.password_input = Text(self.setting_window)

        self.reset_setting_button = Button(self.setting_window, text='reset',
                                                bg='red', fg='black', relief='ridge', command=self.reset_setting)

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
