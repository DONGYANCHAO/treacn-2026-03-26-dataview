import os
from functools import lru_cache
from typing import Dict, Optional, Tuple, Any

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager

from config import (
    CHINESE_FONTS, BMI_THRESHOLDS, BMI_ORDER,
    FONT_SIZE_TITLE, FONT_SIZE_LABEL, FONT_WEIGHT_BOLD,
    GRID_ALPHA, GRID_LINESTYLE, DATA_DIR_NAME, OUTPUT_DIR_NAME,
    SRC_DIR_NAME, DATA_FILENAME
)


class PathManager:
    """路径管理工具类"""

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self._base_dir = base_dir

    @property
    def base(self) -> str:
        return self._base_dir

    @property
    def data(self) -> str:
        return os.path.join(self._base_dir, DATA_DIR_NAME)

    @property
    def output(self) -> str:
        return os.path.join(self._base_dir, OUTPUT_DIR_NAME)

    @property
    def src(self) -> str:
        return os.path.join(self._base_dir, SRC_DIR_NAME)

    @property
    def data_file(self) -> str:
        return os.path.join(self.data, DATA_FILENAME)

    def ensure_dirs(self) -> None:
        for dir_path in [self.base, self.data, self.output, self.src]:
            os.makedirs(dir_path, exist_ok=True)


class DataLoader:
    """带缓存的数据加载器"""

    _cache: Dict[str, pd.DataFrame] = {}

    @classmethod
    def load(cls, file_path: str, use_cache: bool = True) -> pd.DataFrame:
        if use_cache and file_path in cls._cache:
            return cls._cache[file_path].copy()

        df = pd.read_excel(file_path)

        if use_cache:
            cls._cache[file_path] = df.copy()

        return df

    @classmethod
    def clear_cache(cls, file_path: Optional[str] = None) -> None:
        if file_path:
            cls._cache.pop(file_path, None)
        else:
            cls._cache.clear()


def calculate_bmi(weight: float, height_cm: float) -> float:
    return round(weight / (height_cm / 100) ** 2, 2)


def classify_bmi(bmi: float, age: Optional[int] = None) -> str:
    for category, (low, high) in BMI_THRESHOLDS.items():
        if low <= bmi < high:
            return category
    return BMI_ORDER[-1]


def get_bmi_category_order() -> list:
    return BMI_ORDER.copy()


def setup_chinese_font() -> Optional[str]:
    available_fonts = [f.name for f in font_manager.fontManager.ttflist]

    selected_font = None
    for font in CHINESE_FONTS:
        if font in available_fonts:
            selected_font = font
            break

    if selected_font:
        plt.rcParams['font.sans-serif'] = [selected_font] + plt.rcParams['font.sans-serif']
        print(f"使用中文字体: {selected_font}")
    else:
        print("警告: 未找到合适的中文字体，中文可能显示为方框")

    plt.rcParams['axes.unicode_minus'] = False

    return selected_font


def apply_common_style(ax: plt.Axes, title: str, xlabel: str, ylabel: str) -> None:
    ax.set_xlabel(xlabel, fontsize=FONT_SIZE_LABEL, fontweight=FONT_WEIGHT_BOLD)
    ax.set_ylabel(ylabel, fontsize=FONT_SIZE_LABEL, fontweight=FONT_WEIGHT_BOLD)
    ax.set_title(title, fontsize=FONT_SIZE_TITLE, fontweight=FONT_WEIGHT_BOLD, pad=20)
    ax.grid(axis='y', alpha=GRID_ALPHA, linestyle=GRID_LINESTYLE)


def add_value_labels(ax: plt.Axes, bars, fontsize: int = 10, fmt: str = '{:.1f}') -> None:
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height,
            fmt.format(height),
            ha='center', va='bottom',
            fontsize=fontsize, fontweight=FONT_WEIGHT_BOLD
        )


def add_value_labels_with_unit(ax: plt.Axes, bars, unit: str = 'cm', fontsize: int = 10) -> None:
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height,
            f'{height:.1f}{unit}',
            ha='center', va='bottom',
            fontsize=fontsize, fontweight=FONT_WEIGHT_BOLD
        )


def save_figure(fig: plt.Figure, output_dir: str, filename: str, dpi: int = 300) -> str:
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"图表已保存: {filepath}")
    return filepath


def check_dependencies() -> Tuple[bool, list]:
    required_packages = ['pandas', 'numpy', 'matplotlib', 'openpyxl']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    return len(missing_packages) == 0, missing_packages


@lru_cache(maxsize=128)
def cached_mean(values_tuple: tuple) -> float:
    return np.mean(values_tuple)


@lru_cache(maxsize=128)
def cached_std(values_tuple: tuple) -> float:
    return np.std(values_tuple)


def series_to_hashable(s: pd.Series) -> tuple:
    return tuple(s.values)
