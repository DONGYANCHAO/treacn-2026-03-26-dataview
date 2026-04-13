#!/usr/bin/env python3
"""
小学生身高数据分析与可视化系统

本程序用于分析小学各年级学生的身高数据，包括：
- 基础统计分析
- 年级、性别、年龄分组分析
- 生长趋势分析
- BMI分析
- 数据可视化图表生成

作者: AI Assistant
日期: 2026-03-26
"""

import argparse
import os
import sys
from typing import Optional

import config
from analyzer import StudentHeightAnalyzer
from data_generator import generate_student_data, save_to_excel
from report import ReportGenerator
from utils import (
    check_dependencies, ensure_dir, get_data_file_path,
    get_output_path, get_project_paths, load_data
)
from visualizer import HeightVisualizer


def get_project_paths_wrapper() -> dict:
    """获取项目各目录路径的包装函数"""
    return get_project_paths()


def check_dependencies_wrapper() -> bool:
    """检查依赖包的包装函数"""
    is_ok, missing = check_dependencies()
    if not is_ok:
        print("错误: 缺少以下依赖包:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\n请使用以下命令安装:")
        print(f"  pip install {' '.join(missing)}")
        return False
    return True


def generate_data(paths: dict, n: int = 1000) -> str:
    """
    生成模拟数据

    Args:
        paths: 项目路径字典
        n: 生成数据条数

    Returns:
        数据文件路径
    """
    print("\n" + "=" * 60)
    print("步骤 1: 生成模拟数据")
    print("=" * 60)

    data_file = os.path.join(paths['data'], config.DEFAULT_DATA_FILENAME)
    ensure_dir(paths['data'])

    print(f"正在生成 {n} 条学生身高数据...")
    df = generate_student_data(n=n)

    print(f"正在保存数据到: {data_file}")
    save_to_excel(df, data_file)

    print("\n数据预览（前10条）:")
    print(df.head(10).to_string())
    print(f"\n数据总量: {len(df)} 条")

    return data_file


def analyze_data(data_file: str) -> StudentHeightAnalyzer:
    """
    执行数据分析

    Args:
        data_file: 数据文件路径

    Returns:
        分析器实例
    """
    print("\n" + "=" * 60)
    print("步骤 2: 数据分析")
    print("=" * 60)

    df = load_data(data_file)
    analyzer = StudentHeightAnalyzer(df)

    generator = ReportGenerator(analyzer)
    generator.generate_full_report()

    return analyzer


def visualize_data(data_file: str, output_dir: str) -> None:
    """
    生成可视化图表

    Args:
        data_file: 数据文件路径
        output_dir: 输出目录
    """
    print("\n" + "=" * 60)
    print("步骤 3: 数据可视化")
    print("=" * 60)

    df = load_data(data_file)
    visualizer = HeightVisualizer(df, output_dir=output_dir)
    visualizer.generate_all_plots()


def run_full_pipeline(n: int = 1000, skip_generation: bool = False) -> None:
    """
    运行完整的数据分析流程

    Args:
        n: 生成的数据条数
        skip_generation: 是否跳过数据生成步骤
    """
    paths = get_project_paths_wrapper()

    for dir_path in [paths['data'], paths['output']]:
        ensure_dir(dir_path)

    data_file = os.path.join(paths['data'], config.DEFAULT_DATA_FILENAME)

    if not skip_generation or not os.path.exists(data_file):
        data_file = generate_data(paths, n=n)
    else:
        print(f"\n使用已有数据文件: {data_file}")

    analyze_data(data_file)
    visualize_data(data_file, paths['output'])

    print("\n" + "=" * 60)
    print("所有任务已完成！")
    print("=" * 60)
    print(f"\n输出文件位置:")
    print(f"  - 数据文件: {data_file}")
    print(f"  - 图表文件: {paths['output']}/")
    print("\n生成的图表包括:")
    print("  1. height_by_grade.png - 各年级平均身高柱状图")
    print("  2. height_by_gender.png - 男女生身高对比图")
    print("  3. height_distribution.png - 身高分布直方图")
    print("  4. boxplot_by_grade.png - 各年级身高箱线图")
    print("  5. growth_trend.png - 生长趋势折线图")
    print("  6. scatter_age_height.png - 年龄身高散点图")
    print("  7. bmi_distribution.png - BMI分布图")
    print("  8. height_heatmap.png - 身高热力图")
    print("=" * 60)


def main() -> None:
    """主函数"""
    parser = argparse.ArgumentParser(
        description='小学生身高数据分析与可视化系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py                    # 运行完整流程（默认生成1000条数据）
  python main.py -n 500             # 生成500条数据并分析
  python main.py -s                 # 跳过数据生成，使用已有数据
  python main.py -n 2000 -s         # 生成2000条数据，但跳过生成步骤
        """
    )

    parser.add_argument(
        '-n', '--number',
        type=int,
        default=1000,
        help='生成的数据条数（默认: 1000）'
    )

    parser.add_argument(
        '-s', '--skip-generation',
        action='store_true',
        help='跳过数据生成步骤，使用已有数据文件'
    )

    args = parser.parse_args()

    if not check_dependencies_wrapper():
        sys.exit(1)

    try:
        run_full_pipeline(n=args.number, skip_generation=args.skip_generation)
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
