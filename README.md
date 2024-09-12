# Instagram_image_downloader


## 下载Instagram一个博主下所有图片

### 用法&说明： 
### topimage.py：

说明:\
运行后开始下载博主首页的12张照片集，最后会输出一个rext_max_id(下一页的id)，用于loadimage.py

用法：\
在代码中填入 target_dir（图片保存路径）、username（博主username）、cookie(输入你通过浏览器获得的请求cookie)\
username可以查看博主首页，——> https://www.instagram.com/{username}

举例：\
target_dir = "/Users/k/Documents/inpc/mitsui"\
username = 'mitsui.hisashi'\
cookie ='' 不会获取的看底部图片

### loadimage.py：

说明:\
运行后开始从目标页开始循环下载，直到最后一页，next_max_id为你本次下载目标页面的id，每一页下载完都会把下一页的next_max_id打印出来，如果中途下载中断，你可以用最后一次打印的next_max_id复制到next_max_id，重新运行


用法：\
在代码中填入 target_dir（图片保存路径）、next_max_id（下载目标页id）、user_id（博主user_id）、cookie(输入你通过浏览器获得的请求cookie)\
user_id为next_max_id“_”后面的部分

举例：\
target_dir = "/Users/k/Documents/inpc/mitsui"\
next_max_id = '3071960909401083979_57185715084'\
user_id = '57185715084'\
cookie = ''不会获取的看底部图片

### cookie获取方法，使用浏览器（2024.8更新）
![image](https://github.com/user-attachments/assets/2927a625-b0ba-4593-9119-c112204fdc88)

userid获取方法，使用浏览器（2024.8更新）
![image](https://github.com/user-attachments/assets/7e183f3c-fc25-4afe-8416-5783adc10b5d)
![image](https://github.com/user-attachments/assets/b4e6ff41-a1b7-41a4-b064-541d0527f356)




### 运行结果
![image](https://github.com/kthree0213/Instagram_image_downloader/blob/main/operationresult%20.png)
