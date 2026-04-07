# OpenCode Agent Instructions - 精灵数据网站逆向项目

## Project Overview
This repository contains a reverse engineering effort to decrypt API responses from `vapi.jinglingshuju.com`. The main goal is to decode encrypted JSON data returned by the `Data/getNewsList` endpoint.

## Key Facts Agents Should Know

### Target System
- **API Endpoint**: `https://vapi.jinglingshuju.com/Data/getNewsList`
- **Request Method**: POST with parameters `page`, `num`, `uid=undefined`
- **Response Format**: `{"code":0,"msg":"success","data":"encrypted_string"}`

### Current Status
- ✅ Successfully captured and analyzed encrypted API responses
- ✅ Base64 decoding yields 7359-byte payload
- ❌ Cannot decrypt using standard AES methods (ECB/CBC)
- ❌ Data length (7359 bytes) is not 16-byte aligned, suggesting non-standard encryption

### Encryption Characteristics
- Encrypted string starts with: `Ou1c1U7XU3pQRu0GosMzTMQI3WKi1dcVgTrK+Lb2sh9z...`
- Hex signature: `3aed5cd54ed7537a5046ed06a2c3334cc408dd62...`
- Ends with: `3aea870decd89e95877bafe5e925ae4e69812373f...`

### Available Scripts & Their Purpose

#### Core Analysis Tools
- `decrypt_response.py` - Main decryption framework with AES ECB/CBC support
- `text/decrypt_data.py` - Multi-method decryption attempts (Base64, Gzip, AES)
- `text/decrypt_data2.py` - Improved decryption with multiple key/IV combinations
- `text/decrypt_data3.py` - Focused AES testing
- `text/analyze_data.py` - Characteristic analysis of encrypted payload

#### Data Collection
- `text/sample_requests.py` - Complete API request framework for scraping
- Generates `news_page_X.json` files for each page scraped

#### Documentation
- `text/task_summary.md` - High-level task completion summary
- `text/final_report.md` - Detailed technical analysis report
- `final_decryption_results.json` - Summary of all decryption attempts (all failed)

### Critical Constraints & Findings

#### Why Standard AES Fails
1. **Non-block-aligned data**: 7359 bytes is odd and not divisible by 16
2. **Custom implementation likely**: Website may use proprietary encryption variant
3. **Key source unknown**: No obvious key derivation from cookies/headers

#### JavaScript Analysis Target
- Primary target: `text/a5dfecc.js` (webpack chunk containing encryption logic)
- Look for functions: `k()`, `m()`, `l()`, `e()` (exported via webpack module)
- Search for crypto-related function names in minified code

### Testing & Validation Commands

#### Run Individual Analysis Tools
```bash
python text/analyze_data.py          # Analyze encryption characteristics
python text/decrypt_data.py          # Test basic decryption methods
python text/decrypt_data2.py         # Test multiple key/IV combinations
python text/sample_requests.py       # Generate sample API requests
python decrypt_response.py           # Use main decryption framework
```

#### Check Dependencies
The project requires:
- `pycryptodome` or `cryptography` library for AES operations
- `requests` for HTTP calls
- Standard Python libraries: base64, json, gzip, binascii

### Next Steps Priority Order

1. **Analyze a5dfecc.js** - Look for actual encryption/decryption functions
2. **Dynamic debugging** - Use Chrome DevTools to trace encryption calls
3. **Alternative approaches**:
   - Search for other unencrypted API endpoints
   - Contact website for official API documentation
   - Research if public decryption libraries exist

### Common Agent Mistakes to Avoid

#### Don't Assume
- Standard AES-CBC will work (data isn't block-aligned)
- Keys come from simple sources (domain name, user agent, etc.)
- Base64 + UTF-8 decoding will reveal structure

#### Do Remember
- Always check `test_encrypted_data.json` for current test data
- Review `final_decryption_results.json` before trying new approaches
- The JS file `a5dfecc.js` is the most promising lead for actual implementation

### File Organization Guidance

- **Main scripts**: Root directory (`decrypt_response.py`)
- **Supporting tools**: `text/` subdirectory
- **Documentation**: `text/` subdirectory and root JSON results
- **Generated data**: `news_page_*.json` files created during scraping

### Success Metrics
- Decrypt at least one API response to valid JSON
- Identify the actual encryption algorithm used
- Create working Python script that can decrypt arbitrary responses

### Important Notes for Future Agents

This is an active reverse engineering effort where static analysis has reached its limits. Focus on:
1. Dynamic runtime analysis of the JavaScript
2. Network traffic inspection during actual page loads
3. Looking for alternative unencrypted data sources on the website

Previous agents have exhaustively tested standard cryptographic approaches without success, indicating a custom or non-standard implementation likely exists.