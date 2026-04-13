#!/usr/bin/env python3

import pandas as pd
import numpy as np
from functools import lru_cache
from typing import Dict, Tuple, Any

from config import (
    GRADE_ORDER,
    STANDARD_HEIGHTS,
    HEIGHT_BINS,
    HEIGHT_LABELS,
    PERCENTILES
)
from utils import add_bmi_columns, reindex_by_grade


class StudentHeightAnalyzer:
    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df.copy()
        self._results: Dict[str, Any] = {}
        self._basic_stats: Optional[Dict[str, Any]] = None
        self._grade_stats: Optional[pd.DataFrame] = None
        self._gender_stats: Optional[pd.DataFrame] = None
        self._age_stats: Optional[pd.DataFrame] = None
        self._height_dist: Optional[Dict[str, int]] = None
        self._growth_df: Optional[pd.DataFrame] = None
        self._percentile_df: Optional[pd.DataFrame] = None
        self._bmi_dist: Optional[Dict[str, int]] = None
        self._bmi_by_grade: Optional[pd.DataFrame] = None
        self._comparison_df: Optional[pd.DataFrame] = None
        self._df_with_bmi: Optional[pd.DataFrame] = None

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def df_with_bmi(self) -> pd.DataFrame:
        if self._df_with_bmi is None:
            self._df_with_bmi = add_bmi_columns(self._df)
        return self._df_with_bmi

    @property
    def basic_stats(self) -> Dict[str, Any]:
        if self._basic_stats is None:
            self._basic_stats = self._calculate_basic_stats()
        return self._basic_stats

    def _calculate_basic_stats(self) -> Dict[str, Any]:
        return {
            '总人数': len(self._df),
            '男生人数': len(self._df[self._df['性别'] == '男']),
            '女生人数': len(self._df[self._df['性别'] == '女']),
            '平均身高': round(self._df['身高(cm)'].mean(), 2),
            '身高标准差': round(self._df['身高(cm)'].std(), 2),
            '身高最小值': self._df['身高(cm)'].min(),
            '身高最大值': self._df['身高(cm)'].max(),
            '身高中位数': self._df['身高(cm)'].median(),
        }

    @property
    def grade_stats(self) -> pd.DataFrame:
        if self._grade_stats is None:
            self._grade_stats = self._calculate_grade_stats()
        return self._grade_stats

    def _calculate_grade_stats(self) -> pd.DataFrame:
        grade_stats = self._df.groupby('年级').agg({
            '身高(cm)': ['count', 'mean', 'std', 'min', 'max'],
            '体重(kg)': ['mean', 'std']
        }).round(2)

        grade_stats.columns = ['人数', '平均身高', '身高标准差', '最矮身高', '最高身高', '平均体重', '体重标准差']
        return reindex_by_grade(grade_stats)

    @property
    def gender_stats(self) -> pd.DataFrame:
        if self._gender_stats is None:
            self._gender_stats = self._calculate_gender_stats()
        return self._gender_stats

    def _calculate_gender_stats(self) -> pd.DataFrame:
        gender_stats = self._df.groupby(['年级', '性别'])['身高(cm)'].agg(
            ['count', 'mean', 'std']
        ).round(2)
        gender_stats.columns = ['人数', '平均身高', '标准差']
        return gender_stats

    @property
    def age_stats(self) -> pd.DataFrame:
        if self._age_stats is None:
            self._age_stats = self._calculate_age_stats()
        return self._age_stats

    def _calculate_age_stats(self) -> pd.DataFrame:
        age_stats = self._df.groupby('年龄')['身高(cm)'].agg(
            ['count', 'mean', 'std', 'min', 'max']
        ).round(2)
        age_stats.columns = ['人数', '平均身高', '标准差', '最矮身高', '最高身高']
        return age_stats

    @property
    def height_distribution(self) -> Dict[str, int]:
        if self._height_dist is None:
            self._height_dist = self._calculate_height_distribution()
        return self._height_dist

    def _calculate_height_distribution(self) -> Dict[str, int]:
        df_copy = self._df.copy()
        df_copy['身高段'] = pd.cut(
            df_copy['身高(cm)'],
            bins=HEIGHT_BINS,
            labels=HEIGHT_LABELS,
            right=False
        )
        return df_copy['身高段'].value_counts().sort_index().to_dict()

    @property
    def growth_analysis(self) -> pd.DataFrame:
        if self._growth_df is None:
            self._growth_df = self._calculate_growth()
        return self._growth_df

    def _calculate_growth(self) -> pd.DataFrame:
        grade_means = self._df.groupby('年级')['身高(cm)'].mean()
        grade_means = reindex_by_grade(grade_means)

        growth_data = []
        for i in range(1, len(GRADE_ORDER)):
            prev_grade = GRADE_ORDER[i-1]
            curr_grade = GRADE_ORDER[i]
            growth = grade_means[curr_grade] - grade_means[prev_grade]
            growth_data.append({
                '年级段': f"{prev_grade}到{curr_grade}",
                '身高增长(cm)': round(growth, 2),
                '增长率(%)': round(growth / grade_means[prev_grade] * 100, 2)
            })

        return pd.DataFrame(growth_data)

    @property
    def percentile_analysis(self) -> pd.DataFrame:
        if self._percentile_df is None:
            self._percentile_df = self._calculate_percentiles()
        return self._percentile_df

    def _calculate_percentiles(self) -> pd.DataFrame:
        percentile_data = []
        for grade in GRADE_ORDER:
            grade_data = self._df[self._df['年级'] == grade]['身高(cm)']
            row = {'年级': grade}
            for p in PERCENTILES:
                row[f'P{p}'] = round(np.percentile(grade_data, p), 1)
            percentile_data.append(row)

        return pd.DataFrame(percentile_data)

    @property
    def bmi_analysis(self) -> Tuple[Dict[str, int], pd.DataFrame]:
        if self._bmi_dist is None or self._bmi_by_grade is None:
            self._bmi_dist, self._bmi_by_grade = self._calculate_bmi()
        return self._bmi_dist, self._bmi_by_grade

    def _calculate_bmi(self) -> Tuple[Dict[str, int], pd.DataFrame]:
        df_with_bmi = self.df_with_bmi
        bmi_dist = df_with_bmi['BMI分类'].value_counts().to_dict()
        bmi_by_grade = pd.crosstab(df_with_bmi['年级'], df_with_bmi['BMI分类'])
        bmi_by_grade = reindex_by_grade(bmi_by_grade)
        return bmi_dist, bmi_by_grade

    @property
    def standard_comparison(self) -> pd.DataFrame:
        if self._comparison_df is None:
            self._comparison_df = self._calculate_standard_comparison()
        return self._comparison_df

    def _calculate_standard_comparison(self) -> pd.DataFrame:
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

        return pd.DataFrame(comparison_data)

    def run_all_analysis(self) -> Dict[str, Any]:
        self._results['basic'] = self.basic_stats
        self._results['by_grade'] = self.grade_stats
        self._results['by_gender'] = self.gender_stats
        self._results['by_age'] = self.age_stats
        self._results['height_distribution'] = self.height_distribution
        self._results['growth'] = self.growth_analysis
        self._results['percentiles'] = self.percentile_analysis
        self._results['bmi_distribution'], self._results['bmi_by_grade'] = self.bmi_analysis
        self._results['standard_comparison'] = self.standard_comparison

        return self._results
