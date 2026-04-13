"""
报表生成模块 - 格式化输出分析结果
"""

from typing import Any, Dict, Optional, Union

import pandas as pd

from analyzer import StudentHeightAnalyzer


class ReportGenerator:
    """
    报表生成器类

    负责将分析结果格式化为可读性强的文本输出。
    分离了数据分析和输出展示的职责。
    """

    def __init__(self, analyzer: StudentHeightAnalyzer) -> None:
        """
        初始化报表生成器

        Args:
            analyzer: 学生身高分析器实例
        """
        self._analyzer = analyzer

    def generate_full_report(self) -> Dict[str, Any]:
        """
        生成完整分析报告

        Returns:
            所有分析结果的字典
        """
        self._print_header("小学生身高数据分析报告")

        results = self._analyzer.run_all_analysis()

        self._print_section("一、基础统计", results.get('basic'))
        self._print_section("二、年级统计", results.get('by_grade'))
        self._print_section("三、性别统计", results.get('by_gender'))
        self._print_section("四、年龄统计", results.get('by_age'))
        self._print_section("五、身高分布", results.get('height_distribution'))
        self._print_section("六、生长趋势分析", results.get('growth'))
        self._print_section("七、身高百分位数", results.get('percentiles'))
        self._print_bmi_section(results)
        self._print_section("九、与标准身高对比", results.get('standard_comparison'))

        self._print_footer()

        return results

    def _print_header(self, title: str) -> None:
        """打印报告标题"""
        print("=" * 60)
        print(title)
        print("=" * 60)

    def _print_footer(self) -> None:
        """打印报告结尾"""
        print("\n" + "=" * 60)
        print("分析完成！")
        print("=" * 60)

    def _print_section(self, title: str, data: Any) -> None:
        """
        打印单个分析部分

        Args:
            title: 部分标题
            data: 数据内容
        """
        print(f"\n【{title}】")

        if data is None:
            print("  暂无数据")
            return

        if isinstance(data, dict):
            self._print_dict_data(data)
        elif isinstance(data, pd.DataFrame):
            print(data)
        else:
            print(data)

    def _print_dict_data(self, data: Dict[str, Any]) -> None:
        """
        打印字典格式的数据

        Args:
            data: 字典数据
        """
        for key, value in data.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")

    def _print_bmi_section(self, results: Dict[str, Any]) -> None:
        """
        打印BMI分析部分

        Args:
            results: 分析结果字典
        """
        print("\n【八、BMI分析】")

        bmi_dist = results.get('bmi_distribution')
        bmi_by_grade = results.get('bmi_by_grade')

        if bmi_dist:
            print("BMI分布:")
            for key, value in bmi_dist.items():
                print(f"  {key}: {value}人")

        if bmi_by_grade is not None:
            print("\n各年级BMI分布:")
            print(bmi_by_grade)

    def print_basic_stats(self) -> None:
        """打印基础统计信息"""
        stats = self._analyzer.basic_statistics()
        self._print_section("基础统计", stats)

    def print_grade_stats(self) -> None:
        """打印年级统计信息"""
        stats = self._analyzer.grade_statistics()
        self._print_section("年级统计", stats)

    def print_gender_stats(self) -> None:
        """打印性别统计信息"""
        stats = self._analyzer.gender_statistics()
        self._print_section("性别统计", stats)

    def print_age_stats(self) -> None:
        """打印年龄统计信息"""
        stats = self._analyzer.age_statistics()
        self._print_section("年龄统计", stats)

    def print_height_distribution(self) -> None:
        """打印身高分布信息"""
        dist = self._analyzer.height_distribution()
        self._print_section("身高分布", dist)

    def print_growth_analysis(self) -> None:
        """打印生长趋势分析"""
        growth = self._analyzer.growth_analysis()
        self._print_section("生长趋势分析", growth)

    def print_percentile_analysis(self) -> None:
        """打印百分位数分析"""
        percentiles = self._analyzer.percentile_analysis()
        self._print_section("身高百分位数", percentiles)

    def print_bmi_analysis(self) -> None:
        """打印BMI分析"""
        bmi_dist, bmi_by_grade = self._analyzer.bmi_analysis()
        results = {
            'bmi_distribution': bmi_dist,
            'bmi_by_grade': bmi_by_grade
        }
        self._print_bmi_section(results)

    def print_standard_comparison(self) -> None:
        """打印与标准身高对比"""
        comparison = self._analyzer.compare_with_standard()
        self._print_section("与标准身高对比", comparison)


def generate_report(analyzer: StudentHeightAnalyzer) -> Dict[str, Any]:
    """
    快速生成完整报告的便捷函数

    Args:
        analyzer: 学生身高分析器实例

    Returns:
        所有分析结果的字典
    """
    generator = ReportGenerator(analyzer)
    return generator.generate_full_report()
