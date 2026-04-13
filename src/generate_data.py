import random
from typing import List, Dict, Tuple, Any

import pandas as pd
import numpy as np

from config import (
    SURNAMES, GIVEN_NAMES, GRADE_ORDER,
    GRADE_AGE_RANGE, GRADE_TO_NUM, HEIGHT_STATS
)


def generate_student_data(n: int = 1000, random_seed: int = 42) -> pd.DataFrame:
    np.random.seed(random_seed)
    random.seed(random_seed)

    data: List[Dict[str, Any]] = []
    student_id = 10001

    for _ in range(n):
        grade = random.choice(GRADE_ORDER)
        age_range = GRADE_AGE_RANGE[grade]
        age = random.randint(age_range[0], age_range[1])

        gender = random.choice(['男', '女'])

        mean, std = HEIGHT_STATS[grade][gender]
        height = np.random.normal(mean, std)
        height = round(height, 1)

        bmi_base = 16 if age < 9 else 17
        weight = (height / 100) ** 2 * np.random.normal(bmi_base, 1.5)
        weight = round(weight, 1)

        name = random.choice(SURNAMES) + random.choice(GIVEN_NAMES)

        grade_num = GRADE_TO_NUM[grade]
        year = 2024 - (grade_num - 1)
        month = random.randint(9, 12) if grade_num == 1 else random.randint(1, 12)
        day = random.randint(1, 28)
        enrollment_date = f"{year}-{month:02d}-{day:02d}"

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
    df.to_excel(filepath, index=False, engine='openpyxl')
    print(f"数据已保存至: {filepath}")


if __name__ == "__main__":
    df = generate_student_data(n=1000)

    output_path = "../data/student_height_data.xlsx"
    save_to_excel(df, output_path)

    print("\n数据预览（前10条）:")
    print(df.head(10))
    print(f"\n数据总量: {len(df)} 条")
    print(f"\n数据统计:")
    print(df.describe())
