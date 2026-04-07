#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成示例请求代码 - 用于采集前3页数据
"""

import requests
import json

def get_news_list(page=1, num=20):
    """
    获取资讯列表的示例请求函数
    """
    url = "https://vapi.jinglingshuju.com/Data/getNewsList"

    # 请求参数
    params = {
        'page': page,
        'num': num,
        'uid': 'undefined'
    }

    # 请求头
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'https://www.jinglingshuju.com',
        'Referer': 'https://www.jinglingshuju.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Connection': 'keep-alive',
    }

    try:
        # 发送POST请求
        response = requests.post(url, data=params, headers=headers, timeout=10)

        if response.status_code == 200:
            print(f"✅ 第{page}页请求成功")
            return response.json()
        else:
            print(f"❌ 第{page}页请求失败，状态码: {response.status_code}")
            return None

    except Exception as e:
        print(f"❌ 第{page}页请求异常: {e}")
        return None

def save_data_to_file(data, filename):
    """保存数据到文件"""
    if data and 'data' in data:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ 数据已保存到 {filename}")
        except Exception as e:
            print(f"❌ 保存文件失败: {e}")
    else:
        print("❌ 无效的数据")

def main():
    """主函数 - 采集前3页数据"""
    print("开始采集精灵数据网站资讯...")
    print("=" * 60)

    all_data = []

    for page in range(1, 4):  # 前3页
        print(f"\n正在采集第{page}页...")

        data = get_news_list(page=page, num=20)

        if data:
            # 保存每页数据
            filename = f"news_page_{page}.json"
            save_data_to_file(data, filename)

            # 添加到总数据中
            all_data.append({
                'page': page,
                'data': data
            })

            # 显示基本信息
            if 'data' in data and isinstance(data['data'], str):
                encrypted_length = len(data['data'])
                print(f"  加密数据长度: {encrypted_length} 字符")

    # 保存所有页面的汇总数据
    if all_data:
        summary_filename = "all_pages_summary.json"
        try:
            with open(summary_filename, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 所有页面数据已汇总保存到 {summary_filename}")
        except Exception as e:
            print(f"❌ 保存汇总文件失败: {e}")

    print("\n" + "=" * 60)
    print("采集完成!")
    print("说明:")
    print("1. 数据以加密字符串形式返回，需要进一步解密")
    print("2. 请查看生成的JSON文件了解数据结构")
    print("3. 后续需要实现解密算法才能获得原始数据")

if __name__ == "__main__":
    main()