import tkinter as tk
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


class GraphModel:
    """グラフの色データを管理"""

    def __init__(self, index):
        self.index = index
        self.color = [0, 0, 255]  # 初期色（青）

    def update_color(self, color_key, value):
        """RGB値を更新（if文なし）"""
        color_index = {"r": 0, "g": 1, "b": 2}  # color_key に対応するインデックス
        self.color[color_index[color_key]] = value

    def get_color(self):
        """Matplotlib用に正規化した色を取得"""
        return tuple(c / 255 for c in self.color)


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class GraphController(tk.Frame):
    """Matplotlibを使ったグラフ描画クラス（ズーム・拡大対応）"""

    def __init__(self, parent, event_handler, graph_models):
        super().__init__(parent)
        self.event_handler = event_handler
        self.graph_models = graph_models

        # Figure を作成
        self.figure = plt.figure(figsize=(5, 6))
        self.axes = []  # 複数の Axes を管理するリスト

        # 3つのグラフを add_subplot で追加
        for i in range(3):
            ax = self.figure.add_subplot(3, 1, i + 1)  # (行, 列, インデックス)
            self.axes.append(ax)

        # Matplotlib キャンバスを Tkinter に埋め込む
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side="top", fill="both", expand=True)

        # Navigation Toolbar（拡大・ズーム用）
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.toolbar.pack(side="top", fill="x")

        # イベントを購読
        self.event_handler.subscribe("color_changed", self.update_graph)

        self.draw_graphs()

    def draw_graphs(self):
        """すべてのグラフを描画"""
        x = np.linspace(0, 10, 100)
        y_list = [np.sin(x), np.cos(x), np.tan(x)]

        for i, ax in enumerate(self.axes):
            ax.clear()
            ax.plot(x, y_list[i], color=self.graph_models[i].get_color())
            ax.set_title(f"Graph {i+1}")

        self.canvas.draw()

    def update_graph(self, graph_index):
        """指定されたグラフのみ更新（拡大状態を保持）"""
        x = np.linspace(0, 10, 100)
        y_list = [np.sin(x), np.cos(x), np.tan(x)]

        ax = self.axes[graph_index]

        # 現在のズーム状態（表示範囲）を保存
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        ax.clear()
        ax.plot(
            x, y_list[graph_index], color=self.graph_models[graph_index].get_color()
        )
        ax.set_title(f"Graph {graph_index+1}")

        # ズーム状態を元に戻す
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)

        self.canvas.draw()


class ColorControl(tk.Frame):
    """RGBスライダーとボタンを管理"""

    def __init__(self, parent, event_handler, graph_model, color_key):
        super().__init__(parent)
        self.event_handler = event_handler
        self.graph_model = graph_model
        self.color_key = color_key

        # color_key を正式な色名に変換
        color_name = {"r": "Red", "g": "Green", "b": "Blue"}[color_key]
        color_fg = {"r": "red", "g": "green", "b": "blue"}[
            color_key
        ]  # 色指定を正式な名前に変換

        tk.Label(self, text=color_name, fg=color_fg, font=("Arial", 10, "bold")).pack()

        self.scale = tk.Scale(
            self,
            from_=0,
            to=255,
            orient="horizontal",
            length=250,
            command=self.on_scale_change,
        )
        self.scale.pack(fill="x")

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
        """スライダー変更時の処理"""
        self.graph_model.update_color(self.color_key, int(value))
        self.event_handler.notify("color_changed", self.graph_model.index)

    def adjust_scale(self, delta):
        """ボタン押下でスライドバーの値を変更"""
        new_value = self.scale.get() + delta
        new_value = max(0, min(255, new_value))
        self.scale.set(new_value)
        self.on_scale_change(new_value)


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RGB変更でグラフの色を変更")
        self.geometry("900x700")

        self.event_handler = EventHandler()
        self.graph_models = [GraphModel(i) for i in range(3)]

        GraphController(self, self.event_handler, self.graph_models).grid(
            row=0, column=0, sticky="nsew"
        )

        control_frame = tk.Frame(self)
        control_frame.grid(row=0, column=1, sticky="ns")

        for i, model in enumerate(self.graph_models):
            for key in ["r", "g", "b"]:
                ColorControl(control_frame, self.event_handler, model, key).pack(
                    fill="x"
                )


if __name__ == "__main__":
    app = Application()
    app.mainloop()
