import requests
import os
import time
import uuid
from random import randint
from tqdm import tqdm

#这个方法是从目标页开始循环下载，直到最后一页，next_max_id为你本次下载目标页面的id，每一页下载完都会把下一页的next_max_id打印出来，如果中途下载中断，你可以用最后一次打印的next_max_id复制到next_max_id，重新开始
#topimage.py最后打印出来的next_max_id，为这个博主第二页的next_max_id，可以填入下方

target_dir = ""  # 输入你要保存的路径，如果路径不存在会自动创建 / Enter the path where you want to save the files, it will be automatically created if it does not exist/
next_max_id = ''# Enter the path where you want to save the files/输入你要保存的路径
user_id = ''# 输入你要获取图片的博主的user_id,为next_max_id的'_'后面的部分'，举例next_max_id '3071960909401083979_57185715084'，user_id为'57185715084' / Enter the user_id，which is the part after the '_' in the next_max_id，for example, if the next_max_id is '3071960909401083979_57185715084', the user_id is '57185715084
cookie =  ''# 输入你通过游览器获得的请求cookie / Enter the cookie in RequestHeaders



if not os.path.exists(target_dir):
    os.makedirs(target_dir)

print(f"==========开始下载，next_max_id={next_max_id}==========")

# 设置请求头
headers = {
    'x-ig-app-id': '936619743392459',
    'cookie': cookie
}

more_available = True
retry_count = 0

while more_available:
    # 发送请求
    try:
        response = requests.get(
            url=f'https://www.instagram.com/api/v1/feed/user/{user_id}/?count=12&max_id='+next_max_id,
            headers=headers,
            verify=False)
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        # 如果重试次数超过3次，则退出程序
        if retry_count >= 3:
            print("重试次数超过3次，程序退出")
            break
        else:
            retry_count += 1
            print(f"重试第{retry_count}次...")
            time.sleep(5)
            continue

    # 如果请求正常，则将重试次数重置为0
    retry_count = 0

    # 解析返回的 JSON 数据
    r = response.json()

    count = 0
    for item in r['items']:
        if 'carousel_media' in item:
            for media in item['carousel_media']:
                candidate = media['image_versions2']['candidates'][0]
                url = candidate['url']
                count += 1
                file_name = f"{count:03d}_{uuid.uuid1()}.jpg"  # 格式化编号，使其具有固定的宽度（3位），不足则用0补齐
                file_path = os.path.join(target_dir, file_name)
                with open(file_path, 'wb') as f:
                    retry_count = 0
                    while retry_count < 3:
                        try:
                            response = requests.get(url, headers=headers, stream=True)
                            break
                        except requests.exceptions.SSLError as e:
                            print(f"请求异常: {e}")
                            retry_count += 1
                            if retry_count >= 3:
                                print("重试次数超过3次，程序退出")
                                exit()
                            print(f"重试第{retry_count}次...")
                            time.sleep(5)

                    file_size = int(response.headers.get('Content-Length', 0))
                    progress_bar = tqdm(total=file_size, unit='iB', unit_scale=True,
                                        desc=f"{count:03d}/{r['num_results']:03d}",
                                        bar_format='{desc}{bar:10}{percentage:3.0f}%|{bar}|{n_fmt}/{total_fmt} [{elapsed}<{remaining}]',
                                        colour='white')
                    for data in response.iter_content(1024):
                        progress_bar.update(len(data))
                        f.write(data)
                    progress_bar.close()

                    # 随机间隔2-4秒
                    time.sleep(randint(2, 8))
        else:
            candidate = item['image_versions2']['candidates'][0]
            url = candidate['url']
            count += 1
            file_name = f"{count:03d}_{uuid.uuid1()}.jpg"  # 格式化编号，使其具有固定的宽度（3位），不足则用0补齐
            file_path = os.path.join(target_dir, file_name)
            with open(file_path, 'wb') as f:
                retry_count = 0
                while retry_count < 3:
                    try:
                        response = requests.get(url, headers=headers, stream=True)
                        break
                    except requests.exceptions.SSLError as e:
                        print(f"请求异常: {e}")
                        retry_count += 1
                        if retry_count >= 3:
                            print("重试次数超过3次，程序退出")
                            exit()
                        print(f"重试第{retry_count}次...")
                        time.sleep(5)

                file_size = int(response.headers.get('Content-Length', 0))
                progress_bar = tqdm(total=file_size, unit='iB', unit_scale=True,
                                    desc=f"{count:03d}/{r['num_results']:03d}",
                                    bar_format='{desc}{bar:10}{percentage:3.0f}%|{bar}|{n_fmt}/{total_fmt} [{elapsed}<{remaining}]',
                                    colour='white')
                for data in response.iter_content(1024):
                    progress_bar.update(len(data))
                    f.write(data)
                progress_bar.close()

                # 随机间隔2-4秒
                time.sleep(randint(2, 4))

    # 更新max_id和more_available
    more_available = r['more_available']

    # 如果more_available为true，则暂停5秒后继续请求
    if more_available:
        next_max_id = r['next_max_id']
        print(f"==========5秒后将继续下载，next_max_id={next_max_id}, more_available={more_available}","如果下载中断直接将此next_max_id复制到next_max_id，从当前页开始继续下载==========")

        time.sleep(5)

print("==========全部下载完毕==========")
