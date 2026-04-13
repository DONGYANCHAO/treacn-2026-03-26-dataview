from functools import cached_property
from typing import Dict, Any, Tuple, Optional

import pandas as pd
import numpy as np

from config import (
    GRADE_ORDER, HEIGHT_BINS, HEIGHT_LABELS,
    STANDARD_HEIGHTS, PERCENTILES
)
from utils import calculate_bmi, classify_bmi


class StudentHeightAnalyzer:
    """小学生身高数据分析类"""

    def __init__(self, df: pd.DataFrame):
        self._df = df.copy()
        self._results: Dict[str, Any] = {}

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def results(self) -> Dict[str, Any]:
        return self._results

    @cached_property
    def _df_with_bmi(self) -> pd.DataFrame:
        df = self._df.copy()
        df['BMI'] = df.apply(
            lambda x: calculate_bmi(x['体重(kg)'], x['身高(cm)']),
            axis=1
        )
        df['BMI分类'] = df.apply(
            lambda x: classify_bmi(x['BMI'], x['年龄']),
            axis=1
        )
        return df

    def basic_statistics(self) -> Dict[str, Any]:
        stats: Dict[str, Any] = {
            '总人数': len(self._df),
            '男生人数': len(self._df[self._df['性别'] == '男']),
            '女生人数': len(self._df[self._df['性别'] == '女']),
            '平均身高': round(self._df['身高(cm)'].mean(), 2),
            '身高标准差': round(self._df['身高(cm)'].std(), 2),
            '身高最小值': self._df['身高(cm)'].min(),
            '身高最大值': self._df['身高(cm)'].max(),
            '身高中位数': self._df['身高(cm)'].median(),
        }
        self._results['basic'] = stats
        return stats

    def grade_statistics(self) -> pd.DataFrame:
        grade_stats = self._df.groupby('年级').agg({
            '身高(cm)': ['count', 'mean', 'std', 'min', 'max'],
            '体重(kg)': ['mean', 'std']
        }).round(2)

        grade_stats.columns = ['人数', '平均身高', '身高标准差', '最矮身高', '最高身高', '平均体重', '体重标准差']
        grade_stats = grade_stats.reindex(GRADE_ORDER)

        self._results['by_grade'] = grade_stats
        return grade_stats

    def gender_statistics(self) -> pd.DataFrame:
        gender_stats = self._df.groupby(['年级', '性别'])['身高(cm)'].agg(['count', 'mean', 'std']).round(2)
        gender_stats.columns = ['人数', '平均身高', '标准差']

        self._results['by_gender'] = gender_stats
        return gender_stats

    def age_statistics(self) -> pd.DataFrame:
        age_stats = self._df.groupby('年龄')['身高(cm)'].agg(['count', 'mean', 'std', 'min', 'max']).round(2)
        age_stats.columns = ['人数', '平均身高', '标准差', '最矮身高', '最高身高']

        self._results['by_age'] = age_stats
        return age_stats

    def height_distribution(self) -> Dict[str, int]:
        df_temp = self._df.copy()
        df_temp['身高段'] = pd.cut(
            df_temp['身高(cm)'],
            bins=HEIGHT_BINS,
            labels=HEIGHT_LABELS,
            right=False
        )
        distribution = df_temp['身高段'].value_counts().sort_index().to_dict()

        self._results['height_distribution'] = distribution
        return distribution

    def growth_analysis(self) -> pd.DataFrame:
        grade_means = self._df.groupby('年级')['身高(cm)'].mean()
        grade_means = grade_means.reindex(GRADE_ORDER)

        growth_data = []
        for i in range(1, len(GRADE_ORDER)):
            prev_grade = GRADE_ORDER[i - 1]
            curr_grade = GRADE_ORDER[i]
            growth = grade_means[curr_grade] - grade_means[prev_grade]
            growth_data.append({
                '年级段': f"{prev_grade}到{curr_grade}",
                '身高增长(cm)': round(growth, 2),
                '增长率(%)': round(growth / grade_means[prev_grade] * 100, 2)
            })

        growth_df = pd.DataFrame(growth_data)
        self._results['growth'] = growth_df
        return growth_df

    def percentile_analysis(self) -> pd.DataFrame:
        percentile_data = []
        for grade in GRADE_ORDER:
            grade_data = self._df[self._df['年级'] == grade]['身高(cm)']
            row: Dict[str, Any] = {'年级': grade}
            for p in PERCENTILES:
                row[f'P{p}'] = round(np.percentile(grade_data, p), 1)
            percentile_data.append(row)

        percentile_df = pd.DataFrame(percentile_data)
        self._results['percentiles'] = percentile_df
        return percentile_df

    def bmi_analysis(self) -> Tuple[Dict[str, int], pd.DataFrame]:
        df_bmi = self._df_with_bmi

        bmi_dist = df_bmi['BMI分类'].value_counts().to_dict()
        bmi_by_grade = pd.crosstab(df_bmi['年级'], df_bmi['BMI分类'])
        bmi_by_grade = bmi_by_grade.reindex(GRADE_ORDER)

        self._results['bmi_distribution'] = bmi_dist
        self._results['bmi_by_grade'] = bmi_by_grade

        return bmi_dist, bmi_by_grade

    def compare_with_standard(self) -> pd.DataFrame:
        comparison_data = []
        for grade in GRADE_ORDER:
            for gender in ['男', '女']:
                actual_mean = self._df[
                    (self._df['年级'] == grade) & (self._df['性别'] == gender)
                ]['身高(cm)'].mean()
                standard = STANDARD_HEIGHTS[grade][gender]
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


if __name__ == "__main__":
    from utils import DataLoader, PathManager

    path_manager = PathManager()
    df = DataLoader.load(path_manager.data_file)
    analyzer = StudentHeightAnalyzer(df)
    results = analyzer.run_all_analysis()
    print("分析完成，结果键:", list(results.keys()))
