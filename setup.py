"""
Setup script to help you get started with the Stock Sentiment Analysis project.
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_env_file():
    """Create .env file from example if it doesn't exist."""
    env_file = Path('.env')
    example_file = Path('.env.example')
    
    if not env_file.exists() and example_file.exists():
        print("📝 Creating .env file from example...")
        with open(example_file, 'r') as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        print("✅ .env file created! Please edit it with your API keys.")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("❌ No .env.example file found")

def check_directories():
    """Check if all required directories exist."""
    required_dirs = [
        'data/raw',
        'data/processed', 
        'data/results',
        'logs',
        'config'
    ]
    
    for dir_path in required_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✅ All required directories created")

def install_dependencies():
    """Check if we can install dependencies."""
    print("\n🔧 To install dependencies, run:")
    print("   pip install -r requirements.txt")
    
    print("\n📦 Key dependencies that will be installed:")
    print("   • praw (Reddit API)")
    print("   • tweepy (Twitter API)")
    print("   • textblob & vaderSentiment (Sentiment Analysis)")
    print("   • pandas & numpy (Data Processing)")
    print("   • sqlalchemy (Database)")

def show_api_setup_instructions():
    """Show instructions for setting up API keys."""
    print("\n🔑 API SETUP INSTRUCTIONS:")
    print("="*50)
    
    print("\n1️⃣  REDDIT API (Free & Easy):")
    print("   • Go to: https://www.reddit.com/prefs/apps")
    print("   • Click 'Create App' or 'Create Another App'")
    print("   • Choose 'script' for personal use")
    print("   • Copy the client ID and secret to your .env file")
    
    print("\n2️⃣  TWITTER API (May require approval):")
    print("   • Go to: https://developer.twitter.com/")
    print("   • Apply for a developer account")
    print("   • Create a new app")
    print("   • Get Bearer Token and API keys")
    print("   • Copy all tokens to your .env file")
    
    print("\n⚠️  Note: Twitter API now requires approval and may have usage limits")

def show_testing_options():
    """Show testing options."""
    print("\n🧪 TESTING OPTIONS:")
    print("="*30)
    print("1. Test with mock data (no API keys needed):")
    print("   python test_with_mock_data.py")
    print()
    print("2. Test with real data (requires API keys):")
    print("   python run_analysis.py")

def main():
    """Main setup function."""
    print("🚀 Stock Sentiment Analysis - Setup Helper")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Create directories
    check_directories()
    
    # Create .env file
    create_env_file()
    
    # Show installation instructions
    install_dependencies()
    
    # Show API setup instructions
    show_api_setup_instructions()
    
    # Show testing options
    show_testing_options()
    
    print("\n✅ Setup complete!")
    print("\n📋 NEXT STEPS:")
    print("1. Run: pip install -r requirements.txt")
    print("2. Edit .env file with your API keys")
    print("3. Test with: python test_with_mock_data.py")
    print("4. Run real analysis with: python run_analysis.py")

if __name__ == "__main__":
    main()
