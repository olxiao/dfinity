import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

def decrypt_aes_ecb(encrypted_data, key):
    """Decrypt AES ECB mode"""
    try:
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(encrypted_data)
        return unpad(decrypted, AES.block_size).decode('utf-8')
    except Exception as e:
        return f"AES ECB decryption failed: {str(e)}"

def decrypt_aes_cbc(encrypted_data, key, iv):
    """Decrypt AES CBC mode"""
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted_data)
        return unpad(decrypted, AES.block_size).decode('utf-8')
    except Exception as e:
        return f"AES CBC decryption failed: {str(e)}"

def try_base64_decode(data):
    """Try to decode Base64 data"""
    try:
        return base64.b64decode(data)
    except Exception as e:
        return None

def decrypt_response(response_json, aes_key=None, aes_iv=None):
    """
    Decrypt response data from {"code":0,"msg":"success","data":"encrypted_string"}
    
    Args:
        response_json (str): JSON string response
        aes_key (bytes): AES key for decryption
        aes_iv (bytes): AES IV for CBC mode
    
    Returns:
        dict: Decrypted response
    """
    # Parse JSON response
    response = json.loads(response_json)
    
    if response.get("code") != 0:
        return response
    
    encrypted_data = response.get("data", "")
    
    # Try Base64 decoding first
    decoded_data = try_base64_decode(encrypted_data)
    if not decoded_data:
        # If not Base64, treat as raw data
        decoded_data = encrypted_data.encode('utf-8')
    
    results = {}
    
    # Try AES ECB if key provided
    if aes_key:
        results["AES_ECB"] = decrypt_aes_ecb(decoded_data, aes_key)
        
        # Try AES CBC if IV also provided
        if aes_iv:
            results["AES_CBC"] = decrypt_aes_cbc(decoded_data, aes_key, aes_iv)
    
    # Add original data for reference
    results["original"] = encrypted_data
    
    # Update response with decryption attempts
    response["decrypted_attempts"] = results
    return response

# Example usage
if __name__ == "__main__":
    # Example encrypted response
    sample_response = '{"code":0,"msg":"success","data":"encrypted_string_here"}'
    
    # AES key and IV (you need to find these)
    # Key should be 16, 24, or 32 bytes for AES-128, AES-192, or AES-256
    aes_key = b"your-16-byte-key"  # Replace with actual key
    aes_iv = b"your-16-byte-iv"    # Replace with actual IV if needed
    
    # Decrypt response
    result = decrypt_response(sample_response, aes_key, aes_iv)
    print(json.dumps(result, indent=2))