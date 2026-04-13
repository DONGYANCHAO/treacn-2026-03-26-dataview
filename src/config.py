#!/usr/bin/env python3

from typing import List, Dict, Tuple

GRADE_ORDER: List[str] = [
    '一年级',
    '二年级',
    '三年级',
    '四年级',
    '五年级',
    '六年级'
]

CHINESE_FONTS: List[str] = [
    'Heiti TC',
    'STHeiti',
    'PingFang HK',
    'Arial Unicode MS',
    'Noto Sans CJK SC',
    'SimHei',
    'Microsoft YaHei'
]

STANDARD_HEIGHTS: Dict[str, Dict[str, float]] = {
    '一年级': {'男': 120.0, '女': 119.0},
    '二年级': {'男': 125.0, '女': 124.0},
    '三年级': {'男': 130.0, '女': 129.0},
    '四年级': {'男': 135.0, '女': 134.0},
    '五年级': {'男': 140.0, '女': 140.0},
    '六年级': {'男': 147.0, '女': 148.0},
}

BMI_THRESHOLDS: Dict[str, Tuple[float, float]] = {
    '偏瘦': (0, 14),
    '正常': (14, 18),
    '超重': (18, 21),
    '肥胖': (21, float('inf'))
}

BMI_CATEGORIES: List[str] = ['偏瘦', '正常', '超重', '肥胖']

HEIGHT_BINS: List[int] = [0, 110, 120, 130, 140, 150, 160, 200]
HEIGHT_LABELS: List[str] = [
    '<110cm',
    '110-120cm',
    '120-130cm',
    '130-140cm',
    '140-150cm',
    '150-160cm',
    '>160cm'
]

PERCENTILES: List[int] = [3, 10, 25, 50, 75, 90, 97]

HEIGHT_HISTOGRAM_BINS: range = range(100, 170, 5)

GRADE_COLORS: List[str] = [
    '#FF6B6B',
    '#4ECDC4',
    '#45B7D1',
    '#96CEB4',
    '#FFEAA7',
    '#DDA0DD'
]

GENDER_COLORS: Dict[str, str] = {
    '男': '#4A90E2',
    '女': '#E94B8A'
}

BMI_COLORS: List[str] = [
    '#2ECC71',
    '#3498DB',
    '#F39C12',
    '#E74C3C'
]

GENERAL_COLORS: Dict[str, str] = {
    'overall': '#2E86AB',
    'male': '#4A90E2',
    'female': '#E94B8A',
    'mean': 'red',
    'median': 'green',
    'trend': 'red'
}

PLOT_STYLES: Dict[str, int] = {
    'dpi': 300,
    'base_fontsize': 10,
    'label_fontsize': 12,
    'title_fontsize': 14,
    'legend_fontsize': 11
}

FIGURE_SIZES: Dict[str, Tuple[int, int]] = {
    'default': (10, 6),
    'wide': (12, 6),
    'extra_wide': (14, 6),
    'square': (8, 6)
}

REQUIRED_PACKAGES: List[str] = [
    'pandas',
    'numpy',
    'matplotlib',
    'openpyxl'
]

DATA_FILENAME: str = 'student_height_data.xlsx'
