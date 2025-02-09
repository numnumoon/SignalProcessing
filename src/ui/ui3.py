import os

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from testdata import create_test_data


class ButtonComponent(tk.Button):
    """ボタンの設定を個別管理するためのクラス"""

    def __init__(self, master, text, xpos, ypos, width, height, command=None):
        super().__init__(master, text=text, command=command)
        self.place(x=xpos, y=ypos, width=width, height=height)


class EntryComponent(tk.Entry):
    """エントリーの設定を個別管理するためのクラス"""

    def __init__(self, master, text, xpos, ypos, width, height):
        super().__init__(master, textvariable=text)
        self.place(x=xpos, y=ypos, width=width, height=height)


class SliderComponent(tk.Scale):
    """スライドバーの設定を個別管理するためのクラス"""

    def __init__(self, master, xpos, ypos, min_value, max_value):
        super().__init__(master, orient="horizontal", from_=min_value, to=max_value)
        self.place(x=xpos, y=ypos)

    def get_value(self):
        return self.get()


class MatplotComponent:
    """読み込んだ3次元データをmatplotのfigureに変換するクラス"""

    def __init__(self, vol3d):
        self.vol3d = vol3d

    def create_figure(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.imshow(self.vol3d[0, :, :])
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.imshow(self.vol3d[:, 0, :])
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.imshow(self.vol3d[:, :, 0])
        return fig


class MainApp(tk.Frame):
    """GUIのメインクラス"""

    def __init__(self, master=None):
        super().__init__(master)
        master.geometry("1600x900")
        master.title("ソフトウェア")

        self.create_widgets()

        self.pack()

    def create_widgets(self):
        self.button = [
            ButtonComponent(
                self.master, "データ選択", 20, 20, 80, 20, self.select_folder
            ),
            ButtonComponent(
                self.master, "データ表示", 550, 20, 80, 20, self.display_data
            ),
        ]

        self.stringvar = tk.StringVar()
        self.entry1 = EntryComponent(self.master, self.stringvar, 100, 20, 450, 20)

        self.create_graph()

        self.image_slider = [
            SliderComponent(self.master, 1000, 620, 0, 100),  # time
            SliderComponent(self.master, 1000, 670, 0, 500),  # pos
            SliderComponent(self.master, 1000, 720, 0, 5000),  # range
        ]

    def create_graph(self):
        self.fig_canvas = FigureCanvasTkAgg(
            MatplotComponent(create_test_data()).create_figure()
        )
        self.toolbar = NavigationToolbar2Tk(self.fig_canvas, self.master)
        self.fig_canvas.get_tk_widget().place(x=10, y=100, width=1200, height=700)

    def select_folder(self):
        init_dir = os.path.abspath(os.path.dirname(__file__))
        folder_path = filedialog.askdirectory(initialdir=init_dir)
        if folder_path:
            self.stringvar.set(folder_path)

    def display_data(self):
        if self.stringvar.get():
            print("OK")
        else:  # todo:ここのエラーチェックをもう少しまともに エラーチェックとか
            messagebox.showinfo("error", "Pathが選択されていません。")


def main():
    root = tk.Tk()
    app = MainApp(master=root)

    # ウィンドウサイズの変更禁止
    root.resizable(False, False)
    app.mainloop()


if __name__ == "__main__":
    main()
