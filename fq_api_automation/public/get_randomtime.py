import arrow
import random

def get_YYYYMMDDHHmm_randomtime():
    # 定义起始和结束日期
    start_date = arrow.get(2024, 1, 1)
    end_date = arrow.get(2035, 12, 31)

    # 生成随机天数
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date.shift(days=random_days)

    # 生成随机小时
    random_hours = random.randint(0, 23)
    # 生成随机分钟
    random_minutes = random.randint(0, 59)
    # 生成随机秒
    random_seconds = random.randint(0, 59)

    # 组合成随机时间
    random_time = random_date.replace(hour=random_hours, minute=random_minutes, second=random_seconds)

    return arrow.get(random_time).format("YYYY-MM-DD HH:mm")

if __name__ == '__main__':
    print(get_YYYYMMDDHHmm_randomtime())