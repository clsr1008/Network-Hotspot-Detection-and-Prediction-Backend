import openai
from openai import OpenAI
import logging
import time
logging.basicConfig(level=logging.INFO)
models = ['gpt-3.5-turbo-1106']
def askgpt(text):
    """
    askgpt(用于调用chatgpt并返回结果，包括生成的文本、目前剩余quests和目前剩余token(这里的剩余指的是在60s内)
    由于有限速，所以要判断remain_request, remain_tokens的情况
    为了加速，增加了两个机制：
    1. api key自动切换机制，通过最晚调用时间来对api key进行排序，优先使用最晚调用时间最早的api key
    2. model自动切换机制，发现openai对不同模型的限制是分开计算的
    """

    max_retries = 2  # 最大重试次数
    retry_delay = 10  # 初始重试延迟（秒）
    max_retry_delay = 60  # 最大重试延迟（秒）

    # 从优先级队列中获取最晚调用时间最早的 API 密钥
    
    client = OpenAI(api_key='sk-NFxr7dzBKJT5f0vM6f717eFb23924aB4Af2d1e1bB3604bCc',base_url="https://api.xiaoai.plus/v1")

    # 尝试所有模型
    for model in models:
        retry_count = 0
        while retry_count < max_retries:
            try:
                response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": text}],
                response_format= {"type":"json_object"},
                timeout=max_retry_delay)
                return response.choices[0].message.content,response.model
            except openai.APIConnectionError as e:
                logging.info(f"An error occurred: {str(e)}")
            except openai.RateLimitError as e:
                logging.info(f"Rate limit exceeded: {str(e)}")
            except openai.BadRequestError as e:
                logging.info(f"Invalid request: {str(e)}")
            except openai.AuthenticationError as e:
                logging.info(f"Authentication error: {str(e)}")
            except openai.OpenAIError as e:
                logging.info(f"An error occurred: {str(e)}")
            retry_count += 1
            time.sleep(retry_delay)

    logging.info("Failed to complete request after exponential backoff.")
    return None, None

def getExtraJson(text):
    res,model = askgpt(text) 
    return res
with open('prompt.txt', 'r', encoding='utf-8') as f:
    prompt = f.read()
title = '中山大学获校友捐赠1亿元'
content = '中山大学今年迎来百岁华诞。17日，中山大学校友伉俪林斌、刘向东向中山大学捐赠1亿元庆祝母校百年华诞。据介绍，林斌、刘向东均为中山大学1986级校友，其中林斌现为小米集团联合创始人、副董事长，刘向东为林斌刘向东基金会理事长。'

prompt = prompt.replace('（在此处插入文章内容）', content)
print(prompt)
print(getExtraJson(prompt))