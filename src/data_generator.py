"""
数据生成模块 - 生成学生身高模拟数据
"""

import random
from typing import Optional

import numpy as np
import pandas as pd

import config
from utils import generate_enrollment_date, generate_random_name


def generate_student_data(
    n: int = config.DEFAULT_SAMPLE_SIZE,
    random_seed: int = config.DEFAULT_RANDOM_SEED
) -> pd.DataFrame:
    """
    生成小学生身高模拟数据

    Args:
        n: 生成数据条数，默认1000
        random_seed: 随机种子，保证可重复性

    Returns:
        包含学生信息的DataFrame
    """
    np.random.seed(random_seed)
    random_gen = random.Random(random_seed)

    data = []
    student_id = 10001

    for _ in range(n):
        grade = random_gen.choice(config.GRADE_ORDER)
        age_range = config.GRADE_AGE_RANGE[grade]
        age = random_gen.randint(age_range[0], age_range[1])

        gender = random_gen.choice(['男', '女'])

        mean, std = config.HEIGHT_STATS[grade][gender]
        height = np.random.normal(mean, std)
        height = round(height, 1)

        bmi_base = config.BMI_BMI_BASE_BY_AGE.get(age, 16.5)
        weight = (height / 100) ** 2 * np.random.normal(bmi_base, 1.5)
        weight = round(weight, 1)

        name = generate_random_name(random_gen)
        enrollment_date = generate_enrollment_date(grade, random_gen)

        data.append({
            '学生ID': student_id,
            '姓名': name,
            '性别': gender,
            '年级': grade,
            '年龄': age,
            '身高(cm)': height,
            '体重(kg)': weight,
            '入学日期': enrollment_date
        })

        student_id += 1

    return pd.DataFrame(data)


def save_to_excel(df: pd.DataFrame, filepath: str) -> None:
    """
    将数据保存为Excel文件

    Args:
        df: DataFrame数据
        filepath: 保存路径
    """
    from utils import ensure_dir
    ensure_dir(filepath)
    df.to_excel(filepath, index=False, engine='openpyxl')
    print(f"数据已保存至: {filepath}")


if __name__ == "__main__":
    df = generate_student_data(n=1000)
    output_path = "../data/student_height_data.xlsx"
    save_to_excel(df, output_path)

    print("\n数据预览（前10条）:")
    print(df.head(10))
    print(f"\n数据总量: {len(df)} 条")
    print("\n数据统计:")
    print(df.describe())
