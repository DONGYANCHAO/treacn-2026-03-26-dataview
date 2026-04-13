import os
from typing import Optional, List

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from config import (
    GRADE_ORDER, COLORS_GRADE, COLOR_MALE, COLOR_FEMALE,
    COLOR_OVERALL, COLORS_BMI, COLOR_HISTOGRAM, COLORMAP_HEATMAP,
    FONT_SIZE_TITLE, FONT_SIZE_LABEL, FONT_SIZE_LEGEND,
    FONT_SIZE_ANNOTATION, FONT_SIZE_VALUE_LABEL, FONT_WEIGHT_BOLD,
    FIGURE_SIZE_WIDE, FIGURE_SIZE_STANDARD, FIGURE_SIZE_HEATMAP,
    FIGURE_SIZE_BMI, DPI, GRID_ALPHA, GRID_LINESTYLE,
    BAR_WIDTH, BAR_EDGE_WIDTH, SCATTER_ALPHA, SCATTER_SIZE,
    LINE_WIDTH_MAIN, LINE_WIDTH_SECONDARY, MARKER_SIZE_MAIN,
    MARKER_SIZE_SECONDARY, REPORT_LINE_WIDTH
)
from utils import (
    setup_chinese_font, apply_common_style, add_value_labels,
    add_value_labels_with_unit, save_figure, calculate_bmi, classify_bmi
)


class HeightVisualizer:
    """身高数据可视化类"""

    def __init__(self, df: pd.DataFrame, output_dir: str = "../output"):
        self._df = df.copy()
        self._output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        setup_chinese_font()

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @property
    def output_dir(self) -> str:
        return self._output_dir

    def _get_grade_means(self) -> pd.Series:
        return self._df.groupby('年级')['身高(cm)'].mean().reindex(GRADE_ORDER)

    def _get_gender_stats(self) -> pd.DataFrame:
        gender_stats = self._df.groupby(['年级', '性别'])['身高(cm)'].mean().unstack()
        return gender_stats.reindex(GRADE_ORDER)

    def plot_height_by_grade(self, save: bool = True) -> Optional[str]:
        fig, ax = plt.subplots(figsize=FIGURE_SIZE_STANDARD)

        grade_means = self._get_grade_means()
        bars = ax.bar(
            GRADE_ORDER, grade_means,
            color=COLORS_GRADE,
            edgecolor='black',
            linewidth=BAR_EDGE_WIDTH
        )

        add_value_labels_with_unit(ax, bars, unit='cm', fontsize=FONT_SIZE_VALUE_LABEL)

        apply_common_style(
            ax,
            title='各年级学生平均身高分布',
            xlabel='年级',
            ylabel='平均身高 (cm)'
        )
        ax.set_ylim(0, max(grade_means) * 1.15)

        plt.tight_layout()
        if save:
            return save_figure(fig, self._output_dir, 'height_by_grade.png', DPI)
        plt.show()
        return None

    def plot_height_by_gender(self, save: bool = True) -> Optional[str]:
        fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)

        gender_stats = self._get_gender_stats()
        x = np.arange(len(GRADE_ORDER))

        bars1 = ax.bar(
            x - BAR_WIDTH / 2, gender_stats['男'], BAR_WIDTH,
            label='男', color=COLOR_MALE, edgecolor='black'
        )
        bars2 = ax.bar(
            x + BAR_WIDTH / 2, gender_stats['女'], BAR_WIDTH,
            label='女', color=COLOR_FEMALE, edgecolor='black'
        )

        for bars in [bars1, bars2]:
            add_value_labels(ax, bars, fontsize=FONT_SIZE_ANNOTATION)

        apply_common_style(
            ax,
            title='各年级男女生平均身高对比',
            xlabel='年级',
            ylabel='平均身高 (cm)'
        )
        ax.set_xticks(x)
        ax.set_xticklabels(GRADE_ORDER)
        ax.legend(fontsize=FONT_SIZE_LEGEND)

        plt.tight_layout()
        if save:
            return save_figure(fig, self._output_dir, 'height_by_gender.png', DPI)
        plt.show()
        return None

    def plot_height_distribution(self, save: bool = True) -> Optional[str]:
        fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)

        bins = range(100, 170, 5)
        ax.hist(
            self._df['身高(cm)'], bins=bins,
            color=COLOR_HISTOGRAM, edgecolor='black', alpha=0.7
        )

        mean_height = self._df['身高(cm)'].mean()
        median_height = self._df['身高(cm)'].median()

        ax.axvline(
            mean_height, color='red', linestyle='--', linewidth=2,
            label=f'平均值: {mean_height:.1f}cm'
        )
        ax.axvline(
            median_height, color='green', linestyle='--', linewidth=2,
            label=f'中位数: {median_height:.1f}cm'
        )

        apply_common_style(
            ax,
            title='学生身高分布直方图',
            xlabel='身高 (cm)',
            ylabel='人数'
        )
        ax.legend(fontsize=FONT_SIZE_LEGEND)

        plt.tight_layout()
        if save:
            return save_figure(fig, self._output_dir, 'height_distribution.png', DPI)
        plt.show()
        return None

    def plot_boxplot_by_grade(self, save: bool = True) -> Optional[str]:
        fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)

        data_by_grade = [
            self._df[self._df['年级'] == grade]['身高(cm)'].values
            for grade in GRADE_ORDER
        ]

        box_plot = ax.boxplot(data_by_grade, labels=GRADE_ORDER, patch_artist=True)

        for patch, color in zip(box_plot['boxes'], COLORS_GRADE):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        apply_common_style(
            ax,
            title='各年级学生身高分布箱线图',
            xlabel='年级',
            ylabel='身高 (cm)'
        )

        plt.tight_layout()
        if save:
            return save_figure(fig, self._output_dir, 'boxplot_by_grade.png', DPI)
        plt.show()
        return None

    def plot_growth_trend(self, save: bool = True) -> Optional[str]:
        fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)

        overall_means = self._get_grade_means()
        ax.plot(
            GRADE_ORDER, overall_means,
            marker='o', linewidth=LINE_WIDTH_MAIN, markersize=MARKER_SIZE_MAIN,
            color=COLOR_OVERALL, label='总体平均',
            markerfacecolor='white', markeredgewidth=2
        )

        male_means = self._df[self._df['性别'] == '男'].groupby('年级')['身高(cm)'].mean().reindex(GRADE_ORDER)
        ax.plot(
            GRADE_ORDER, male_means,
            marker='s', linewidth=LINE_WIDTH_SECONDARY, markersize=MARKER_SIZE_SECONDARY,
            color=COLOR_MALE, label='男生', linestyle='--'
        )

        female_means = self._df[self._df['性别'] == '女'].groupby('年级')['身高(cm)'].mean().reindex(GRADE_ORDER)
        ax.plot(
            GRADE_ORDER, female_means,
            marker='^', linewidth=LINE_WIDTH_SECONDARY, markersize=MARKER_SIZE_SECONDARY,
            color=COLOR_FEMALE, label='女生', linestyle='--'
        )

        for i, (grade, height) in enumerate(zip(GRADE_ORDER, overall_means)):
            ax.annotate(
                f'{height:.1f}cm', (i, height),
                textcoords="offset points",
                xytext=(0, 10), ha='center',
                fontsize=FONT_SIZE_ANNOTATION, fontweight=FONT_WEIGHT_BOLD
            )

        apply_common_style(
            ax,
            title='各年级身高生长趋势',
            xlabel='年级',
            ylabel='平均身高 (cm)'
        )
        ax.legend(fontsize=FONT_SIZE_LEGEND, loc='upper left')
        ax.grid(True, alpha=GRID_ALPHA, linestyle=GRID_LINESTYLE)

        plt.tight_layout()
        if save:
            return save_figure(fig, self._output_dir, 'growth_trend.png', DPI)
        plt.show()
        return None

    def plot_scatter_age_height(self, save: bool = True) -> Optional[str]:
        fig, ax = plt.subplots(figsize=FIGURE_SIZE_WIDE)

        colors = {'男': COLOR_MALE, '女': COLOR_FEMALE}
        for gender in ['男', '女']:
            data = self._df[self._df['性别'] == gender]
            ax.scatter(
                data['年龄'], data['身高(cm)'],
                c=colors[gender], alpha=SCATTER_ALPHA, s=SCATTER_SIZE,
                label=gender, edgecolors='white', linewidth=0.5
            )

        z = np.polyfit(self._df['年龄'], self._df['身高(cm)'], 1)
        p = np.poly1d(z)
        ax.plot(
            sorted(self._df['年龄'].unique()),
            p(sorted(self._df['年龄'].unique())),
            "r--", alpha=0.8, linewidth=2, label='趋势线'
        )

        apply_common_style(
            ax,
            title='年龄与身高关系散点图',
            xlabel='年龄 (岁)',
            ylabel='身高 (cm)'
        )
        ax.legend(fontsize=FONT_SIZE_LEGEND)
        ax.grid(True, alpha=GRID_ALPHA, linestyle=GRID_LINESTYLE)

        plt.tight_layout()
        if save:
            return save_figure(fig, self._output_dir, 'scatter_age_height.png', DPI)
        plt.show()
        return None

    def plot_bmi_distribution(self, save: bool = True) -> Optional[str]:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=FIGURE_SIZE_BMI)

        df_bmi = self._df.copy()
        df_bmi['BMI'] = df_bmi.apply(
            lambda x: calculate_bmi(x['体重(kg)'], x['身高(cm)']),
            axis=1
        )
        df_bmi['BMI分类'] = df_bmi['BMI'].apply(classify_bmi)
        bmi_counts = df_bmi['BMI分类'].value_counts()

        explode = (0.05, 0, 0, 0)
        wedges, texts, autotexts = ax1.pie(
            bmi_counts, labels=bmi_counts.index, autopct='%1.1f%%',
            colors=COLORS_BMI, explode=explode, shadow=True,
            startangle=90, textprops={'fontsize': FONT_SIZE_LEGEND}
        )
        ax1.set_title('BMI分布比例', fontsize=FONT_SIZE_TITLE, fontweight=FONT_WEIGHT_BOLD, pad=20)

        bmi_by_grade = pd.crosstab(df_bmi['年级'], df_bmi['BMI分类'])
        bmi_by_grade = bmi_by_grade.reindex(GRADE_ORDER)

        bmi_by_grade.plot(kind='bar', ax=ax2, color=COLORS_BMI, width=0.8)
        ax2.set_xlabel('年级', fontsize=FONT_SIZE_LABEL, fontweight=FONT_WEIGHT_BOLD)
        ax2.set_ylabel('人数', fontsize=FONT_SIZE_LABEL, fontweight=FONT_WEIGHT_BOLD)
        ax2.set_title('各年级BMI分布', fontsize=FONT_SIZE_TITLE, fontweight=FONT_WEIGHT_BOLD, pad=20)
        ax2.legend(title='BMI分类', fontsize=FONT_SIZE_ANNOTATION)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
        ax2.grid(axis='y', alpha=GRID_ALPHA, linestyle=GRID_LINESTYLE)

        plt.tight_layout()
        if save:
            return save_figure(fig, self._output_dir, 'bmi_distribution.png', DPI)
        plt.show()
        return None

    def plot_height_heatmap(self, save: bool = True) -> Optional[str]:
        fig, ax = plt.subplots(figsize=FIGURE_SIZE_HEATMAP)

        pivot_table = self._df.pivot_table(
            values='身高(cm)', index='年级', columns='性别', aggfunc='mean'
        )
        pivot_table = pivot_table.reindex(GRADE_ORDER)

        im = ax.imshow(pivot_table.values, cmap=COLORMAP_HEATMAP, aspect='auto')

        ax.set_xticks(np.arange(len(pivot_table.columns)))
        ax.set_yticks(np.arange(len(pivot_table.index)))
        ax.set_xticklabels(pivot_table.columns)
        ax.set_yticklabels(pivot_table.index)

        for i in range(len(pivot_table.index)):
            for j in range(len(pivot_table.columns)):
                ax.text(
                    j, i, f'{pivot_table.iloc[i, j]:.1f}',
                    ha="center", va="center", color="black", fontweight=FONT_WEIGHT_BOLD
                )

        ax.set_title('各年级男女生平均身高热力图', fontsize=FONT_SIZE_TITLE, fontweight=FONT_WEIGHT_BOLD, pad=20)
        ax.set_xlabel('性别', fontsize=FONT_SIZE_LABEL, fontweight=FONT_WEIGHT_BOLD)
        ax.set_ylabel('年级', fontsize=FONT_SIZE_LABEL, fontweight=FONT_WEIGHT_BOLD)

        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('身高 (cm)', fontsize=FONT_SIZE_LABEL)

        plt.tight_layout()
        if save:
            return save_figure(fig, self._output_dir, 'height_heatmap.png', DPI)
        plt.show()
        return None

    def generate_all_plots(self) -> List[str]:
        print("=" * REPORT_LINE_WIDTH)
        print("开始生成可视化图表...")
        print("=" * REPORT_LINE_WIDTH)

        saved_files = []
        saved_files.append(self.plot_height_by_grade())
        saved_files.append(self.plot_height_by_gender())
        saved_files.append(self.plot_height_distribution())
        saved_files.append(self.plot_boxplot_by_grade())
        saved_files.append(self.plot_growth_trend())
        saved_files.append(self.plot_scatter_age_height())
        saved_files.append(self.plot_bmi_distribution())
        saved_files.append(self.plot_height_heatmap())

        print("\n" + "=" * REPORT_LINE_WIDTH)
        print(f"所有图表已保存至: {self._output_dir}")
        print("=" * REPORT_LINE_WIDTH)

        return [f for f in saved_files if f is not None]


if __name__ == "__main__":
    from utils import DataLoader, PathManager

    path_manager = PathManager()
    df = DataLoader.load(path_manager.data_file)
    visualizer = HeightVisualizer(df, output_dir=path_manager.output)
    visualizer.generate_all_plots()
