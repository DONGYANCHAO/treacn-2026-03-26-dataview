from typing import Dict, List, Tuple

GRADE_ORDER: List[str] = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级']

GRADE_TO_NUM: Dict[str, int] = {
    '一年级': 1, '二年级': 2, '三年级': 3,
    '四年级': 4, '五年级': 5, '六年级': 6
}

GRADE_AGE_RANGE: Dict[str, Tuple[int, int]] = {
    '一年级': (6, 7),
    '二年级': (7, 8),
    '三年级': (8, 9),
    '四年级': (9, 10),
    '五年级': (10, 11),
    '六年级': (11, 12)
}

HEIGHT_STATS: Dict[str, Dict[str, Tuple[float, float]]] = {
    '一年级': {'男': (120.0, 5.5), '女': (119.0, 5.3)},
    '二年级': {'男': (125.0, 5.8), '女': (124.0, 5.5)},
    '三年级': {'男': (130.0, 6.0), '女': (129.0, 5.8)},
    '四年级': {'男': (135.0, 6.2), '女': (134.0, 6.0)},
    '五年级': {'男': (140.0, 6.5), '女': (140.0, 6.3)},
    '六年级': {'男': (147.0, 7.0), '女': (148.0, 6.8)},
}

STANDARD_HEIGHTS: Dict[str, Dict[str, float]] = {
    '一年级': {'男': 120.0, '女': 119.0},
    '二年级': {'男': 125.0, '女': 124.0},
    '三年级': {'男': 130.0, '女': 129.0},
    '四年级': {'男': 135.0, '女': 134.0},
    '五年级': {'男': 140.0, '女': 140.0},
    '六年级': {'男': 147.0, '女': 148.0},
}

HEIGHT_BINS: List[int] = [0, 110, 120, 130, 140, 150, 160, 200]
HEIGHT_LABELS: List[str] = ['<110cm', '110-120cm', '120-130cm', '130-140cm', '140-150cm', '150-160cm', '>160cm']

BMI_THRESHOLDS: Dict[str, Tuple[float, float]] = {
    '偏瘦': (0, 14),
    '正常': (14, 18),
    '超重': (18, 21),
    '肥胖': (21, float('inf'))
}

BMI_ORDER: List[str] = ['偏瘦', '正常', '超重', '肥胖']

PERCENTILES: List[int] = [3, 10, 25, 50, 75, 90, 97]

SURNAMES: List[str] = [
    '王', '李', '张', '刘', '陈', '杨', '黄', '赵', '吴', '周',
    '徐', '孙', '马', '朱', '胡', '郭', '何', '林', '罗', '高',
    '郑', '梁', '谢', '宋', '唐', '许', '韩', '冯', '邓', '曹'
]

GIVEN_NAMES: List[str] = [
    '伟', '芳', '娜', '秀英', '敏', '静', '丽', '强', '磊', '军',
    '洋', '勇', '艳', '杰', '娟', '涛', '明', '超', '秀兰', '霞',
    '平', '刚', '桂英', '文', '辉', '鑫', '宇', '博', '浩', '然',
    '梓', '涵', '轩', '怡', '欣', '雨', '晨', '曦', '阳', '昊',
    '思', '琪', '佳', '雪', '梦', '瑶', '琳', '婉', '清', '悦'
]

COLORS_GRADE: List[str] = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']

COLOR_MALE: str = '#4A90E2'
COLOR_FEMALE: str = '#E94B8A'
COLOR_OVERALL: str = '#2E86AB'

COLORS_BMI: List[str] = ['#2ECC71', '#3498DB', '#F39C12', '#E74C3C']

COLOR_HISTOGRAM: str = '#5DADE2'

COLORMAP_HEATMAP: str = 'YlOrRd'

FONT_SIZE_TITLE: int = 14
FONT_SIZE_LABEL: int = 12
FONT_SIZE_TICK: int = 11
FONT_SIZE_LEGEND: int = 11
FONT_SIZE_ANNOTATION: int = 9
FONT_SIZE_VALUE_LABEL: int = 10

FONT_WEIGHT_BOLD: str = 'bold'

LINE_WIDTH_MAIN: float = 3.0
LINE_WIDTH_SECONDARY: float = 2.5
MARKER_SIZE_MAIN: int = 10
MARKER_SIZE_SECONDARY: int = 8

FIGURE_SIZE_WIDE: Tuple[int, int] = (12, 6)
FIGURE_SIZE_STANDARD: Tuple[int, int] = (10, 6)
FIGURE_SIZE_HEATMAP: Tuple[int, int] = (8, 6)
FIGURE_SIZE_BMI: Tuple[int, int] = (14, 6)

DPI: int = 300

GRID_ALPHA: float = 0.3
GRID_LINESTYLE: str = '--'

BAR_WIDTH: float = 0.35
BAR_EDGE_WIDTH: float = 1.2

SCATTER_ALPHA: float = 0.6
SCATTER_SIZE: int = 50

CHINESE_FONTS: List[str] = ['Heiti TC', 'STHeiti', 'PingFang HK', 'Arial Unicode MS', 'Noto Sans CJK SC']

DATA_DIR_NAME: str = 'data'
OUTPUT_DIR_NAME: str = 'output'
SRC_DIR_NAME: str = 'src'

DATA_FILENAME: str = 'student_height_data.xlsx'

REPORT_LINE_WIDTH: int = 60
