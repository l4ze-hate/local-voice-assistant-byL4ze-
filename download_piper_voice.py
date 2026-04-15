#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Download Piper Russian Voice Manually
Direct download from HuggingFace
"""
import os
import urllib.request

print("=" * 60)
print("Piper Russian Voice Downloader")
print("=" * 60)

model_dir = ".cache/piper_voices"
os.makedirs(model_dir, exist_ok=True)

# Direct download links (correct - with medium suffix)
files = {
    "ru_RU.onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ru/ru_RU/ruslan/medium/ru_RU-ruslan-medium.onnx",
    "ru_RU.onnx.json": "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ru/ru_RU/ruslan/medium/ru_RU-ruslan-medium.onnx.json"
}

print(f"\nDownloading to: {model_dir}\n")

success = True
for filename, url in files.items():
    filepath = os.path.join(model_dir, filename)
    
    # Skip if already exists
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ {filename} already exists ({size / 1024 / 1024:.1f} MB)")
        continue
    
    print(f"📥 Downloading {filename}...")
    print(f"   URL: {url}")
    
    try:
        urllib.request.urlretrieve(url, filepath)
        size = os.path.getsize(filepath)
        print(f"   ✅ Downloaded: {size / 1024 / 1024:.1f} MB")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        success = False
        try:
            os.remove(filepath)
        except:
            pass

print("\n" + "=" * 60)
if success:
    print("✅ SUCCESS! Voice files downloaded!")
    print("\nNow run: python test_piper_diagnostic.py")
else:
    print("❌ Some files failed to download!")
    print("\nManual download:")
    print("1. Visit: https://huggingface.co/rhasspy/piper-voices/tree/v1.0.0/ru/ru_RU/ruslan")
    print("2. Download ru_RU-ruslan.onnx and ru_RU-ruslan.onnx.json")
    print(f"3. Place in: {model_dir}")
print("=" * 60)
