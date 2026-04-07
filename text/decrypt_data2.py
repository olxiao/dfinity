#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
精灵数据网站API响应数据解密脚本 - 改进版
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

def decode_gzip(data):
    """Gzip解压"""
    try:
        return gzip.decompress(data)
    except Exception as e:
        print(f"Gzip解压失败: {e}")
        return None

def decrypt_aes_256_cbc(encrypted_data, key, iv):
    """
    AES-256-CBC解密
    :param encrypted_data: 加密的数据
    :param key: 密钥 (32字节)
    :param iv: 初始化向量 (16字节)
    :return: 解密后的数据
    """
    try:
        # 确保key和iv是bytes类型
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(iv, str):
            iv = iv.encode('utf-8')

        # 截取正确的长度
        key = key[:32]  # AES-256需要32字节密钥
        iv = iv[:16]    # IV需要16字节

        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()

        # 解密数据
        decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

        # 移除PKCS7填充
        padding_length = decrypted_padded[-1]
        decrypted_data = decrypted_padded[:-padding_length]

        return decrypted_data
    except Exception as e:
        print(f"AES解密失败: {e}")
        return None

def analyze_hex_data(data):
    """分析十六进制数据"""
    print(f"数据长度: {len(data)}")
    print(f"前64字节十六进制: {binascii.hexlify(data[:64]).decode()}")
    print(f"后64字节十六进制: {binascii.hexlify(data[-64:]).decode()}")

    # 尝试识别模式
    if data.startswith(b'\x00' * len(data)):
        print("检测到全零数据")
    elif data.endswith(b'\x00' * len(data)):
        print("检测到以零结尾的数据")

    # 检查是否是gzip格式
    if data.startswith(b'\x1f\x8b'):
        print("可能是gzip压缩数据")

    # 检查是否是JSON格式的开头
    if data.lstrip().startswith((b'{', b'[')):
        print("可能是JSON格式数据")

def try_decrypt_data(encrypted_string, key=None, iv=None, method_name=""):
    """
    尝试多种方法解密数据
    """
    print(f"\n=== {method_name} ===")

    # 方法1: 直接Base64解码
    print("\n--- Base64解码 ---")
    data = decode_base64(encrypted_string)
    if data:
        print(f"Base64解码成功，原始数据长度: {len(data)}")
        analyze_hex_data(data)

        # 尝试解析为JSON
        try:
            json_data = json.loads(data.decode('utf-8'))
            print(f"JSON解析成功! 内容: {json.dumps(json_data, indent=2, ensure_ascii=False)}")
            return json_data
        except Exception as e:
            print(f"JSON解析失败: {e}")

        # 尝试UTF-8解码
        try:
            text = data.decode('utf-8')
            print(f"UTF-8解码成功! 前500字符: {text[:500]}")
            return text
        except Exception as e:
            print(f"UTF-8解码失败: {e}")

        # 尝试Latin-1解码
        try:
            text = data.decode('latin-1')
            print(f"Latin-1解码成功! 前500字符: {text[:500]}")
            return text
        except Exception as e:
            print(f"Latin-1解码失败: {e}")

    # 方法2: Gzip解压
    print("\n--- Gzip解压 ---")
    data = decode_base64(encrypted_string)
    if data and data.startswith(b'\x1f\x8b'):
        decompressed = decode_gzip(data)
        if decompressed:
            print(f"Gzip解压成功，解压后数据长度: {len(decompressed)}")
            analyze_hex_data(decompressed)

            # 尝试UTF-8解码
            try:
                text = decompressed.decode('utf-8')
                print(f"解压后UTF-8解码成功! 前500字符: {text[:500]}")
                return text
            except Exception as e:
                print(f"解压后UTF-8解码失败: {e}")

    # 方法3: AES解密
    print("\n--- AES解密 ---")
    if key and iv:
        data = decode_base64(encrypted_string)
        if data:
            decrypted = decrypt_aes_256_cbc(data, key, iv)
            if decrypted:
                print(f"AES解密成功! 解密后数据长度: {len(decrypted)}")
                analyze_hex_data(decrypted)

                # 尝试UTF-8解码
                try:
                    text = decrypted.decode('utf-8')
                    print(f"AES解密后UTF-8解码成功! 前500字符: {text[:500]}")
                    return text
                except Exception as e:
                    print(f"AES解密后UTF-8解码失败: {e}")
            else:
                print("AES解密失败")
    else:
        print("未提供密钥和IV，跳过AES解密")

    return None

if __name__ == "__main__":
    # 示例数据 - 替换为您获取的实际加密数据
    encrypted_string = "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"

    # 保存测试数据供后续分析
    with open('test_encrypted_data.json', 'w', encoding='utf-8') as f:
        json.dump({
            "encrypted_string": encrypted_string,
            "length": len(encrypted_string),
            "characteristics": {
                "starts_with": encrypted_string[:10],
                "ends_with": encrypted_string[-10:],
                "has_special_chars": any(c in encrypted_string for c in ['+', '/', '=']),
                "length_modulo_4": len(encrypted_string) % 4,
            }
        }, f, ensure_ascii=False, indent=2)
    print("测试数据已保存到 test_encrypted_data.json")

    # 尝试不同的解密方法
    results = []

    # 方法1: Base64解码 + UTF-8解码
    result = try_decrypt_data(
        encrypted_string,
        method_name="方法1: Base64解码 + UTF-8解码"
    )
    results.append(("Base64+UTF8", result))

    # 方法2: Base64解码 + Latin-1解码
    result = try_decrypt_data(
        encrypted_string,
        method_name="方法2: Base64解码 + Latin-1解码"
    )
    results.append(("Base64+Latin1", result))

    # 方法3: Base64解码 + Gzip解压 + UTF-8解码
    result = try_decrypt_data(
        encrypted_string,
        method_name="方法3: Base64解码 + Gzip解压 + UTF-8解码"
    )
    results.append(("Base64+Gzip+UTF8", result))

    # 方法4: Base64解码 + AES解密
    test_keys = [
        b"jinglingshuju.com",  # 可能的密钥
        b"1234567890123456",      # 16字节密钥
        b"abcdefghijklmnopqrstuvwxyz123456",  # 32字节密钥
        b"0123456789abcdef0123456789abcdef",  # 32字节密钥
    ]

    test_ivs = [
        b"1234567890123456",      # 16字节IV
        b"abcdefghijklmnop",      # 16字节IV
        b"0123456789abcdef",      # 16字节IV
    ]

    for i, key in enumerate(test_keys):
        for j, iv in enumerate(test_ivs):
            result = try_decrypt_data(
                encrypted_string,
                key=key,
                iv=iv,
                method_name=f"方法4.{i*3+j+1}: AES解密 (key={key}, iv={iv})"
            )
            results.append((f"AES-key{i}-iv{j}", result))

    # 总结结果
    print("\n" + "="*60)
    print("解密方法总结:")
    print("="*60)
    for method, result in results:
        status = "✓ 成功" if result else "✗ 失败"
        print(f"{method:<20} | {status}")

    # 保存所有尝试的结果
    with open('decryption_attempts.log', 'w', encoding='utf-8') as f:
        f.write("解密尝试日志\n")
        f.write("="*60 + "\n")
        for method, result in results:
            f.write(f"{method:<20} | {'成功' if result else '失败'}\n")
            if result:
                f.write("-" * 40 + "\n")
                f.write(str(result)[:1000] + "...\n")
                f.write("\n")

    print(f"\n详细日志已保存到 decryption_attempts.log")