#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精灵数据网站API响应数据解密脚本 - 终极版
重点分析AES解密结果
"""

import base64
import json
import gzip
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii

def decode_base64(data):
    """Base64解码"""
    try:
        return base64.b64decode(data)
    except Exception as e:
        print(f"Base64解码失败: {e}")
        return None

def analyze_hex_data(data, label=""):
    """详细分析十六进制数据"""
    print(f"\n{label} 数据分析:")
    print(f"数据长度: {len(data)}")
    print(f"前64字节十六进制: {binascii.hexlify(data[:64]).decode()}")
    if len(data) > 128:
        print(f"中间64字节: ...{binascii.hexlify(data[64:128]).decode()}...")
    print(f"后64字节十六进制: {binascii.hexlify(data[-64:]).decode()}")

    # 检查特殊模式
    if data.startswith(b'\x00' * min(10, len(data))):
        print("  ⚠️ 检测到全零前缀")
    if data.endswith(b'\x00' * min(10, len(data))):
        print("  ⚠️ 检测到以零结尾")

    # 尝试识别JSON结构
    stripped = data.lstrip()
    if stripped.startswith((b'{', b'[')):
        print("  ✅ 可能是JSON格式数据")
        try:
            # 尝试不同的编码
            for encoding in ['utf-8', 'gbk', 'gb2312', 'latin-1']:
                try:
                    text = data.decode(encoding)
                    if '{' in text and '}' in text:
                        print(f"  ✅ {encoding}解码成功，包含JSON特征")
                        return True
                except:
                    continue
        except:
            pass
    else:
        print("  ❌ 不是明显的JSON格式")

    return False

def try_aes_decryption(encrypted_string, key, iv, method_name=""):
    """
    专门测试AES解密
    """
    print(f"\n=== {method_name} ===")

    # Base64解码
    data = decode_base64(encrypted_string)
    if not data:
        return None

    print(f"原始数据长度: {len(data)}")

    # AES解密
    try:
        # 确保key和iv是bytes类型并截取正确长度
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(iv, str):
            iv = iv.encode('utf-8')

        key = key[:32]  # AES-256需要32字节密钥
        iv = iv[:16]    # IV需要16字节

        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()

        # 解密数据
        decrypted_padded = decryptor.update(data) + decryptor.finalize()

        # 移除PKCS7填充
        padding_length = decrypted_padded[-1]
        if padding_length <= 16:  # 合理的填充长度
            decrypted_data = decrypted_padded[:-padding_length]
            print(f"AES解密成功! 解密后数据长度: {len(decrypted_data)}")

            # 详细分析解密结果
            analyze_hex_data(decrypted_data, "AES解密结果")

            # 尝试各种编码解码
            encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
            for encoding in encodings:
                try:
                    text = decrypted_data.decode(encoding)
                    print(f"  ✅ {encoding}解码成功，前200字符: {text[:200]}")
                    if '{' in text and '}' in text:
                        print("  🎉 发现JSON格式!")
                        try:
                            json_data = json.loads(text)
                            print(f"  🎉 JSON解析成功! 内容: {json.dumps(json_data, indent=2, ensure_ascii=False)[:500]}...")
                            return json_data
                        except:
                            print("  ⚠️ JSON解析失败，但包含花括号")
                    return text
                except UnicodeDecodeError as e:
                    continue
                except Exception as e:
                    print(f"  ❌ {encoding}解码异常: {e}")
                    continue

            return decrypted_data

        else:
            print(f"  ❌ 无效的填充长度: {padding_length}")
            return None

    except Exception as e:
        print(f"AES解密失败: {e}")
        return None

if __name__ == "__main__":
    # 示例数据
    encrypted_string = "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... <truncated>"

    # 重点测试几个可能成功的AES组合
    test_cases = [
        {
            "name": "最可能的组合1",
            "key": b"1234567890123456",      # 16字节密钥 (AES-128)
            "iv": b"1234567890123456",     # 16字节IV
        },
        {
            "name": "最可能的组合2",
            "key": b"abcdefghijklmnop",      # 16字节密钥
            "iv": b"abcdefghijklmnop",     # 16字节IV
        },
        {
            "name": "网站域名相关",
            "key": b"jinglingshuju.com123", # 24字节，截取为16字节
            "iv": b"jinglingshuju.com",    # 16字节
        },
        {
            "name": "用户信息相关",
            "key": b"userinfo12345678",       # 16字节
            "iv": b"userinfo12345678",      # 16字节
        }
    ]

    results = []

    for i, case in enumerate(test_cases):
        result = try_aes_decryption(
            encrypted_string,
            case["key"],
            case["iv"],
            f"测试{i+1}: {case['name']}"
        )
        results.append({
            "method": case["name"],
            "result": result,
            "success": result is not None
        })

    # 保存结果
    with open('final_decryption_results.json', 'w', encoding='utf-8') as f:
        json.dump({
            "encrypted_string_length": len(encrypted_string),
            "test_cases": results,
            "summary": {
                "total_tests": len(results),
                "successful": sum(1 for r in results if r["success"]),
                "failed": sum(1 for r in results if not r["success"])
            }
        }, f, ensure_ascii=False, indent=2)

    print("\n" + "="*60)
    print("最终测试结果:")
    print("="*60)
    for result in results:
        status = "✅ 成功" if result["success"] else "❌ 失败"
        print(f"{result['method']:<20} | {status}")

    print(f"\n详细结果已保存到 final_decryption_results.json")