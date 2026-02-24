#!/usr/bin/env python3
"""
Configuration Test Script - Verifies the RAG system setup

Run this to ensure all dependencies and configuration are correct:
    python3 /home/kali/Desktop/RAG/test_config.py
"""

import sys
import os
from pathlib import Path

# Add parent for imports
sys.path.insert(0, str(Path(__file__).parent))


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def test_directories():
    """Test that all required directories exist"""
    print_section("📁 Directory Structure")

    import config

    dirs_to_check = [
        ("RAG Root", config.RAG_ROOT),
        ("Environment Dir", config.ENV_DIR),
        ("Chunks Dir", config.CHUNKS_DIR),
        ("Default Chunks", config.DEFAULT_CHUNKS_DIR),
    ]

    all_ok = True
    for name, path in dirs_to_check:
        exists = path.exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {name}: {path}")
        if not exists:
            all_ok = False

    return all_ok


def test_env_files():
    """Test that environment files exist"""
    print_section("🔑 Environment Files")

    import config

    env_files = [
        ("Pinecone", config.ENV_DIR / "pinecone.env"),
        ("OpenAI", config.ENV_DIR / "openai.env"),
        ("Telegram", config.ENV_DIR / "telegram.env"),
        ("Gemini (optional)", config.ENV_DIR / "gemini.env"),
    ]

    all_ok = True
    for name, path in env_files:
        exists = path.exists()
        status = "✅" if exists else "⚠️"
        optional = " (optional)" if "optional" in name else ""
        print(f"  {status} {name}{optional}: {path}")

        if exists:
            # Check if file has content
            content = path.read_text().strip()
            if content:
                lines = len(
                    [l for l in content.split("\n") if l and not l.startswith("#")]
                )
                print(f"      └─ {lines} configuration line(s)")
        elif "optional" not in name:
            all_ok = False

    return all_ok


def test_api_keys():
    """Test that API keys can be loaded"""
    print_section("🔐 API Key Access")

    import config

    tests = [
        ("Pinecone", config.get_pinecone_key, False),
        ("OpenAI", config.get_openai_key, False),
        ("Telegram", lambda: config.get_telegram_keys(), True),  # Returns tuple
        (
            "Gemini",
            lambda: open(config.ENV_DIR / "gemini.env").read()
            if (config.ENV_DIR / "gemini.env").exists()
            else None,
            False,
        ),
    ]

    all_ok = True
    for name, getter, is_tuple in tests:
        try:
            result = getter()
            if result:
                if isinstance(result, tuple):
                    status = "✅"
                    detail = f"({len(result)} keys)"
                elif isinstance(result, str):
                    status = "✅"
                    # Show first 10 chars + ...
                    masked = result[:10] + "..." if len(result) > 10 else result
                    detail = f"[{masked}]"
                else:
                    status = "✅"
                    detail = "loaded"
                print(f"  {status} {name}: {detail}")
            else:
                status = "⚠️" if "optional" in name.lower() else "❌"
                print(f"  {status} {name}: Not configured")
                all_ok = False if "optional" not in name.lower() else all_ok
        except Exception as e:
            status = "❌"
            print(f"  {status} {name}: {str(e)[:60]}...")
            all_ok = False

    return all_ok


def test_imports():
    """Test that required Python packages are available"""
    print_section("📦 Python Package Dependencies")

    packages = [
        ("pinecone", "Pinecone Vector DB"),
        ("openai", "OpenAI API"),
        ("telegram", "Telegram Bot API"),
        ("dotenv", "Environment Variable Loader"),
        ("yaml", "YAML Parser"),
        ("langchain_openai", "LangChain OpenAI (optional)"),
        ("langchain_google_genai", "LangChain Google (optional)"),
        ("langchain_pinecone", "LangChain Pinecone (optional)"),
    ]

    all_ok = True
    for package, description in packages:
        try:
            __import__(package)
            status = "✅"
            print(f"  {status} {package:25s} - {description}")
        except ImportError:
            is_optional = "optional" in description.lower()
            status = "⚠️" if is_optional else "❌"
            print(f"  {status} {package:25s} - {description}")
            if not is_optional:
                all_ok = False

    return all_ok


def test_chunk_registry():
    """Test chunk registry"""
    print_section("📚 Chunk Registry")

    import config

    registry_path = config.CHUNK_REGISTRY
    if registry_path.exists():
        import json

        try:
            with open(registry_path) as f:
                registry = json.load(f)
            status = "✅"
            print(f"  {status} Registry found: {len(registry)} chunks registered")
            return True
        except Exception as e:
            print(f"  ❌ Registry error: {e}")
            return False
    else:
        print(f"  ⚠️ Registry not found: {registry_path}")
        print(f"     └─ This is normal for new installations")
        return True


def test_config_module():
    """Test configuration module initialization"""
    print_section("⚙️ Configuration Module")

    try:
        import config

        # Test init_environment
        result = config.init_environment()

        print(f"  ✅ Configuration initialized successfully")
        print(f"\n  Configuration Details:")
        for key, value in result.items():
            print(f"    {key:20s}: {value}")

        return True
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  RAG SYSTEM CONFIGURATION TEST")
    print("=" * 70)

    results = {
        "Directories": test_directories(),
        "Environment Files": test_env_files(),
        "API Keys": test_api_keys(),
        "Python Packages": test_imports(),
        "Chunk Registry": test_chunk_registry(),
        "Configuration Module": test_config_module(),
    }

    # Summary
    print_section("📊 Test Summary")

    all_passed = True
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
        if not result:
            all_passed = False

    print()
    if all_passed:
        print("  ✅ All tests passed! RAG system is ready to use.")
        print("\n  Next steps:")
        print("    1. Create .env files in /home/kali/Desktop/RAG/.env/")
        print("    2. Add your API keys to the configuration files")
        print(
            "    3. Run: python3 /home/kali/Desktop/RAG/src/query_agent.py 'test query'"
        )
    else:
        print("  ⚠️ Some tests failed. Check the output above for details.")
        print("\n  For help, see: /home/kali/Desktop/RAG/CONFIGURATION.md")

    print("\n" + "=" * 70 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
