# Asset Downloader for Navigator VisionQuest
# Copyright © Toni Mandušić 2025

import requests
import os

def download_file(url, filename):
    """Download file from URL to specified filename"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"✅ Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False

def main():
    print("🚢 Downloading assets for Navigator VisionQuest...")
    
    # Create directory structure
    os.makedirs("assets/banners", exist_ok=True)
    os.makedirs("assets/test_icons", exist_ok=True)
    
    # Banner images
    banners = {
        "main_banner.png": "https://i.postimg.cc/fbcrnNXC/Gemini-Generated-Image-6gukqc6gukqc6guk.png",
        "lantern_banner.png": "https://i.postimg.cc/HLgBVDzm/Gemini-Generated-Image-2uib402uib402uib.png",
        "fm15_banner.png": "https://i.postimg.cc/mDhMr806/Gemini-Generated-Image-7a116v7a116v7a11.png",
        "ecdis_banner.png": "https://i.postimg.cc/hvSkxQ0B/Gemini-Generated-Image-2mye5e2mye5e2mye.png",
        "ishihara_banner.png": "https://i.postimg.cc/vZ6N4vdv/Gemini-Generated-Image-5xg9ca5xg9ca5xg9.png"
    }
    
    # Test icons
    icons = {
        "lantern_icon.png": "https://i.postimg.cc/HLgBVDzm/Gemini-Generated-Image-2uib402uib402uib.png",
        "fm15_icon.png": "https://i.postimg.cc/mDhMr806/Gemini-Generated-Image-7a116v7a116v7a11.png",
        "ecdis_icon.png": "https://i.postimg.cc/hvSkxQ0B/Gemini-Generated-Image-2mye5e2mye5e2mye.png",
        "ishihara_icon.png": "https://i.postimg.cc/vZ6N4vdv/Gemini-Generated-Image-5xg9ca5xg9ca5xg9.png"
    }
    
    # Download banners
    print("\n📋 Downloading banners...")
    for filename, url in banners.items():
        download_file(url, f"assets/banners/{filename}")
    
    # Download icons
    print("\n🎯 Downloading test icons...")
    for filename, url in icons.items():
        download_file(url, f"assets/test_icons/{filename}")
    
    print("\n🎉 All assets downloaded successfully!")
    print("👉 Now run: streamlit run app.py")

if __name__ == "__main__":
    main()