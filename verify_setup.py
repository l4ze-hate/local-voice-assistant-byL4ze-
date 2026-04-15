#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick verification that all systems are ready before running main.py
"""
import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"[OK] Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  WARNING: Python 3.8+ required")
        return False
    return True

def check_imports():
    """Check critical imports"""
    imports = [
        ('groq', 'Groq API'),
        ('piper', 'Piper TTS'),
        ('speech_recognition', 'Speech Recognition'),
        ('sounddevice', 'Sounddevice'),
        ('customtkinter', 'CustomTkinter GUI'),
        ('edge_tts', 'Edge TTS'),
        ('numpy', 'NumPy'),
    ]
    
    print("\nChecking imports:")
    all_ok = True
    for module, name in imports:
        try:
            __import__(module)
            print(f"  [OK] {name}")
        except ImportError:
            print(f"  [ERROR] {name} - NOT INSTALLED")
            all_ok = False
    
    return all_ok

def check_config():
    """Check configuration"""
    print("\nChecking configuration:")
    try:
        from config import AI_PROVIDER, GROQ_API_KEY, TTS_PROVIDER
        print(f"  [OK] AI Provider: {AI_PROVIDER}")
        print(f"  [OK] TTS Provider: {TTS_PROVIDER}")
        
        if not GROQ_API_KEY or GROQ_API_KEY.startswith("gsk_"):
            print(f"  [OK] Groq API Key configured")
        else:
            print(f"  [ERROR] Groq API Key may be invalid")
            return False
        return True
    except Exception as e:
        print(f"  [ERROR] Config error: {e}")
        return False

def check_piper():
    """Check Piper installation"""
    print("\nChecking Piper TTS:")
    try:
        piper_exe = os.path.join(
            os.path.dirname(__file__),
            '.venv', 'Scripts', 'piper.exe'
        )
        if os.path.exists(piper_exe):
            print(f"  [OK] Piper executable found")
        else:
            print(f"  [ERROR] Piper not found at {piper_exe}")
            return False
        
        # Try to import and test
        from piper import PiperVoice
        print(f"  [OK] PiperVoice module imported")
        return True
    except Exception as e:
        print(f"  [ERROR] Piper error: {e}")
        return False

def test_voice():
    """Quick voice test"""
    print("\nTesting voice output:")
    try:
        from assistant.text_to_speech import speak
        print("  Testing: 'Система готова к работе'")
        speak("Система готова к работе")
        print("  [OK] Voice test complete")
        return True
    except Exception as e:
        print(f"  [ERROR] Voice test failed: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("SYSTEM VERIFICATION")
    print("=" * 60)
    
    checks = [
        ("Python version", check_python_version),
        ("Package imports", check_imports),
        ("Configuration", check_config),
        ("Piper TTS", check_piper),
        ("Voice output", test_voice),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n[ERROR] {name} check error: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "[OK]" if result else "[ERROR]"
        print(f"{status} {name}")
    
    all_ok = all(result for _, result in results)
    
    if all_ok:
        print("\n[OK] All systems ready! Run: python main.py")
    else:
        print("\n[ERROR] Some systems not ready. Fix above issues first.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
