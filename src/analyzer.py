"""
数据分析模块 - 学生身高与BMI分析器
"""

from functools import lru_cache
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

import config
from utils import add_bmi_to_dataframe, reorder_grade_index


class StudentHeightAnalyzer:
    """
    小学生身高数据分析类

    该类负责所有数据分析计算，不包含任何输出或打印逻辑。
    所有方法返回原始数据结果，由报表生成器负责格式化输出。
    """

    def __init__(self, df: pd.DataFrame) -> None:
        """
        初始化分析器

        Args:
            df: 学生数据DataFrame，必须包含以下列：
                - 学生ID, 姓名, 性别, 年级, 年龄, 身高(cm), 体重(kg), 入学日期
        """
        self._df: pd.DataFrame = df.copy()
        self._results: Dict[str, Any] = {}

    @property
    def df(self) -> pd.DataFrame:
        """获取数据副本"""
        return self._df.copy()

    @property
    def results(self) -> Dict[str, Any]:
        """获取所有分析结果"""
        return self._results.copy()

    @lru_cache(maxsize=1)
    def basic_statistics(self) -> Dict[str, Union[int, float]]:
        """
        基础统计分析

        Returns:
            包含各项统计指标的字典
        """
        height_series = self._df['身高(cm)']

        stats = {
            '总人数': len(self._df),
            '男生人数': int((self._df['性别'] == '男').sum()),
            '女生人数': int((self._df['性别'] == '女').sum()),
            '平均身高': round(height_series.mean(), 2),
            '身高标准差': round(height_series.std(), 2),
            '身高最小值': float(height_series.min()),
            '身高最大值': float(height_series.max()),
            '身高中位数': float(height_series.median()),
        }
        self._results['basic'] = stats
        return stats

    @lru_cache(maxsize=1)
    def grade_statistics(self) -> pd.DataFrame:
        """
        按年级统计

        Returns:
            各年级的统计信息DataFrame
        """
        grade_stats = self._df.groupby('年级').agg({
            '身高(cm)': ['count', 'mean', 'std', 'min', 'max'],
            '体重(kg)': ['mean', 'std']
        }).round(2)

        grade_stats.columns = [
            '人数', '平均身高', '身高标准差', '最矮身高', '最高身高', '平均体重', '体重标准差'
        ]

        grade_stats = reorder_grade_index(grade_stats)
        self._results['by_grade'] = grade_stats
        return grade_stats

    @lru_cache(maxsize=1)
    def gender_statistics(self) -> pd.DataFrame:
        """
        按性别统计

        Returns:
            按性别和年级的统计信息DataFrame
        """
        gender_stats = self._df.groupby(['年级', '性别'])['身高(cm)'].agg([
            'count', 'mean', 'std'
        ]).round(2)
        gender_stats.columns = ['人数', '平均身高', '标准差']

        self._results['by_gender'] = gender_stats
        return gender_stats

    @lru_cache(maxsize=1)
    def age_statistics(self) -> pd.DataFrame:
        """
        按年龄统计

        Returns:
            各年龄的统计信息DataFrame
        """
        age_stats = self._df.groupby('年龄')['身高(cm)'].agg([
            'count', 'mean', 'std', 'min', 'max'
        ]).round(2)
        age_stats.columns = ['人数', '平均身高', '标准差', '最矮身高', '最高身高']

        self._results['by_age'] = age_stats
        return age_stats

    @lru_cache(maxsize=1)
    def height_distribution(self) -> Dict[str, int]:
        """
        身高分布统计

        Returns:
            各身高段的人数分布字典
        """
        self._df['身高段'] = pd.cut(
            self._df['身高(cm)'],
            bins=config.HEIGHT_BINS,
            labels=config.HEIGHT_LABELS,
            right=False
        )
        distribution = self._df['身高段'].value_counts().sort_index().to_dict()

        self._results['height_distribution'] = distribution
        return distribution

    @lru_cache(maxsize=1)
    def growth_analysis(self) -> pd.DataFrame:
        """
        生长趋势分析

        Returns:
            相邻年级的身高增长情况DataFrame
        """
        grade_means = self._df.groupby('年级')['身高(cm)'].mean()
        grade_means = grade_means.reindex(config.GRADE_ORDER)

        growth_data: List[Dict[str, Union[str, float]]] = []
        for i in range(1, len(config.GRADE_ORDER)):
            prev_grade = config.GRADE_ORDER[i - 1]
            curr_grade = config.GRADE_ORDER[i]
            growth = grade_means[curr_grade] - grade_means[prev_grade]
            growth_data.append({
                '年级段': f"{prev_grade}到{curr_grade}",
                '身高增长(cm)': round(growth, 2),
                '增长率(%)': round(growth / grade_means[prev_grade] * 100, 2)
            })

        growth_df = pd.DataFrame(growth_data)
        self._results['growth'] = growth_df
        return growth_df

    @lru_cache(maxsize=1)
    def percentile_analysis(self) -> pd.DataFrame:
        """
        身高百分位数分析

        Returns:
            各年级的身高百分位数DataFrame
        """
        percentile_data: List[Dict[str, Union[str, float]]] = []

        for grade in config.GRADE_ORDER:
            grade_data = self._df[self._df['年级'] == grade]['身高(cm)']
            row: Dict[str, Union[str, float]] = {'年级': grade}
            for p in config.PERCENTILES:
                row[f'P{p}'] = round(np.percentile(grade_data, p), 1)
            percentile_data.append(row)

        percentile_df = pd.DataFrame(percentile_data)
        self._results['percentiles'] = percentile_df
        return percentile_df

    @lru_cache(maxsize=1)
    def bmi_analysis(self) -> Tuple[Dict[str, int], pd.DataFrame]:
        """
        BMI分析

        Returns:
            (BMI总体分布字典, 各年级BMI分布DataFrame)
        """
        df_with_bmi = add_bmi_to_dataframe(self._df)

        bmi_dist = df_with_bmi['BMI分类'].value_counts().to_dict()
        bmi_by_grade = pd.crosstab(df_with_bmi['年级'], df_with_bmi['BMI分类'])
        bmi_by_grade = reorder_grade_index(bmi_by_grade)

        self._results['bmi_distribution'] = bmi_dist
        self._results['bmi_by_grade'] = bmi_by_grade

        return bmi_dist, bmi_by_grade

    @lru_cache(maxsize=1)
    def compare_with_standard(self) -> pd.DataFrame:
        """
        与标准身高对比

        Returns:
            各年级与标准身高的对比DataFrame
        """
        comparison_data: List[Dict[str, Union[str, float]]] = []

        for grade in config.GRADE_ORDER:
            for gender in ['男', '女']:
                actual_mean = self._df[
                    (self._df['年级'] == grade) & (self._df['性别'] == gender)
                ]['身高(cm)'].mean()
                standard = config.STANDARD_HEIGHTS[grade][gender]
                diff = actual_mean - standard

                comparison_data.append({
                    '年级': grade,
                    '性别': gender,
                    '实际平均身高': round(actual_mean, 2),
                    '标准身高': standard,
                    '差异': round(diff, 2),
                    '差异百分比': round(diff / standard * 100, 2)
                })

        comparison_df = pd.DataFrame(comparison_data)
        self._results['standard_comparison'] = comparison_df
        return comparison_df

    def run_all_analysis(self) -> Dict[str, Any]:
        """
        运行所有分析

        Returns:
            所有分析结果的字典
        """
        self.basic_statistics()
        self.grade_statistics()
        self.gender_statistics()
        self.age_statistics()
        self.height_distribution()
        self.growth_analysis()
        self.percentile_analysis()
        self.bmi_analysis()
        self.compare_with_standard()

        return self._results

