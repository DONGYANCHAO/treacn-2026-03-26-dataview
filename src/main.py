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

import os
import sys
import argparse
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import REPORT_LINE_WIDTH
from utils import PathManager, DataLoader, check_dependencies
from analyzer import StudentHeightAnalyzer
from report import ReportGenerator
from visualizer import HeightVisualizer
from generate_data import generate_student_data, save_to_excel


def generate_data(paths: PathManager, n: int = 1000) -> str:
    print("\n" + "=" * REPORT_LINE_WIDTH)
    print("步骤 1: 生成模拟数据")
    print("=" * REPORT_LINE_WIDTH)

    data_file = paths.data_file

    print(f"正在生成 {n} 条学生身高数据...")
    df = generate_student_data(n=n)

    print(f"正在保存数据到: {data_file}")
    save_to_excel(df, data_file)

    print("\n数据预览（前10条）:")
    print(df.head(10).to_string())
    print(f"\n数据总量: {len(df)} 条")

    return data_file


def analyze_data(df) -> StudentHeightAnalyzer:
    print("\n" + "=" * REPORT_LINE_WIDTH)
    print("步骤 2: 数据分析")
    print("=" * REPORT_LINE_WIDTH)

    analyzer = StudentHeightAnalyzer(df)
    report = ReportGenerator(analyzer)
    report.generate_full_report()

    return analyzer


def visualize_data(df, output_dir: str) -> None:
    print("\n" + "=" * REPORT_LINE_WIDTH)
    print("步骤 3: 数据可视化")
    print("=" * REPORT_LINE_WIDTH)

    visualizer = HeightVisualizer(df, output_dir=output_dir)
    visualizer.generate_all_plots()


def run_full_pipeline(n: int = 1000, skip_generation: bool = False) -> None:
    paths = PathManager()
    paths.ensure_dirs()

    data_file = paths.data_file

    if not skip_generation or not os.path.exists(data_file):
        data_file = generate_data(paths, n=n)
    else:
        print(f"\n使用已有数据文件: {data_file}")

    df = DataLoader.load(data_file)

    analyze_data(df)

    visualize_data(df, paths.output)

    ReportGenerator.print_completion_message(data_file, paths.output)


def main() -> None:
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

    deps_ok, missing = check_dependencies()
    if not deps_ok:
        print("错误: 缺少以下依赖包:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\n请使用以下命令安装:")
        print(f"  pip install {' '.join(missing)}")
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
