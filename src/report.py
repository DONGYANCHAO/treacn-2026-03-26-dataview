from typing import Dict, Any

import pandas as pd

from config import REPORT_LINE_WIDTH
from analyzer import StudentHeightAnalyzer


class ReportGenerator:
    """报表生成器 - 负责格式化输出分析结果"""

    def __init__(self, analyzer: StudentHeightAnalyzer):
        self._analyzer = analyzer

    def print_separator(self, char: str = "=", width: int = REPORT_LINE_WIDTH) -> None:
        print(char * width)

    def print_section_header(self, title: str) -> None:
        print(f"\n【{title}】")

    def print_basic_statistics(self) -> None:
        stats = self._analyzer.basic_statistics()
        self.print_section_header("一、基础统计")
        for key, value in stats.items():
            print(f"  {key}: {value}")

    def print_grade_statistics(self) -> None:
        grade_stats = self._analyzer.grade_statistics()
        self.print_section_header("二、年级统计")
        print(grade_stats)

    def print_gender_statistics(self) -> None:
        gender_stats = self._analyzer.gender_statistics()
        self.print_section_header("三、性别统计")
        print(gender_stats)

    def print_age_statistics(self) -> None:
        age_stats = self._analyzer.age_statistics()
        self.print_section_header("四、年龄统计")
        print(age_stats)

    def print_height_distribution(self) -> None:
        dist = self._analyzer.height_distribution()
        self.print_section_header("五、身高分布")
        for key, value in dist.items():
            print(f"  {key}: {value}人")

    def print_growth_analysis(self) -> None:
        growth = self._analyzer.growth_analysis()
        self.print_section_header("六、生长趋势分析")
        print(growth)

    def print_percentile_analysis(self) -> None:
        percentiles = self._analyzer.percentile_analysis()
        self.print_section_header("七、身高百分位数")
        print(percentiles)

    def print_bmi_analysis(self) -> None:
        bmi_dist, bmi_by_grade = self._analyzer.bmi_analysis()
        self.print_section_header("八、BMI分析")
        print("BMI分布:")
        for key, value in bmi_dist.items():
            print(f"  {key}: {value}人")
        print("\n各年级BMI分布:")
        print(bmi_by_grade)

    def print_standard_comparison(self) -> None:
        comparison = self._analyzer.compare_with_standard()
        self.print_section_header("九、与标准身高对比")
        print(comparison)

    def generate_full_report(self) -> Dict[str, Any]:
        self.print_separator()
        print("小学生身高数据分析报告")
        self.print_separator()

        self.print_basic_statistics()
        self.print_grade_statistics()
        self.print_gender_statistics()
        self.print_age_statistics()
        self.print_height_distribution()
        self.print_growth_analysis()
        self.print_percentile_analysis()
        self.print_bmi_analysis()
        self.print_standard_comparison()

        self.print_separator()
        print("分析完成！")
        self.print_separator()

        return self._analyzer.results

    @staticmethod
    def print_completion_message(data_file: str, output_dir: str) -> None:
        print("\n" + "=" * REPORT_LINE_WIDTH)
        print("所有任务已完成！")
        print("=" * REPORT_LINE_WIDTH)
        print(f"\n输出文件位置:")
        print(f"  - 数据文件: {data_file}")
        print(f"  - 图表文件: {output_dir}/")
        print("\n生成的图表包括:")
        print("  1. height_by_grade.png - 各年级平均身高柱状图")
        print("  2. height_by_gender.png - 男女生身高对比图")
        print("  3. height_distribution.png - 身高分布直方图")
        print("  4. boxplot_by_grade.png - 各年级身高箱线图")
        print("  5. growth_trend.png - 生长趋势折线图")
        print("  6. scatter_age_height.png - 年龄身高散点图")
        print("  7. bmi_distribution.png - BMI分布图")
        print("  8. height_heatmap.png - 身高热力图")
        print("=" * REPORT_LINE_WIDTH)


if __name__ == "__main__":
    from utils import DataLoader, PathManager

    path_manager = PathManager()
    df = DataLoader.load(path_manager.data_file)
    analyzer = StudentHeightAnalyzer(df)
    report = ReportGenerator(analyzer)
    report.generate_full_report()
