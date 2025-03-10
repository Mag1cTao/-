def find_free_students(students, weekdays, max_class):
    # 生成全量时间段
    all_periods = {(day, c) for day in weekdays for c in range(1, max_class+1)}
    
    # 构建结果字典
    result = {period: [] for period in sorted(all_periods, key=lambda x: (weekdays.index(x[0]), x[1]))}
    
    # 遍历所有时间段
    for period in result.keys():
        current_day, current_class = period
        # 检查每个学生
        for name, schedule in students.items():
            # 该学生当天是否有课
            if current_day not in schedule:
                result[period].append(name)
                continue
            # 当前节次是否空闲
            if current_class not in schedule[current_day]:
                result[period].append(name)
    return result

import pandas as pd

def format_output(result):
    # 转换为DataFrame
    df = pd.DataFrame(
        [(f"{day}第{cls}节", ", ".join(names)) for (day, cls), names in result.items()],
        columns=["时间段", "空闲学生"]
    )
    
    # 按天分组展示（可选）
    df['星期'] = df['时间段'].str[:2]
    df['节次'] = df['时间段'].str.extract('(\d+)').astype(int)
    df = df.sort_values(['星期', '节次']).drop(['星期', '节次'], axis=1)
    
    return df


import pandas as pd
from collections import defaultdict

def parse_class_periods(period_str):
    """解析节次字符串为数字列表，支持格式：1 / 1,3,5 / 2-4"""
    periods = []
    for part in str(period_str).split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            periods.extend(range(start, end+1))
        else:
            if part.isdigit():
                periods.append(int(part))
    return sorted(list(set(periods)))  # 去重并排序

def read_schedule(file_path):
    """读取CSV/Excel文件并转换为课程表字典"""
    # 读取文件
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)  # Specify encoding here
    else:
        df = pd.read_excel(file_path)  # Specify encoding here
    
    # 数据清洗
    df = df.dropna()  # 删除空行
    df['星期'] = df['星期'].str.strip()  # 去除空格
    
    # 构建数据结构
    students = defaultdict(lambda: defaultdict(list))
    for _, row in df.iterrows():
        name = row['姓名']
        day = row['星期']
        periods = parse_class_periods(row['节次'])
        
        # 合并相同星期数据
        students[name][day] = sorted(list(set(students[name][day] + periods)))
    
    return dict(students)

# ----------- 使用示例 -----------
if __name__ == "__main__":
    # 从文件读取数据（支持.csv和.xlsx）
    students = read_schedule("course_schedule.xlsx")  # 或 course_schedule.csv
    
    # 后续处理（复用之前的函数）
    free_time = find_free_students(students, weekdays=["周一","周二","周三","周四","周五"], max_class=8)
    df = format_output(free_time)
    print(df.to_string(index=False))

# 输出到Excel
df.to_excel("free_time_statistics.xlsx", index=False)

# 控制台打印
print(df.to_string(index=False))
