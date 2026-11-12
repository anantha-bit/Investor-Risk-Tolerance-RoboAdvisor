"""
Data Download and Verification Module
Downloads the Survey of Consumer Finances (SCF) 2009 panel dataset and market data.
"""

import os
import urllib.request
import urllib.parse

BASE_URL = "https://raw.githubusercontent.com/tatsath/fin-ml/master/Chapter%205%20-%20Sup.%20Learning%20-%20Regression%20and%20Time%20Series%20models/Case%20Study%203%20-%20Investor%20Risk%20Tolerance%20and%20Robo-advisors/"
DATA_FILES = [
    "InputData.csv",
    "SP500Data.csv",
    "SCFP2009panel.xlsx"
]

def ensure_data_directory(dest_dir="data"):
    os.makedirs(dest_dir, exist_ok=True)
    return dest_dir

def download_file(file_name, dest_dir="data"):
    ensure_data_directory(dest_dir)
    dest_path = os.path.join(dest_dir, file_name)
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
        print(f"[OK] {file_name} already exists ({os.path.getsize(dest_path):,} bytes)")
        return dest_path
    
    encoded_name = urllib.parse.quote(file_name)
    url = BASE_URL + encoded_name
    print(f"[DOWNLOADING] {file_name} from {url}...")
    urllib.request.urlretrieve(url, dest_path)
    print(f"[SAVED] {dest_path} ({os.path.getsize(dest_path):,} bytes)")
    return dest_path

def download_all(dest_dir="data"):
    paths = {}
    for f in DATA_FILES:
        try:
            paths[f] = download_file(f, dest_dir)
        except Exception as e:
            print(f"[ERROR] Could not download {f}: {e}")
    return paths

if __name__ == "__main__":
    download_all()
