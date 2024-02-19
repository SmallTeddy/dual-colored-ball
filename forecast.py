import requests
import json
import random
import pandas as pd

cookies = {
    'HMF_CI': '9e661dfdf867a0f0e754cadb110695b96f656f6188d9407dba8b499d07a1fc377b9f271aea4955645e06c7f04d08cea10664b0cba3ece782e2144e8debfca933c5',
    '21_vq': '28',
}

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Referer': 'https://www.cwl.gov.cn/ygkj/wqkjgg/ssq/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

params = {
    'name': 'ssq',
    'issueCount': '',
    'issueStart': '',
    'issueEnd': '',
    'dayStart': '',
    'dayEnd': '',
    'pageNo': '1',
    'pageSize': '3000',
    'week': '',
    'systemType': 'PC',
}

response = requests.get(
    'https://www.cwl.gov.cn/cwl_admin/front/cwlkj/search/kjxx/findDrawNotice',
    params=params,
    cookies=cookies,
    headers=headers,
).json()
formatted_json = json.dumps(response, indent=4, ensure_ascii=False)

# with open('双色球历史数据.json', 'w', encoding='utf-8') as f:
#     f.write(formatted_json)

# 将JSON字符串转换为Python字典
data_dict = json.loads(formatted_json)

# 创建一个空的DataFrame来存储红球和蓝球数据
red_balls = []
blue_balls = []

# 遍历结果列表
for result in data_dict['result']:
    red_balls.append(result['red'])
    blue_balls.append(result['blue'])

# 将列表转换为DataFrame
red_df = pd.DataFrame(red_balls, columns=['Red'])
blue_df = pd.DataFrame(blue_balls, columns=['Blue'])

# 分析红球的出现频率
red_frequency = red_df['Red'].value_counts().sort_index()

# 分析蓝球的出现频率
blue_frequency = blue_df['Blue'].value_counts().sort_index()

# 预测下一次可能出现的红球
next_red = red_frequency.sample(10, random_state=1).index.tolist()

# 预测下一次可能出现的蓝球
next_blue = blue_frequency.sample(10, random_state=1).index.tolist()

# 创建一个DataFrame来存储预测结果
red_predictions_df = pd.DataFrame(columns=['Red1', 'Red2', 'Red3', 'Red4', 'Red5', 'Red6'])
blue_predictions_df = pd.DataFrame(next_blue, columns=['Blue'])


# 定义一个函数来转换单个数字为两位数的字符串
def convert_to_two_digit(number):
    return str(number).zfill(2)


# 遍历红球字符串列表，分割字符串并填充到DataFrame
for i, balls_str in enumerate(next_red):
    # 分割字符串并转换为列表
    balls_list = balls_str.split(',')
    # 转换为两位数的字符串并填充到DataFrame
    red_predictions_df.loc[i] = [convert_to_two_digit(ball) for ball in balls_list]

# 遍历蓝球字符串列表，填充到DataFrame
for i, ball_str in enumerate(next_blue):
    # 蓝球已经是两位数的字符串，直接填充
    ball = convert_to_two_digit(int(ball_str))
    blue_predictions_df.loc[i] = [ball]

# 合并红球和蓝球的预测结果
predictions_df = pd.concat([red_predictions_df, blue_predictions_df], axis=1)

def generate_unique_numbers(df):
    # 初始化一个空集合来存储已选择的号码
    selected_numbers = set()

    # 从Red1到Red6列中随机选择号码，直到所有号码都不同
    for i in range(1, 7):
        while True:
            number = random.choice(df[f'Red{i}'].dropna().unique())
            if number not in selected_numbers:
                selected_numbers.add(number)
                break

    # 从Blue列中随机选择一个号码
    blue_number = random.choice(df['Blue'].dropna().unique())

    # 返回选择的号码列表
    return list(selected_numbers) + [blue_number]


forecast_numbers = generate_unique_numbers(predictions_df)

# 使用sorted()函数对列表进行排序，但不包括最后一个元素
forecast_list = sorted(forecast_numbers[:-1])

# 将最后一个元素添加到排序后的列表末尾
forecast_list.append(forecast_numbers[-1])

# 打印预览表
print(forecast_list)

