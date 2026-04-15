#!/usr/bin/env python
"""
Quick verification that all systems are ready before running main.py
"""
import sys
import os

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
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
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT INSTALLED")
            all_ok = False
    
    return all_ok

def check_config():
    """Check configuration"""
    print("\nChecking configuration:")
    try:
        from config import AI_PROVIDER, GROQ_API_KEY, TTS_PROVIDER
        print(f"  ✓ AI Provider: {AI_PROVIDER}")
        print(f"  ✓ TTS Provider: {TTS_PROVIDER}")
        
        if not GROQ_API_KEY or GROQ_API_KEY.startswith("gsk_"):
            print(f"  ✓ Groq API Key configured")
        else:
            print(f"  ✗ Groq API Key may be invalid")
            return False
        return True
    except Exception as e:
        print(f"  ✗ Config error: {e}")
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
            print(f"  ✓ Piper executable found")
        else:
            print(f"  ✗ Piper not found at {piper_exe}")
            return False
        
        # Try to import and test
        from piper import PiperVoice
        print(f"  ✓ PiperVoice module imported")
        return True
    except Exception as e:
        print(f"  ✗ Piper error: {e}")
        return False

def test_voice():
    """Quick voice test"""
    print("\nTesting voice output:")
    try:
        from assistant.text_to_speech import speak
        print("  Testing: 'Система готова к работе'")
        speak("Система готова к работе")
        print("  ✓ Voice test complete")
        return True
    except Exception as e:
        print(f"  ✗ Voice test failed: {e}")
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
            print(f"\n✗ {name} check error: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {name}")
    
    all_ok = all(result for _, result in results)
    
    if all_ok:
        print("\n✓ All systems ready! Run: python main.py")
    else:
        print("\n✗ Some systems not ready. Fix above issues first.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
