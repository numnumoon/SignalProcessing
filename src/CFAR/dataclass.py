from dataclasses import dataclass

from common.load_yaml import load_yaml


@dataclass(frozen=True)
class WeibullConfig:
    guard_cell: int
    reference_cell: int
    pfa: float


# 他のCFARへの拡張を見越してここを分けた。
@dataclass(frozen=True)
class CFARConfig:
    cfar_config: WeibullConfig


def load_cfar_config():
    yaml_data = load_yaml("setting/CFAR.yaml")
    return CFARConfig(**yaml_data)
