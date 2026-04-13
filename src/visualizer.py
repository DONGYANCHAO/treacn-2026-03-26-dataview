"""
可视化模块 - 学生身高数据可视化器
"""

from typing import Any, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import config
from utils import (
    add_value_labels, apply_common_style, get_output_path,
    reorder_grade_index, save_figure, setup_chinese_font
)


class HeightVisualizer:
    """
    身高数据可视化类

    该类负责所有图表的生成和保存，不包含任何数据分析逻辑。
    所有方法接受数据作为参数，不直接访问数据源。
    """

    def __init__(self, df: pd.DataFrame, output_dir: Optional[str] = None) -> None:
        """
        初始化可视化器

        Args:
            df: 学生数据DataFrame
            output_dir: 图表输出目录，默认为项目output目录
        """
        self._df: pd.DataFrame = df.copy()
        self._output_dir: str = output_dir or get_output_path('')
        setup_chinese_font()

    def _create_figure(self, figsize: Tuple[int, int] = config.FIGURE_SIZE_DEFAULT) -> Tuple[Figure, Axes]:
        """
        创建图表和轴对象

        Args:
            figsize: 图表尺寸

        Returns:
            (Figure, Axes)元组
        """
        fig, ax = plt.subplots(figsize=figsize)
        return fig, ax

    def _save_and_show(self, fig: Figure, filename: str, save: bool = True) -> None:
        """
        保存并显示图表

        Args:
            fig: 图表对象
            filename: 保存文件名
            save: 是否保存
        """
        plt.tight_layout()
        if save:
            filepath = get_output_path(filename)
            save_figure(fig, filepath)
        plt.show()

    def plot_height_by_grade(self, save: bool = True) -> Figure:
        """
        各年级平均身高柱状图

        Args:
            save: 是否保存图表

        Returns:
            图表对象
        """
        fig, ax = self._create_figure(config.FIGURE_SIZE_SMALL)

        grade_means = self._df.groupby('年级')['身高(cm)'].mean().reindex(config.GRADE_ORDER)

        bars = ax.bar(
            config.GRADE_ORDER,
            grade_means,
            color=config.COLORS_GRADE,
            edgecolor='black',
            linewidth=1.2
        )

        add_value_labels(ax, bars, fmt='{:.1f}cm', fontsize=10)

        ax.set_ylim(0, max(grade_means) * 1.15)
        apply_common_style(
            ax,
            title='各年级学生平均身高分布',
            xlabel='年级',
            ylabel='平均身高 (cm)'
        )

        self._save_and_show(fig, 'height_by_grade.png', save)
        return fig

    def plot_height_by_gender(self, save: bool = True) -> Figure:
        """
        男女身高对比图

        Args:
            save: 是否保存图表

        Returns:
            图表对象
        """
        fig, ax = self._create_figure()

        gender_stats = self._df.groupby(['年级', '性别'])['身高(cm)'].mean().unstack()
        gender_stats = gender_stats.reindex(config.GRADE_ORDER)

        x = np.arange(len(config.GRADE_ORDER))
        width = 0.35

        bars1 = ax.bar(
            x - width / 2,
            gender_stats['男'],
            width,
            label='男',
            color=config.COLOR_MALE,
            edgecolor='black'
        )
        bars2 = ax.bar(
            x + width / 2,
            gender_stats['女'],
            width,
            label='女',
            color=config.COLOR_FEMALE,
            edgecolor='black'
        )

        for bars in [bars1, bars2]:
            add_value_labels(ax, bars, fmt='{:.1f}', fontsize=9)

        ax.set_xticks(x)
        ax.set_xticklabels(config.GRADE_ORDER)
        ax.legend(fontsize=config.FONT_SIZE_LEGEND)

        apply_common_style(
            ax,
            title='各年级男女生平均身高对比',
            xlabel='年级',
            ylabel='平均身高 (cm)'
        )

        self._save_and_show(fig, 'height_by_gender.png', save)
        return fig

    def plot_height_distribution(self, save: bool = True) -> Figure:
        """
        身高分布直方图

        Args:
            save: 是否保存图表

        Returns:
            图表对象
        """
        fig, ax = self._create_figure()

        ax.hist(
            self._df['身高(cm)'],
            bins=list(config.HEIGHT_HIST_BINS),
            color=config.COLOR_DISTRIBUTION,
            edgecolor='black',
            alpha=0.7
        )

        mean_height = self._df['身高(cm)'].mean()
        median_height = self._df['身高(cm)'].median()

        ax.axvline(
            mean_height,
            color='red',
            linestyle='--',
            linewidth=2,
            label=f'平均值: {mean_height:.1f}cm'
        )
        ax.axvline(
            median_height,
            color='green',
            linestyle='--',
            linewidth=2,
            label=f'中位数: {median_height:.1f}cm'
        )

        ax.legend(fontsize=config.FONT_SIZE_LEGEND)
        apply_common_style(
            ax,
            title='学生身高分布直方图',
            xlabel='身高 (cm)',
            ylabel='人数'
        )

        self._save_and_show(fig, 'height_distribution.png', save)
        return fig

    def plot_boxplot_by_grade(self, save: bool = True) -> Figure:
        """
        各年级身高箱线图

        Args:
            save: 是否保存图表

        Returns:
            图表对象
        """
        fig, ax = self._create_figure()

        data_by_grade = [
            self._df[self._df['年级'] == grade]['身高(cm)'].values
            for grade in config.GRADE_ORDER
        ]

        box_plot = ax.boxplot(
            data_by_grade,
            labels=config.GRADE_ORDER,
            patch_artist=True
        )

        for patch, color in zip(box_plot['boxes'], config.COLORS_GRADE):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        apply_common_style(
            ax,
            title='各年级学生身高分布箱线图',
            xlabel='年级',
            ylabel='身高 (cm)'
        )

        self._save_and_show(fig, 'boxplot_by_grade.png', save)
        return fig

    def plot_growth_trend(self, save: bool = True) -> Figure:
        """
        生长趋势折线图

        Args:
            save: 是否保存图表

        Returns:
            图表对象
        """
        fig, ax = self._create_figure()

        overall_means = self._df.groupby('年级')['身高(cm)'].mean().reindex(config.GRADE_ORDER)
        ax.plot(
            config.GRADE_ORDER,
            overall_means,
            marker='o',
            linewidth=3,
            markersize=10,
            color=config.COLOR_OVERALL,
            label='总体平均',
            markerfacecolor='white',
            markeredgewidth=2
        )

        male_means = self._df[self._df['性别'] == '男'].groupby('年级')['身高(cm)'].mean()
        male_means = male_means.reindex(config.GRADE_ORDER)
        ax.plot(
            config.GRADE_ORDER,
            male_means,
            marker='s',
            linewidth=2.5,
            markersize=8,
            color=config.COLOR_MALE,
            label='男生',
            linestyle='--'
        )

        female_means = self._df[self._df['性别'] == '女'].groupby('年级')['身高(cm)'].mean()
        female_means = female_means.reindex(config.GRADE_ORDER)
        ax.plot(
            config.GRADE_ORDER,
            female_means,
            marker='^',
            linewidth=2.5,
            markersize=8,
            color=config.COLOR_FEMALE,
            label='女生',
            linestyle='--'
        )

        for i, (grade, height) in enumerate(zip(config.GRADE_ORDER, overall_means)):
            ax.annotate(
                f'{height:.1f}cm',
                (i, height),
                textcoords="offset points",
                xytext=(0, 10),
                ha='center',
                fontsize=config.FONT_SIZE_ANNOTATION,
                fontweight='bold'
            )

        ax.legend(fontsize=config.FONT_SIZE_LEGEND, loc='upper left')
        ax.grid(True, alpha=config.GRID_ALPHA, linestyle=config.GRID_LINESTYLE)

        apply_common_style(
            ax,
            title='各年级身高生长趋势',
            xlabel='年级',
            ylabel='平均身高 (cm)'
        )

        self._save_and_show(fig, 'growth_trend.png', save)
        return fig

    def plot_scatter_age_height(self, save: bool = True) -> Figure:
        """
        年龄身高散点图

        Args:
            save: 是否保存图表

        Returns:
            图表对象
        """
        fig, ax = self._create_figure()

        for gender in ['男', '女']:
            data = self._df[self._df['性别'] == gender]
            ax.scatter(
                data['年龄'],
                data['身高(cm)'],
                c=config.COLORS_GENDER[gender],
                alpha=0.6,
                s=50,
                label=gender,
                edgecolors='white',
                linewidth=0.5
            )

        z = np.polyfit(self._df['年龄'], self._df['身高(cm)'], 1)
        p = np.poly1d(z)
        unique_ages = sorted(self._df['年龄'].unique())
        ax.plot(
            unique_ages,
            p(unique_ages),
            "r--",
            alpha=0.8,
            linewidth=2,
            label='趋势线'
        )

        ax.legend(fontsize=config.FONT_SIZE_LEGEND)
        ax.grid(True, alpha=config.GRID_ALPHA, linestyle=config.GRID_LINESTYLE)

        apply_common_style(
            ax,
            title='年龄与身高关系散点图',
            xlabel='年龄 (岁)',
            ylabel='身高 (cm)'
        )

        self._save_and_show(fig, 'scatter_age_height.png', save)
        return fig

    def plot_bmi_distribution(self, save: bool = True) -> Figure:
        """
        BMI分布图（饼图+柱状图）

        Args:
            save: 是否保存图表

        Returns:
            图表对象
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=config.FIGURE_SIZE_LARGE)

        from utils import add_bmi_to_dataframe
        df_with_bmi = add_bmi_to_dataframe(self._df)
        bmi_counts = df_with_bmi['BMI分类'].value_counts()

        explode = (0.05, 0, 0, 0)
        wedges, texts, autotexts = ax1.pie(
            bmi_counts,
            labels=bmi_counts.index,
            autopct='%1.1f%%',
            colors=config.COLORS_BMI,
            explode=explode,
            shadow=True,
            startangle=90,
            textprops={'fontsize': config.FONT_SIZE_TICK}
        )
        ax1.set_title('BMI分布比例', fontsize=config.FONT_SIZE_TITLE, fontweight='bold', pad=20)

        bmi_by_grade = pd.crosstab(df_with_bmi['年级'], df_with_bmi['BMI分类'])
        bmi_by_grade = reorder_grade_index(bmi_by_grade)

        bmi_by_grade.plot(
            kind='bar',
            ax=ax2,
            color=config.COLORS_BMI,
            width=0.8
        )
        ax2.set_xlabel('年级', fontsize=config.FONT_SIZE_LABEL, fontweight='bold')
        ax2.set_ylabel('人数', fontsize=config.FONT_SIZE_LABEL, fontweight='bold')
        ax2.set_title('各年级BMI分布', fontsize=config.FONT_SIZE_TITLE, fontweight='bold', pad=20)
        ax2.legend(title='BMI分类', fontsize=9)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
        ax2.grid(axis='y', alpha=config.GRID_ALPHA, linestyle=config.GRID_LINESTYLE)

        plt.tight_layout()
        if save:
            filepath = get_output_path('bmi_distribution.png')
            save_figure(fig, filepath)
        plt.show()
        return fig

    def plot_height_heatmap(self, save: bool = True) -> Figure:
        """
        身高热力图（年级vs性别）

        Args:
            save: 是否保存图表

        Returns:
            图表对象
        """
        fig, ax = self._create_figure(config.FIGURE_SIZE_SQUARE)

        pivot_table = self._df.pivot_table(
            values='身高(cm)',
            index='年级',
            columns='性别',
            aggfunc='mean'
        )
        pivot_table = pivot_table.reindex(config.GRADE_ORDER)

        im = ax.imshow(pivot_table.values, cmap=config.COLORMAP_HEATMAP, aspect='auto')

        ax.set_xticks(np.arange(len(pivot_table.columns)))
        ax.set_yticks(np.arange(len(pivot_table.index)))
        ax.set_xticklabels(pivot_table.columns)
        ax.set_yticklabels(pivot_table.index)

        for i in range(len(pivot_table.index)):
            for j in range(len(pivot_table.columns)):
                ax.text(
                    j, i,
                    f'{pivot_table.iloc[i, j]:.1f}',
                    ha="center",
                    va="center",
                    color="black",
                    fontweight='bold'
                )

        ax.set_title(
            '各年级男女生平均身高热力图',
            fontsize=config.FONT_SIZE_TITLE,
            fontweight='bold',
            pad=20
        )
        ax.set_xlabel('性别', fontsize=config.FONT_SIZE_LABEL, fontweight='bold')
        ax.set_ylabel('年级', fontsize=config.FONT_SIZE_LABEL, fontweight='bold')

        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('身高 (cm)', fontsize=config.FONT_SIZE_LABEL)

        self._save_and_show(fig, 'height_heatmap.png', save)
        return fig

    def generate_all_plots(self) -> List[Figure]:
        """
        生成所有图表

        Returns:
            所有图表对象的列表
        """
        print("=" * 60)
        print("开始生成可视化图表...")
        print("=" * 60)

        figures: List[Figure] = [
            self.plot_height_by_grade(),
            self.plot_height_by_gender(),
            self.plot_height_distribution(),
            self.plot_boxplot_by_grade(),
            self.plot_growth_trend(),
            self.plot_scatter_age_height(),
            self.plot_bmi_distribution(),
            self.plot_height_heatmap()
        ]

        print("\n" + "=" * 60)
        print(f"所有图表已保存至: {self._output_dir}")
        print("=" * 60)

        return figures
