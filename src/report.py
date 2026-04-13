#!/usr/bin/env python3

from typing import Dict, Any
from analyzer import StudentHeightAnalyzer


class ReportGenerator:
    def __init__(self, analyzer: StudentHeightAnalyzer) -> None:
        self.analyzer = analyzer

    def print_basic_stats(self) -> None:
        print("\n【一、基础统计】")
        for key, value in self.analyzer.basic_stats.items():
            print(f"  {key}: {value}")

    def print_grade_stats(self) -> None:
        print("\n【二、年级统计】")
        print(self.analyzer.grade_stats)

    def print_gender_stats(self) -> None:
        print("\n【三、性别统计】")
        print(self.analyzer.gender_stats)

    def print_age_stats(self) -> None:
        print("\n【四、年龄统计】")
        print(self.analyzer.age_stats)

    def print_height_distribution(self) -> None:
        print("\n【五、身高分布】")
        for key, value in self.analyzer.height_distribution.items():
            print(f"  {key}: {value}人")

    def print_growth_analysis(self) -> None:
        print("\n【六、生长趋势分析】")
        print(self.analyzer.growth_analysis)

    def print_percentile_analysis(self) -> None:
        print("\n【七、身高百分位数】")
        print(self.analyzer.percentile_analysis)

    def print_bmi_analysis(self) -> None:
        print("\n【八、BMI分析】")
        bmi_dist, bmi_by_grade = self.analyzer.bmi_analysis
        print("BMI分布:")
        for key, value in bmi_dist.items():
            print(f"  {key}: {value}人")
        print("\n各年级BMI分布:")
        print(bmi_by_grade)

    def print_standard_comparison(self) -> None:
        print("\n【九、与标准身高对比】")
        print(self.analyzer.standard_comparison)

    def generate_full_report(self) -> Dict[str, Any]:
        print("=" * 60)
        print("小学生身高数据分析报告")
        print("=" * 60)

        self.print_basic_stats()
        self.print_grade_stats()
        self.print_gender_stats()
        self.print_age_stats()
        self.print_height_distribution()
        self.print_growth_analysis()
        self.print_percentile_analysis()
        self.print_bmi_analysis()
        self.print_standard_comparison()

        print("\n" + "=" * 60)
        print("分析完成！")
        print("=" * 60)

        return self.analyzer.run_all_analysis()
