import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class EventHandler:
    """イベントを管理するクラス"""

    def __init__(self):
        self._events = {}

    def subscribe(self, event_name, callback):
        """イベントに関数を登録"""
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(callback)

    def notify(self, event_name, *args, **kwargs):
        """イベントを発火し、登録された関数を実行"""
        if event_name in self._events:
            for callback in self._events[event_name]:
                callback(*args, **kwargs)


class ClassA(tk.Frame):
    """スケールの値を変更するクラス（R, G, B）"""

    def __init__(self, parent, event_handler, label_text, color_key, graph_index):
        super().__init__(parent, bd=2, relief="groove", padx=5, pady=5)
        self.event_handler = event_handler
        self.color_key = color_key  # "r", "g", "b" のいずれか
        self.graph_index = graph_index  # 0, 1, 2（どのグラフに対応するか）

        # color_key を Tkinter の色名に変換
        color_name = {"r": "red", "g": "green", "b": "blue"}[color_key]

        self.label = tk.Label(
            self, text=label_text, fg=color_name, font=("Arial", 10, "bold")
        )
        self.label.pack(anchor="w")

        self.scale = tk.Scale(
            self,
            from_=0,
            to=255,
            orient="horizontal",
            length=250,
            command=self.on_scale_change,
        )
        self.scale.pack(fill="x")

        # ボタン（-10, -1, +1, +10）
        btn_frame = tk.Frame(self)
        btn_frame.pack()

        for text, delta in [("-10", -10), ("-1", -1), ("+1", 1), ("+10", 10)]:
            tk.Button(
                btn_frame,
                text=text,
                command=lambda d=delta: self.adjust_scale(d),
                width=4,
            ).pack(side="left")

    def on_scale_change(self, value):
        """スケール変更時にRGB値を更新（対象グラフのみ再描画）"""
        self.event_handler.notify(
            "color_changed", self.graph_index, self.color_key, int(value)
        )

    def adjust_scale(self, delta):
        """ボタン押下でスライドバーの値を変更"""
        new_value = self.scale.get() + delta
        new_value = max(0, min(255, new_value))  # 0〜255の範囲に制限
        self.scale.set(new_value)
        self.on_scale_change(new_value)  # 変更を即時反映


class ClassC(tk.Frame):
    """Matplotlibを使ったグラフ描画クラス（3つのグラフを管理）"""

    def __init__(self, parent, event_handler):
        super().__init__(parent)
        self.event_handler = event_handler
        self.line_colors = [
            [0, 0, 255],
            [0, 255, 0],
            [255, 0, 0],
        ]  # 初期色（青・緑・赤）

        # Matplotlibのセットアップ（3つのグラフを並べる）
        self.figure, self.axes = plt.subplots(3, 1, figsize=(5, 6))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack()

        # イベントを購読
        self.event_handler.subscribe("color_changed", self.update_color)

    def update_color(self, graph_index, color_key, value):
        """指定されたグラフのみ色を変更して再描画"""
        if color_key == "r":
            self.line_colors[graph_index][0] = value
        elif color_key == "g":
            self.line_colors[graph_index][1] = value
        elif color_key == "b":
            self.line_colors[graph_index][2] = value

        # 対象のグラフのみ再描画
        x = np.linspace(0, 10, 100)
        y_list = [np.sin(x), np.cos(x), np.tan(x)]

        self.axes[graph_index].clear()
        self.axes[graph_index].plot(
            x, y_list[graph_index], color=self._get_color(graph_index)
        )
        self.axes[graph_index].set_title(f"Graph {graph_index+1}")
        self.canvas.draw()

    def _get_color(self, graph_index):
        """現在のRGB値を正規化してMatplotlib用の色に変換"""
        return tuple(c / 255 for c in self.line_colors[graph_index])


class Application(tk.Tk):
    """アプリケーション全体を管理するクラス"""

    def __init__(self):
        super().__init__()

        self.title("RGB変更でグラフの色を変更")
        self.geometry("900x700")  # ウィンドウサイズを広げる

        self.event_handler = EventHandler()

        # メインフレーム（左：グラフ / 右：スライダー）
        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # 左側：グラフ
        graph_frame = tk.Frame(main_frame, bd=3, relief="ridge", padx=5, pady=5)
        graph_frame.pack(side="left", fill="both", expand=True)
        self.class_c = ClassC(graph_frame, self.event_handler)
        self.class_c.pack()

        # 右側：スライダー
        control_frame = tk.Frame(main_frame, bd=3, relief="ridge", padx=10, pady=10)
        control_frame.pack(side="right", fill="y")

        tk.Label(
            control_frame, text="Color Controls", font=("Arial", 14, "bold")
        ).pack()

        # 各グラフに対応するスライダーを右側に配置
        for i in range(3):
            frame = tk.Frame(control_frame, bd=2, relief="groove", padx=5, pady=5)
            frame.pack(pady=5, fill="x")

            tk.Label(
                frame, text=f"Graph {i+1} Controls", font=("Arial", 12, "bold")
            ).pack()

            ClassA(frame, self.event_handler, "Red", "r", i).pack(fill="x")
            ClassA(frame, self.event_handler, "Green", "g", i).pack(fill="x")
            ClassA(frame, self.event_handler, "Blue", "b", i).pack(fill="x")


if __name__ == "__main__":
    app = Application()
    app.mainloop()
