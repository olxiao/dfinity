# 精灵数据网站API逆向分析项目

## 项目概述

本项目旨在逆向分析精灵数据网站（vapi.jinglingshuju.com）的加密API响应数据，并实现Python脚本解密和采集前3页的资讯数据。

## 技术发现

### API接口分析
- **目标URL**: `https://vapi.jinglingshuju.com/Data/getNewsList`
- **请求方式**: POST
- **请求参数**: `page=1&num=20&uid=undefined`
- **响应格式**: `{"code":0,"msg":"success","data":"加密字符串"}`

### 加密数据分析
通过Base64解码获得原始数据（7359字节），特征如下：

```
十六进制开头: 3aed5cd54ed7537a5046ed06a2c3334cc408dd62...
十六进制结尾: 3aea870decd89e95877bafe5e925ae4e69812373f...
```

**关键观察:**
- 数据长度为奇数（7359字节），不是标准AES CBC模式的16字节整数倍
- 尝试了多种AES密钥组合均未能成功解密
- 可能存在自定义加密算法或非标准实现

### 技术栈确认
- 前端框架: Nuxt.js (__NUXT__对象存在)
- 主要逻辑: webpack打包的JS文件(a5dfecc.js等)
- 网络请求: 跨域请求，需要Referer头

## 已完成工作

### ✅ 数据采集框架
建立了完整的API请求和响应处理框架：

```python
import requests

def get_news_list(page=1, num=20):
    url = "https://vapi.jinglingshuju.com/Data/getNewsList"
    params = {'page': page, 'num': num, 'uid': 'undefined'}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        # ... 其他必要headers
    }
    response = requests.post(url, data=params, headers=headers)
    return response.json()
```

### ✅ 多方法解密尝试
实现了多种解密策略：

1. **基础方法**: Base64 + UTF-8/Latin-1解码
2. **压缩方法**: Base64 + Gzip解压 + 编码转换
3. **AES方法**: AES-128/192/256 CBC模式尝试
4. **自定义密钥**: 基于域名、用户信息等生成密钥

### ✅ 数据特征分析
详细分析了加密数据的结构特征，为后续破解提供方向。

## 当前状态

### 成功部分
- ✅ 完整捕获API接口行为
- ✅ 建立数据采集框架
- ✅ 完成初步加密分析
- ✅ 生成可运行的示例代码

### 待解决问题
- ❌ 加密算法尚未破解
- ❌ 无法获得原始JSON数据

## 文件产出

### 核心脚本
1. `text/decrypt_data.py` - 基础解密尝试
2. `text/decrypt_data2.py` - 改进版多方法尝试
3. `text/decrypt_data3.py` - 终极版专注AES测试
4. `text/analyze_data.py` - 数据特征分析
5. `text/sample_requests.py` - API请求示例

### 分析结果
1. `test_encrypted_data.json` - 加密数据基本信息
2. `decryption_attempts.log` - 详细解密日志
3. `final_decryption_results.json` - 最终测试结果
4. `task_summary.md` - 任务总结
5. `final_report.md` - 本报告

## 后续建议

### 1. 深入分析JS文件
建议优先分析下载的JS文件，寻找：
- 加密函数的实现位置
- 密钥生成或获取机制
- 可能的算法变种或自定义实现

### 2. 动态调试方案
如果静态分析受阻，建议：
- 在Chrome DevTools中设置XHR断点
- 跟踪加密函数的调用栈
- 捕获运行时参数和中间值

### 3. 备选方案
如继续无法破解，可考虑：
- 联系网站获取官方API文档
- 搜索是否有公开的反向工程成果
- 分析是否有其他接口返回未加密数据

## 结论

本次任务成功建立了对精灵数据网站API的完整认知框架，包括接口行为、数据格式和加密特征。虽然暂时未能完全破解加密算法，但为后续工作奠定了坚实基础。建议优先转向JS文件的动态分析和运行时调试。

---

**重要提醒**: 本项目目前处于逆向工程阶段，所有尝试均未成功破解加密算法。请谨慎处理任何可能涉及版权或法律问题的数据收集和分析操作。