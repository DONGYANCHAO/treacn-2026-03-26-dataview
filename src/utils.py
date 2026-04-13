#!/usr/bin/env python3

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from functools import lru_cache
from typing import Dict, Tuple, Optional

from config import (
    CHINESE_FONTS,
    BMI_THRESHOLDS,
    PLOT_STYLES,
    GRADE_ORDER
)

_DATA_CACHE: Optional[pd.DataFrame] = None


@lru_cache(maxsize=None)
def load_data_cached(data_path: str) -> pd.DataFrame:
    global _DATA_CACHE
    if _DATA_CACHE is None:
        _DATA_CACHE = pd.read_excel(data_path)
    return _DATA_CACHE


def clear_data_cache() -> None:
    global _DATA_CACHE
    _DATA_CACHE = None
    load_data_cached.cache_clear()


def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    return round(weight_kg / (height_cm / 100) ** 2, 2)


def classify_bmi(bmi: float, age: Optional[int] = None) -> str:
    for category, (lower, upper) in BMI_THRESHOLDS.items():
        if lower <= bmi < upper:
            return category
    return '肥胖'


def add_bmi_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['BMI'] = df.apply(
        lambda row: calculate_bmi(row['身高(cm)'], row['体重(kg)']),
        axis=1
    )
    df['BMI分类'] = df.apply(
        lambda row: classify_bmi(row['BMI'], row['年龄']),
        axis=1
    )
    return df


def setup_chinese_font() -> None:
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


def apply_plot_style(ax, xlabel: str = None, ylabel: str = None,
                     title: str = None, grid_axis: str = 'y') -> None:
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=PLOT_STYLES['label_fontsize'], fontweight='bold')
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=PLOT_STYLES['label_fontsize'], fontweight='bold')
    if title:
        ax.set_title(title, fontsize=PLOT_STYLES['title_fontsize'], fontweight='bold', pad=20)
    if grid_axis:
        ax.grid(axis=grid_axis, alpha=0.3, linestyle='--')


def add_value_labels(bars, ax, decimals: int = 1, unit: str = '',
                     offset: int = 0, fontsize: int = None) -> None:
    if fontsize is None:
        fontsize = PLOT_STYLES['base_fontsize']
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height + offset,
            f'{height:.{decimals}f}{unit}',
            ha='center',
            va='bottom',
            fontsize=fontsize,
            fontweight='bold'
        )


def get_project_paths() -> Dict[str, str]:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return {
        'base': base_dir,
        'data': os.path.join(base_dir, 'data'),
        'src': os.path.join(base_dir, 'src'),
        'output': os.path.join(base_dir, 'output')
    }


def ensure_directories(paths: Dict[str, str]) -> None:
    for dir_path in paths.values():
        os.makedirs(dir_path, exist_ok=True)


def check_dependencies() -> bool:
    from config import REQUIRED_PACKAGES
    missing_packages = []
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("错误: 缺少以下依赖包:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        print("\n请使用以下命令安装:")
        print(f"  pip install {' '.join(missing_packages)}")
        return False
    return True


def reindex_by_grade(df: pd.DataFrame) -> pd.DataFrame:
    return df.reindex(GRADE_ORDER)


def save_plot(fig, output_path: str, filename: str) -> None:
    fig.tight_layout()
    full_path = os.path.join(output_path, filename)
    plt.savefig(full_path, dpi=PLOT_STYLES['dpi'], bbox_inches='tight')
    print(f"图表已保存: {full_path}")
    plt.show()
