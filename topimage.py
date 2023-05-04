import requests
import os
import time
import uuid
from random import randint
from tqdm import tqdm

# 这个方法是你要爬的人在ins上首页的12张照片集，最后会输出一个rext_max_id(下一页的id)，用于你放到loadimage.py的next_max_id里

target_dir = ""  #输入你要保存的路径，如果路径不存在会自动创建 / Enter the path where you want to save the files, it will be automatically created if it does not exist
username = ''  #输入你要获取图片的博主的username / Enter the username of the blogger whose pictures you want to retrieve/
cookie = ''#输入你通过游览器获得的请求cookie / Enter the cookie in RequestHeaders



if not os.path.exists(target_dir):
    os.makedirs(target_dir)

# 设置请求头
headers = {
    'x-ig-app-id': '936619743392459',
    'cookie': cookie
}

retry_count = 0

# 发送请求
while retry_count < 3:
    try:
        response = requests.get(
            url=f'https://www.instagram.com/api/v1/feed/user/{username}/username/?count=12',
            headers=headers,
            verify=False)
        break
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        retry_count += 1
        if retry_count >= 3:
            print("重试次数超过3次，程序退出")
            exit()
        print(f"重试第{retry_count}次...")
        time.sleep(5)

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
                time.sleep(randint(2, 4))
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

print("==========全部下载完毕,rext_max_id=", r['next_max_id'],"，这个id为这个博主第二页的next_max_id，你可以将它复制到loadimage.py的next_max_id里进行接下去的下载==========")