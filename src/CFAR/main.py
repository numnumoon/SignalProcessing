import sys
from pathlib import Path

# 現在のファイル位置から3階層上のディレクトリを取得
project_root = Path(__file__).resolve().parent.parent.parent

# sys.path にプロジェクトのルートディレクトリを追加
sys.path.append(str(project_root))

from dataclass import load_cfar_config

if __name__ == "__main__":
    cfar_config = load_cfar_config()
    print(cfar_config)
