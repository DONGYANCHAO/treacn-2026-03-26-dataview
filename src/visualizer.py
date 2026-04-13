#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from typing import Optional

from config import (
    GRADE_ORDER,
    GRADE_COLORS,
    GENDER_COLORS,
    BMI_COLORS,
    GENERAL_COLORS,
    FIGURE_SIZES,
    HEIGHT_HISTOGRAM_BINS
)
from utils import (
    setup_chinese_font,
    apply_plot_style,
    add_value_labels,
    save_plot,
    add_bmi_columns,
    reindex_by_grade
)

setup_chinese_font()


class HeightVisualizer:
    def __init__(self, df: pd.DataFrame, output_dir: str = "../output") -> None:
        self._df = df.copy()
        self._output_dir = output_dir
        self._df_with_bmi: Optional[pd.DataFrame] = None
        os.makedirs(output_dir, exist_ok=True)

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def df_with_bmi(self) -> pd.DataFrame:
        if self._df_with_bmi is None:
            self._df_with_bmi = add_bmi_columns(self._df)
        return self._df_with_bmi

    def _get_grade_means(self) -> pd.Series:
        grade_means = self._df.groupby('年级')['身高(cm)'].mean()
        return reindex_by_grade(grade_means)

    def plot_height_by_grade(self, save: bool = True) -> None:
        fig, ax = plt.subplots(figsize=FIGURE_SIZES['default'])

        grade_means = self._get_grade_means()

        bars = ax.bar(
            GRADE_ORDER,
            grade_means,
            color=GRADE_COLORS,
            edgecolor='black',
            linewidth=1.2
        )

        add_value_labels(bars, ax, decimals=1, unit='cm')

        apply_plot_style(
            ax,
            xlabel='年级',
            ylabel='平均身高 (cm)',
            title='各年级学生平均身高分布'
        )
        ax.set_ylim(0, max(grade_means) * 1.15)

        if save:
            save_plot(fig, self._output_dir, 'height_by_grade.png')

    def plot_height_by_gender(self, save: bool = True) -> None:
        fig, ax = plt.subplots(figsize=FIGURE_SIZES['wide'])

        gender_stats = self._df.groupby(['年级', '性别'])['身高(cm)'].mean().unstack()
        gender_stats = reindex_by_grade(gender_stats)

        x = np.arange(len(GRADE_ORDER))
        width = 0.35

        bars1 = ax.bar(
            x - width/2,
            gender_stats['男'],
            width,
            label='男',
            color=GENDER_COLORS['男'],
            edgecolor='black'
        )
        bars2 = ax.bar(
            x + width/2,
            gender_stats['女'],
            width,
            label='女',
            color=GENDER_COLORS['女'],
            edgecolor='black'
        )

        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2.,
                    height,
                    f'{height:.1f}',
                    ha='center',
                    va='bottom',
                    fontsize=9
                )

        apply_plot_style(
            ax,
            xlabel='年级',
            ylabel='平均身高 (cm)',
            title='各年级男女生平均身高对比'
        )
        ax.set_xticks(x)
        ax.set_xticklabels(GRADE_ORDER)
        ax.legend(fontsize=11)

        if save:
            save_plot(fig, self._output_dir, 'height_by_gender.png')

    def plot_height_distribution(self, save: bool = True) -> None:
        fig, ax = plt.subplots(figsize=FIGURE_SIZES['wide'])

        ax.hist(
            self._df['身高(cm)'],
            bins=HEIGHT_HISTOGRAM_BINS,
            color='#5DADE2',
            edgecolor='black',
            alpha=0.7
        )

        mean_height = self._df['身高(cm)'].mean()
        median_height = self._df['身高(cm)'].median()

        ax.axvline(
            mean_height,
            color=GENERAL_COLORS['mean'],
            linestyle='--',
            linewidth=2,
            label=f'平均值: {mean_height:.1f}cm'
        )
        ax.axvline(
            median_height,
            color=GENERAL_COLORS['median'],
            linestyle='--',
            linewidth=2,
            label=f'中位数: {median_height:.1f}cm'
        )

        apply_plot_style(
            ax,
            xlabel='身高 (cm)',
            ylabel='人数',
            title='学生身高分布直方图'
        )
        ax.legend(fontsize=10)

        if save:
            save_plot(fig, self._output_dir, 'height_distribution.png')

    def plot_boxplot_by_grade(self, save: bool = True) -> None:
        fig, ax = plt.subplots(figsize=FIGURE_SIZES['wide'])

        data_by_grade = [
            self._df[self._df['年级'] == grade]['身高(cm)'].values
            for grade in GRADE_ORDER
        ]

        box_plot = ax.boxplot(
            data_by_grade,
            labels=GRADE_ORDER,
            patch_artist=True
        )

        for patch, color in zip(box_plot['boxes'], GRADE_COLORS):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        apply_plot_style(
            ax,
            xlabel='年级',
            ylabel='身高 (cm)',
            title='各年级学生身高分布箱线图'
        )

        if save:
            save_plot(fig, self._output_dir, 'boxplot_by_grade.png')

    def plot_growth_trend(self, save: bool = True) -> None:
        fig, ax = plt.subplots(figsize=FIGURE_SIZES['wide'])

        overall_means = self._get_grade_means()
        ax.plot(
            GRADE_ORDER,
            overall_means,
            marker='o',
            linewidth=3,
            markersize=10,
            color=GENERAL_COLORS['overall'],
            label='总体平均',
            markerfacecolor='white',
            markeredgewidth=2
        )

        male_means = self._df[self._df['性别'] == '男'].groupby('年级')['身高(cm)'].mean()
        male_means = reindex_by_grade(male_means)
        ax.plot(
            GRADE_ORDER,
            male_means,
            marker='s',
            linewidth=2.5,
            markersize=8,
            color=GENERAL_COLORS['male'],
            label='男生',
            linestyle='--'
        )

        female_means = self._df[self._df['性别'] == '女'].groupby('年级')['身高(cm)'].mean()
        female_means = reindex_by_grade(female_means)
        ax.plot(
            GRADE_ORDER,
            female_means,
            marker='^',
            linewidth=2.5,
            markersize=8,
            color=GENERAL_COLORS['female'],
            label='女生',
            linestyle='--'
        )

        for i, (grade, height) in enumerate(zip(GRADE_ORDER, overall_means)):
            ax.annotate(
                f'{height:.1f}cm',
                (i, height),
                textcoords="offset points",
                xytext=(0, 10),
                ha='center',
                fontsize=9,
                fontweight='bold'
            )

        apply_plot_style(
            ax,
            xlabel='年级',
            ylabel='平均身高 (cm)',
            title='各年级身高生长趋势',
            grid_axis='both'
        )
        ax.legend(fontsize=11, loc='upper left')

        if save:
            save_plot(fig, self._output_dir, 'growth_trend.png')

    def plot_scatter_age_height(self, save: bool = True) -> None:
        fig, ax = plt.subplots(figsize=FIGURE_SIZES['wide'])

        for gender in ['男', '女']:
            data = self._df[self._df['性别'] == gender]
            ax.scatter(
                data['年龄'],
                data['身高(cm)'],
                c=GENDER_COLORS[gender],
                alpha=0.6,
                s=50,
                label=gender,
                edgecolors='white',
                linewidth=0.5
            )

        z = np.polyfit(self._df['年龄'], self._df['身高(cm)'], 1)
        p = np.poly1d(z)
        ax.plot(
            sorted(self._df['年龄'].unique()),
            p(sorted(self._df['年龄'].unique())),
            "r--",
            alpha=0.8,
            linewidth=2,
            label='趋势线'
        )

        apply_plot_style(
            ax,
            xlabel='年龄 (岁)',
            ylabel='身高 (cm)',
            title='年龄与身高关系散点图',
            grid_axis='both'
        )
        ax.legend(fontsize=11)

        if save:
            save_plot(fig, self._output_dir, 'scatter_age_height.png')

    def plot_bmi_distribution(self, save: bool = True) -> None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZES['extra_wide'])

        df_bmi = self.df_with_bmi
        bmi_counts = df_bmi['BMI分类'].value_counts()

        explode = (0.05, 0, 0, 0)
        wedges, texts, autotexts = ax1.pie(
            bmi_counts,
            labels=bmi_counts.index,
            autopct='%1.1f%%',
            colors=BMI_COLORS,
            explode=explode,
            shadow=True,
            startangle=90,
            textprops={'fontsize': 11}
        )
        ax1.set_title(
            'BMI分布比例',
            fontsize=14,
            fontweight='bold',
            pad=20
        )

        bmi_by_grade = pd.crosstab(df_bmi['年级'], df_bmi['BMI分类'])
        bmi_by_grade = reindex_by_grade(bmi_by_grade)

        bmi_by_grade.plot(
            kind='bar',
            ax=ax2,
            color=BMI_COLORS,
            width=0.8
        )
        apply_plot_style(
            ax2,
            xlabel='年级',
            ylabel='人数',
            title='各年级BMI分布'
        )
        ax2.legend(title='BMI分类', fontsize=9)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)

        if save:
            save_plot(fig, self._output_dir, 'bmi_distribution.png')

    def plot_height_heatmap(self, save: bool = True) -> None:
        fig, ax = plt.subplots(figsize=FIGURE_SIZES['square'])

        pivot_table = self._df.pivot_table(
            values='身高(cm)',
            index='年级',
            columns='性别',
            aggfunc='mean'
        )
        pivot_table = reindex_by_grade(pivot_table)

        im = ax.imshow(pivot_table.values, cmap='YlOrRd', aspect='auto')

        ax.set_xticks(np.arange(len(pivot_table.columns)))
        ax.set_yticks(np.arange(len(pivot_table.index)))
        ax.set_xticklabels(pivot_table.columns)
        ax.set_yticklabels(pivot_table.index)

        for i in range(len(pivot_table.index)):
            for j in range(len(pivot_table.columns)):
                ax.text(
                    j,
                    i,
                    f'{pivot_table.iloc[i, j]:.1f}',
                    ha="center",
                    va="center",
                    color="black",
                    fontweight='bold'
                )

        ax.set_title(
            '各年级男女生平均身高热力图',
            fontsize=14,
            fontweight='bold',
            pad=20
        )
        ax.set_xlabel('性别', fontsize=12, fontweight='bold')
        ax.set_ylabel('年级', fontsize=12, fontweight='bold')

        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('身高 (cm)', fontsize=11)

        if save:
            save_plot(fig, self._output_dir, 'height_heatmap.png')

    def generate_all_plots(self) -> None:
        print("=" * 60)
        print("开始生成可视化图表...")
        print("=" * 60)

        self.plot_height_by_grade()
        self.plot_height_by_gender()
        self.plot_height_distribution()
        self.plot_boxplot_by_grade()
        self.plot_growth_trend()
        self.plot_scatter_age_height()
        self.plot_bmi_distribution()
        self.plot_height_heatmap()

        print("\n" + "=" * 60)
        print(f"所有图表已保存至: {self._output_dir}")
        print("=" * 60)
