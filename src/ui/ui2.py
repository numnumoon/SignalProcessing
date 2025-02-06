import tkinter as tk
from tkinter import messagebox


class SliderObserver:
    """スライダーの変更を監視するオブザーバーの基底クラス"""

    def update(self, value_list):
        """スライダーの値が変更されたときに呼ばれる"""
        raise NotImplementedError("update() を実装してください")


class SliderSubject:
    """スライダーの値変更を通知するサブジェクト"""

    def __init__(self):
        self.observers = []  # 登録されたオブザーバーのリスト

    def add_observer(self, observer):
        """オブザーバーを追加"""
        self.observers.append(observer)

    def remove_observer(self, observer):
        """オブザーバーを削除"""
        self.observers.remove(observer)

    def notify_observers(self, value_list):
        """すべてのオブザーバーに現在のスライダー値を通知"""
        for observer in self.observers:
            observer.update(value_list)


class AppLabel(SliderObserver):
    """テキストを表示し、スライダーの変更を受け取るクラス"""

    def __init__(self, parent):
        self.label = tk.Label(parent, text="ボタンを押してください", font=("Arial", 14))
        self.label.pack(pady=10)

    def update(self, value_list):
        """スライダーの変更通知を受け取り、ラベルを更新"""
        self.label.config(text=f"スライダー値: {value_list}")


class AppButton:
    """ボタンを表すクラス"""

    def __init__(self, parent, text, command):
        self.command = command
        self.button = tk.Button(
            parent, text=text, command=self.on_click, font=("Arial", 12)
        )
        self.button.pack(pady=5)

    def on_click(self):
        """ボタンが押されたときにコマンドを実行"""
        if self.command:
            self.command.execute()


class AppSlider:
    """スライダーとその調整ボタンを含むクラス"""

    def __init__(self, parent, label_text, subject, min_value=0, max_value=1000):
        self.subject = subject  # オブザーバー管理クラス
        self.min_value = min_value
        self.max_value = max_value

        self.frame = tk.Frame(parent)
        self.frame.pack(pady=5)

        self.label = tk.Label(self.frame, text=label_text, font=("Arial", 12))
        self.label.pack(side=tk.LEFT, padx=5)

        self.scale = tk.Scale(
            self.frame,
            from_=min_value,
            to=max_value,
            orient=tk.HORIZONTAL,
            length=200,
            command=self.on_value_change,
        )
        self.scale.pack(side=tk.LEFT)

        # 増減ボタンを追加
        self.button_frame = tk.Frame(parent)
        self.button_frame.pack(pady=2)

        self.create_adjust_button("-10", -10)
        self.create_adjust_button("-1", -1)
        self.create_adjust_button("+1", 1)
        self.create_adjust_button("+10", 10)

    def create_adjust_button(self, text, delta):
        """スライダーの値を増減するボタンを作成"""
        btn = tk.Button(
            self.button_frame,
            text=text,
            command=lambda: self.adjust_value(delta),
            width=3,
        )
        btn.pack(side=tk.LEFT, padx=2)

    def adjust_value(self, delta):
        """スライダーの値を増減"""
        new_value = self.scale.get() + delta
        self.scale.set(
            max(self.min_value, min(self.max_value, new_value))
        )  # 範囲内に制限
        self.on_value_change(None)  # スライダーの変更を通知

    def on_value_change(self, _):
        """スライダーの値が変わったらオブザーバーに通知"""
        self.subject.notify_observers(
            [slider.get_value() for slider in self.subject.sliders]
        )

    def get_value(self):
        """スライダーの現在値を取得"""
        return self.scale.get()


class ButtonCommand:
    """ボタンのコマンド基底クラス"""

    def __init__(self, label, sliders):
        self.label = label  # ラベルへの参照を保持
        self.sliders = sliders  # スライダーリストを保持

    def execute(self):
        """ボタンが押された際の処理（サブクラスで実装）"""
        raise NotImplementedError("execute() を実装してください")


class ButtonACommand(ButtonCommand):
    """A ボタンの処理"""

    def execute(self):
        values = [slider.get_value() for slider in self.sliders]
        messagebox.showinfo(
            "A ボタン", f"A ボタンが押されました\nスライダー値: {values}"
        )
        self.label.update(values)


class ButtonBCommand(ButtonCommand):
    """B ボタンの処理"""

    def execute(self):
        values = [slider.get_value() for slider in self.sliders]
        messagebox.showinfo(
            "B ボタン", f"B ボタンが押されました\nスライダー値: {values}"
        )
        self.label.update(values)


class ButtonCCommand(ButtonCommand):
    """C ボタンの処理"""

    def execute(self):
        values = [slider.get_value() for slider in self.sliders]
        messagebox.showinfo(
            "C ボタン", f"C ボタンが押されました\nスライダー値: {values}"
        )
        self.label.update(values)


class MainApp:
    """GUIアプリのメインクラス"""

    def __init__(self, root):
        self.root = root
        self.root.title("サンプルGUIアプリ")
        self.root.geometry("450x450")

        # オブザーバー管理クラス
        self.slider_subject = SliderSubject()

        # ラベルの作成（オブザーバーとして登録）
        self.label = AppLabel(root)
        self.slider_subject.add_observer(self.label)

        # スライダーの作成（異なる範囲で設定）
        self.sliders = [
            AppSlider(
                root, "Slider 1", self.slider_subject, min_value=0, max_value=100
            ),
            AppSlider(
                root, "Slider 2", self.slider_subject, min_value=0, max_value=4000
            ),
            AppSlider(root, "Slider 3", self.slider_subject, min_value=0, max_value=50),
        ]
        self.slider_subject.sliders = self.sliders  # スライダーリストを保存

        # ボタンの作成（スライダーの値を取得できるよう修正）
        self.buttons = [
            AppButton(root, "A", ButtonACommand(self.label, self.sliders)),
            AppButton(root, "B", ButtonBCommand(self.label, self.sliders)),
            AppButton(root, "C", ButtonCCommand(self.label, self.sliders)),
        ]


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
