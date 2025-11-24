import os
import urllib.request
import sys

def download_file(url, dest):
    print(f"Downloading {url}...")
    try:
        urllib.request.urlretrieve(url, dest)
        print(f"Saved to {dest}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def main():
    # Using tessdata_fast for speed and smaller size
    base_url = "https://github.com/tesseract-ocr/tessdata_fast/raw/main/"
    
    langs = ["por.traineddata", "eng.traineddata", "spa.traineddata"]
    
    # Target directory: app/assets/tessdata
    target_dir = os.path.join(os.getcwd(), "app", "assets", "tessdata")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    print(f"Downloading language files to: {target_dir}")
    
    for lang in langs:
        url = base_url + lang
        dest = os.path.join(target_dir, lang)
        if not os.path.exists(dest):
            download_file(url, dest)
        else:
            print(f"{lang} already exists.")
            
    print("Download complete.")

if __name__ == "__main__":
    main()
