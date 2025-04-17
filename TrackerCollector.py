import os
import sys
import requests

#获取项目路径
Project = os.path.realpath(sys.argv[0])
MainPath = os.path.dirname(Project)
MainName = os.path.basename(Project)
MainSuffix = os.path.splitext(Project)[1]

# 获取下载地址
def Read_Address():
    global address_list
    # 读取下载地址
    try:
        with open(f"{MainPath}/Address.txt","r",encoding="utf-8") as f:
            address_data = f.read()
    except FileNotFoundError:
        return False
    address_list = address_data.split("\n")
    return True

# 下载文件
def Download_File(url,file):
    try:
        print(f"[信息] [正在下载] 文件：{url}",end="")
        response = requests.get(url,timeout=10)
        with open(file, 'wb') as f:
            f.write(response.content)
        print(f"\r[信息] [下载成功] 文件：{url}")
        return True
    except Exception as error:
        print(f"\r[警告] [下载失败] 文件：{url}")
        print(f"[警告] [下载失败] 原因：{error}")
        return False

# 列表去重去空
def List_UNIQUE(original_list):
    cleaned_list = list({x for x in original_list if x or x == 0})
    return cleaned_list


#【Tracker格式转化】
def Tracker_Converted():
    print(f"[信息] 正在转化Tracker格式")
    # 读取总列表
    try:
        with open(f"{MainPath}/TrackerList.txt", "r", encoding="utf-8") as f:
            tracker_list_data = f.read()
        tracker_list = tracker_list_data.split("\n")
        tracker_list = List_UNIQUE(tracker_list)
    except FileNotFoundError:
        print(f"[错误] 总列表文件不存在")
        return False

    # 转化成：通用格式
    with open(f"{MainPath}/TrackerList-general.txt", "w", encoding="utf-8") as f:
        f.write("")
    with open(f"{MainPath}/TrackerList-general.txt", "a", encoding="utf-8") as f:
        for tracker in tracker_list:
            f.write(f"{tracker}\n\n")

    # 转化成：Aria2格式
    with open(f"{MainPath}/TrackerList-aria2.txt", "w", encoding="utf-8") as f:
        f.write("")
    with open(f"{MainPath}/TrackerList-aria2.txt", "a", encoding="utf-8") as f:
        for tracker in tracker_list:
            f.write(f"{tracker},")

    print(f"[信息] Tracker格式转化完成")


#【收集Tracker】
def Collect_Tracker():
    print(f"\n[信息] 开始收集Tracker")

    # 更新下载地址
    if Read_Address():
        pass
    else:
        print(f"[错误] 未能获取下载地址列表文件")
        return False
    print(f"[信息] 下载地址更新完毕")

    # 下载整合Tracker列表文件
    for url in address_list:

        # 下载Tracker列表下载文件
        if Download_File(url,f"{MainPath}/download_raw.txt"):
            pass
        else:
            continue

        # 读取Tracker列表下载文件
        try:
            with open(f"{MainPath}/download_raw.txt","r",encoding="utf-8") as f:
                raw_data = f.read()
        except:
            continue

        # 整合Tracker列表文件
        with open(f"{MainPath}/download_tracker.txt","a",encoding="utf-8") as f:
            f.write("\n")
            f.write(raw_data)
            f.write("\n")

    # 转化成列表并去重去空
    with open(f"{MainPath}/download_tracker.txt", "r", encoding="utf-8") as f:
        download_tracker = f.read()
    print(f"[信息] 正在整合列表文件")
    download_tracker_list_raw = download_tracker.split("\n")
    download_tracker_list = List_UNIQUE(download_tracker_list_raw)

    # 读取总列表
    try:
        print(f"[信息] 正在读取总列表")
        with open(f"{MainPath}/TrackerList.txt", "r", encoding="utf-8") as f:
            tracker_list_data = f.read()
        tracker_list = tracker_list_data.split("\n")
        tracker_list = List_UNIQUE(tracker_list)
    except FileNotFoundError:
        tracker_list = []

    # 写入总列表
    print(f"[信息] 正在写入总列表文件")
    tracker_add_number = 0
    for tracker in download_tracker_list:
        with open(f"{MainPath}/TrackerList.txt", "a", encoding="utf-8") as f:
            if tracker in tracker_list:
                pass
            else:
                f.write(f"{tracker}\n")
                tracker_add_number = tracker_add_number + 1

    # 信息统计
    tracker_raw_number = len(download_tracker_list_raw)
    tracker_get_number = len(download_tracker_list)
    tracker_old_number = len(tracker_list)
    tracker_now_number = tracker_old_number + tracker_add_number
    tracker_list_number = len(address_list)

    # 清理文件
    os.remove(f"{MainPath}/download_raw.txt")
    os.remove(f"{MainPath}/download_tracker.txt")
    print(f"[信息] 缓存文件清理完毕")

    print(f"[信息] Tracker收集完毕！\n")

    print(f"[信息] 数据统计 >>> 访问网址:{tracker_list_number} | 本次收集:{tracker_raw_number} | 整合去重:{tracker_get_number} | "
          f"本次新增:{tracker_add_number} | 当前总量:{tracker_now_number}\n")



Collect_Tracker()
Tracker_Converted()



















