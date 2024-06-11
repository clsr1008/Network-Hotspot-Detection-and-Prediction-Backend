# Generated by Django 4.2.13 on 2024-06-11 02:46
import os
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo

def Stamp2Time(timestamp):
    # 将Unix时间戳转换为UTC datetime对象
    utc_time = datetime.fromtimestamp(timestamp, tz=ZoneInfo("UTC"))
    # 转换为本地时区（这里以 "Asia/Shanghai" 为例）
    local_time = utc_time.astimezone(ZoneInfo("Asia/Shanghai"))
    # 使用 strftime 方法格式化时间
    formatted_time = local_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

def load_initial_brief_data(apps, schema_editor):
    CrawlBriefData = apps.get_model("crawl", 'CrawlBriefData')

    initial_brief_data = []
    crawl_data_dict = './crawl_data_csv'
    crawl_dir = os.listdir(crawl_data_dict)
    csv_list = [file for file in crawl_dir if os.path.isfile(os.path.join(crawl_data_dict, file))]

    # csv list name
    csv_names = [os.path.splitext(csv)[0] for csv in csv_list]
    index = 1
    for csv_name in csv_names:
        num = 0
        csv_file_path = os.path.join(crawl_data_dict, csv_name+'.csv')
        print(csv_file_path)

        # get csv name as source
        if csv_name[-1] == 'l':
            continue
        encoding = 'utf-8'
        if csv_name[0] == '中':
            csv_name = csv_name[4:]
            if csv_name[-1] == 'n':
                csv_name = csv_name[:-11]
        else:
            csv_name = csv_name.split("_")[0]

        # get csv row number
        if csv_name[-2] == '凰' or csv_name[-2] == '讯':
            encoding = 'gb2312'

        # csv list count
        print("time: " + Stamp2Time(os.path.getctime(csv_file_path)))
        df = pd.read_csv(csv_file_path, encoding=encoding, encoding_errors="ignore")
        initial_brief_data.append({
            'no': index,
            'name': csv_name,
            'number': df.shape[0],
            'last_update_time': Stamp2Time(os.path.getctime(csv_file_path)),
        })
        index += 1
    CrawlBriefData.objects.bulk_create([
        CrawlBriefData(**data) for data in initial_brief_data
    ])
