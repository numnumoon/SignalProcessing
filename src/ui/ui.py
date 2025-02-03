import tkinter as tk

from ui_parts import *


class ButtonGridFrame(tk.Frame):
    """複数のボタンを管理するフレーム"""

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        """ボタンを作成して配置"""
        self.buttons = [
            PrintButton(self),
            ColorChangeButton(self, self.parent),
            ExitButton(self),
        ]

        # グリッドにボタンを配置
        for i, btn in enumerate(self.buttons):
            btn.grid(row=0, column=i, padx=5, pady=5)


class MainGUI(tk.Tk):
    """メインのGUI管理クラス"""

    def __init__(self):
        super().__init__()
        self.title("Modular Tkinter GUI")
        self.geometry("400x200")
        self.init_ui()

    def init_ui(self):
        """UIの初期化"""
        self.button_frame = ButtonGridFrame(self)
        self.button_frame.pack(expand=True, fill="both", padx=10, pady=10)


# -------------------- アプリ起動 --------------------

if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()
