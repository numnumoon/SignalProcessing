import tkinter as tk

# -------------------- 共通のボタンクラス --------------------


class BaseButton(tk.Button):
    """ボタンの共通基底クラス"""

    def __init__(self, parent, text, command=None):
        super().__init__(parent, text=text, command=self.on_click)
        self.custom_command = command  # 外部から渡される関数

    def on_click(self):
        """ボタンがクリックされたときの処理"""
        if self.custom_command:
            self.custom_command()


# -------------------- 各ボタンのクラス --------------------


class PrintButton(BaseButton):
    """メッセージを表示するボタン"""

    def __init__(self, parent):
        super().__init__(parent, text="Print", command=self.print_message)

    def print_message(self):
        print("PrintButton clicked!")


class ColorChangeButton(BaseButton):
    """背景色を変更するボタン"""

    def __init__(self, parent, target_widget):
        self.target_widget = target_widget
        super().__init__(parent, text="Change Color", command=self.change_color)

    def change_color(self):
        """ウィンドウの背景色を変更"""
        self.target_widget.config(bg="lightblue")


class ExitButton(BaseButton):
    """アプリを終了するボタン"""

    def __init__(self, parent):
        super().__init__(parent, text="Exit", command=self.exit_app)

    def exit_app(self):
        """アプリを終了"""
        print("Exiting Application...")
        self.master.quit()
