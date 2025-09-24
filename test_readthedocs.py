#!/usr/bin/env python3
"""
Test to check if asdf is available in Read the Docs builder image.
"""

import os
import subprocess
import sys


def test_asdf_availability():
    """Test if asdf is available in the current environment."""
    
    print("=== ASDF AVAILABILITY TEST ===")
    
    # Test 1: Check if asdf command exists
    print("\n1. Testing asdf command availability:")
    try:
        result = subprocess.run(['asdf', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ asdf is available: {result.stdout.strip()}")
            asdf_available = True
        else:
            print(f"❌ asdf command failed: {result.stderr}")
            asdf_available = False
    except FileNotFoundError:
        print("❌ asdf command not found")
        asdf_available = False
    except subprocess.TimeoutExpired:
        print("❌ asdf command timed out")
        asdf_available = False
    except Exception as e:
        print(f"❌ Error testing asdf: {e}")
        asdf_available = False
    
    # Test 2: Check if asdf is in PATH
    print("\n2. Testing asdf in PATH:")
    try:
        result = subprocess.run(['which', 'asdf'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ asdf found in PATH: {result.stdout.strip()}")
        else:
            print("❌ asdf not found in PATH")
    except Exception as e:
        print(f"❌ Error checking PATH: {e}")
    
    # Test 3: Check if asdf directory exists
    print("\n3. Testing asdf directory:")
    asdf_home = os.environ.get('ASDF_DIR', os.path.expanduser('~/.asdf'))
    if os.path.exists(asdf_home):
        print(f"✅ asdf directory exists: {asdf_home}")
    else:
        print(f"❌ asdf directory not found: {asdf_home}")
    
    # Test 4: Check if asdf is in common locations
    print("\n4. Testing common asdf locations:")
    common_locations = [
        '/opt/asdf',
        '/usr/local/asdf', 
        '/home/readthedocs/.asdf',
        '/root/.asdf',
        '/usr/share/asdf'
    ]
    
    found_locations = []
    for location in common_locations:
        if os.path.exists(location):
            found_locations.append(location)
            print(f"✅ Found asdf at: {location}")
    
    if not found_locations:
        print("❌ No asdf found in common locations")
    
    # Test 5: Check environment variables
    print("\n5. Testing asdf environment variables:")
    asdf_vars = ['ASDF_DIR', 'ASDF_DATA_DIR', 'ASDF_CONFIG_FILE']
    for var in asdf_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: not set")
    
    print("\n=== SUMMARY ===")
    if asdf_available:
        print("✅ asdf appears to be available in this environment")
        print("   The original Read the Docs config might work")
    else:
        print("❌ asdf is NOT available in this environment")
        print("   The original Read the Docs config would fail")
        print("   Our fix using 'pip install uv' is necessary")
    
    print("\n=== READ THE DOCS CONTEXT ===")
    print("Note: This test runs in the current environment.")
    print("Read the Docs uses Ubuntu 24.04 containers which may differ.")
    print("The safest approach is to avoid asdf dependency entirely.")
    
    return asdf_available


def create_readthedocs_test_config():
    """Create a test Read the Docs config to test asdf availability."""
    
    test_config = """version: 2
build:
  os: ubuntu-24.04
  tools:
    python: '3.13'
  commands:
    - echo "Testing asdf availability..."
    - asdf --version || echo "asdf not available"
    - which asdf || echo "asdf not in PATH"
    - ls -la ~/.asdf || echo "asdf directory not found"
    - echo "Test completed"
"""
    
    test_file = ".readthedocs-test.yaml"
    with open(test_file, 'w') as f:
        f.write(test_config)
    
    print(f"\n📝 Created test config: {test_file}")
    print("You can use this to test asdf availability in Read the Docs:")
    print("1. Upload this config to a test repository")
    print("2. Enable Read the Docs for that repository")
    print("3. Check the build logs for asdf availability")
    
    return test_file


if __name__ == "__main__":
    print("Testing asdf availability in current environment...")
    asdf_available = test_asdf_availability()
    
    print("\n" + "="*50)
    create_readthedocs_test_config()
    
    print(f"\n🎯 CONCLUSION: {'asdf is available' if asdf_available else 'asdf is NOT available'}")
    print("Our fix using 'pip install uv' is the safest approach regardless.")