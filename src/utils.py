"""
工具模块 - 封装通用功能
"""

import os
from functools import lru_cache
from typing import Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager

import config


# =============================================================================
# 路径管理
# =============================================================================

def get_project_paths(base_dir: Optional[str] = None) -> Dict[str, str]:
    """
    获取项目各目录路径

    Args:
        base_dir: 项目根目录，默认为当前文件的上两级目录

    Returns:
        包含各目录路径的字典
    """
    if base_dir is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    return {
        'base': base_dir,
        'data': os.path.join(base_dir, config.DEFAULT_DATA_DIR),
        'src': os.path.join(base_dir, 'src'),
        'output': os.path.join(base_dir, config.DEFAULT_OUTPUT_DIR)
    }


def ensure_dir(path: str) -> str:
    """
    确保目录存在，不存在则创建

    Args:
        path: 目录路径

    Returns:
        目录路径
    """
    os.makedirs(path, exist_ok=True)
    return path


def get_data_file_path(filename: Optional[str] = None, base_dir: Optional[str] = None) -> str:
    """
    获取数据文件完整路径

    Args:
        filename: 文件名，默认使用配置中的默认文件名
        base_dir: 项目根目录

    Returns:
        数据文件完整路径
    """
    if filename is None:
        filename = config.DEFAULT_DATA_FILENAME
    paths = get_project_paths(base_dir)
    return os.path.join(paths['data'], filename)


def get_output_path(filename: str, base_dir: Optional[str] = None) -> str:
    """
    获取输出文件完整路径

    Args:
        filename: 输出文件名
        base_dir: 项目根目录

    Returns:
        输出文件完整路径
    """
    paths = get_project_paths(base_dir)
    ensure_dir(paths['output'])
    return os.path.join(paths['output'], filename)


# =============================================================================
# 数据加载器（带缓存）
# =============================================================================

@lru_cache(maxsize=4)
def load_data_cached(file_path: str) -> pd.DataFrame:
    """
    带缓存的数据加载器

    Args:
        file_path: Excel文件路径

    Returns:
        DataFrame数据
    """
    return pd.read_excel(file_path)


def load_data(file_path: str, use_cache: bool = True) -> pd.DataFrame:
    """
    加载数据文件

    Args:
        file_path: Excel文件路径
        use_cache: 是否使用缓存

    Returns:
        DataFrame数据
    """
    if use_cache:
        return load_data_cached(file_path)
    return pd.read_excel(file_path)


def save_data(df: pd.DataFrame, filepath: str) -> None:
    """
    保存数据到Excel文件

    Args:
        df: DataFrame数据
        filepath: 保存路径
    """
    ensure_dir(os.path.dirname(filepath))
    df.to_excel(filepath, index=False, engine='openpyxl')


# =============================================================================
# BMI 计算与分类
# =============================================================================

def calculate_bmi(height_cm: float, weight_kg: float) -> float:
    """
    计算BMI值

    Args:
        height_cm: 身高（厘米）
        weight_kg: 体重（千克）

    Returns:
        BMI值（保留2位小数）
    """
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def classify_bmi(bmi: float) -> str:
    """
    根据BMI值分类（儿童标准）

    Args:
        bmi: BMI值

    Returns:
        BMI分类标签
    """
    if bmi < config.BMI_THRESHOLDS['underweight']:
        return '偏瘦'
    elif bmi < config.BMI_THRESHOLDS['normal']:
        return '正常'
    elif bmi < config.BMI_THRESHOLDS['overweight']:
        return '超重'
    else:
        return '肥胖'


def add_bmi_to_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    为DataFrame添加BMI列和BMI分类列

    Args:
        df: 包含身高体重列的DataFrame

    Returns:
        添加了BMI列的DataFrame
    """
    df = df.copy()
    df['BMI'] = df.apply(
        lambda row: calculate_bmi(row['身高(cm)'], row['体重(kg)']),
        axis=1
    )
    df['BMI分类'] = df['BMI'].apply(classify_bmi)
    return df


# =============================================================================
# 字体与图表样式设置
# =============================================================================

def setup_chinese_font() -> Optional[str]:
    """
    设置中文字体

    Returns:
        选中的字体名称，如果未找到则返回None
    """
    available_fonts = [f.name for f in font_manager.fontManager.ttflist]

    selected_font = None
    for font in config.CHINESE_FONTS:
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


def apply_common_style(ax, title: Optional[str] = None,
                       xlabel: Optional[str] = None,
                       ylabel: Optional[str] = None) -> None:
    """
    应用通用图表样式

    Args:
        ax: matplotlib轴对象
        title: 标题
        xlabel: X轴标签
        ylabel: Y轴标签
    """
    if title:
        ax.set_title(title, fontsize=config.FONT_SIZE_TITLE, fontweight='bold', pad=20)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=config.FONT_SIZE_LABEL, fontweight='bold')
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=config.FONT_SIZE_LABEL, fontweight='bold')

    ax.grid(axis='y', alpha=config.GRID_ALPHA, linestyle=config.GRID_LINESTYLE)


def add_value_labels(ax, bars, fmt: str = '{:.1f}',
                     offset: Tuple[float, float] = (0, 0),
                     fontsize: int = 9) -> None:
    """
    为柱状图添加数值标签

    Args:
        ax: matplotlib轴对象
        bars: 柱状图对象
        fmt: 数值格式
        offset: 文本偏移量
        fontsize: 字体大小
    """
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2. + offset[0],
            height + offset[1],
            fmt.format(height),
            ha='center', va='bottom', fontsize=fontsize
        )


def save_figure(fig, filepath: str, dpi: int = config.DPI) -> None:
    """
    保存图表到文件

    Args:
        fig: matplotlib图形对象
        filepath: 保存路径
        dpi: 分辨率
    """
    ensure_dir(os.path.dirname(filepath))
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"图表已保存: {filepath}")


# =============================================================================
# 数据处理工具
# =============================================================================

def sort_by_grade(df: pd.DataFrame, grade_col: str = '年级') -> pd.DataFrame:
    """
    按年级顺序排序DataFrame

    Args:
        df: 包含年级列的DataFrame
        grade_col: 年级列名

    Returns:
        排序后的DataFrame
    """
    if grade_col in df.index.names:
        return df.reindex(config.GRADE_ORDER)
    return df.reindex(config.GRADE_ORDER)


def reorder_grade_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    重新排序以年级为索引的DataFrame

    Args:
        df: 以年级为索引的DataFrame

    Returns:
        排序后的DataFrame
    """
    return df.reindex(config.GRADE_ORDER)


# =============================================================================
# 依赖检查
# =============================================================================

def check_dependencies() -> Tuple[bool, List[str]]:
    """
    检查必要的依赖包

    Returns:
        (是否全部存在, 缺失的包列表)
    """
    required_packages = ['pandas', 'numpy', 'matplotlib', 'openpyxl']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    return len(missing_packages) == 0, missing_packages


# =============================================================================
# 数据生成工具
# =============================================================================

def generate_random_name(random_gen) -> str:
    """
    生成随机姓名

    Args:
        random_gen: 随机数生成器

    Returns:
        随机姓名
    """
    return random_gen.choice(config.SURNAMES) + random_gen.choice(config.NAMES)


def generate_enrollment_date(grade: str, random_gen) -> str:
    """
    生成入学日期

    Args:
        grade: 年级
        random_gen: 随机数生成器

    Returns:
        入学日期字符串
    """
    grade_num = config.GRADE_TO_NUM[grade]
    year = 2024 - (grade_num - 1)
    month = random_gen.randint(9, 12) if grade_num == 1 else random_gen.randint(1, 12)
    day = random_gen.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"
