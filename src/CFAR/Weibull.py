import numpy as np
import dataclasses
import matplotlib.pyplot as plt

import CFAR


@dataclasses.dataclass
class WeibullCFAR(CFAR):
    """ワイブルCFAR処理

    Args:
        CFAR (_type_): _description_

    Returns:
        int: 検出結果 (1:ターゲット, 0:ノイズ)
    """

    threshold: float
    guard_cell: int
    reference_cell: int
    pfa: float

    def calculate_average():
        q

    def judgment_threshold(self, after_cfar_data):
        return np.where(after_cfar_data <= self.threshold, 0, 255)


if __name__ == "__main__":
    plt.show()
