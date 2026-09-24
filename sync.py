#!/usr/bin/env python3
"""
Auto-sync script for 9Router config to Hugging Face Dataset
Downloads backup on startup, uploads changes every 5 minutes
"""

import os
import sys
import time
import shutil
from datetime import datetime
from huggingface_hub import HfApi, snapshot_download
import hashlib
import json

# Configuration
HF_TOKEN = os.environ.get("HF_TOKEN")
HF_USERNAME = os.environ.get("HF_USERNAME", "otakcoding")
DATASET_NAME = os.environ.get("HF_DATASET_NAME", "9router-data-backup")
DATA_DIR = os.environ.get("DATA_DIR", "/app/data")
SYNC_INTERVAL = 300  # 5 minutes
MAX_RETRIES = 3
RETRY_DELAY = 30  # 30 seconds

# Directories to exclude from backup (runtime node_modules, logs, cache)
EXCLUDE_DIRS = {"runtime", "logs", "cache", ".git", "node_modules"}
# Files that change constantly and shouldn't be backed up
EXCLUDE_FILES = {"*.pid", "*.lock", "*.tmp"}

# Initialize HF API
hf_api = HfApi(token=HF_TOKEN)
dataset_id = f"{HF_USERNAME}/{DATASET_NAME}"

def should_exclude(path):
    """Check if path should be excluded from backup"""
    rel = os.path.relpath(path, DATA_DIR) if os.path.dirname(path) != DATA_DIR else os.path.basename(path)
    parts = rel.split(os.sep)
    for part in parts[:-1]:
        if part in EXCLUDE_DIRS:
            return True
    filename = os.path.basename(path)
    for pattern in EXCLUDE_FILES:
        if pattern.startswith("*") and filename.endswith(pattern[1:]):
            return True
    return False

def get_file_hash(filepath):
    """Get MD5 hash of a file"""
    if not os.path.exists(filepath):
        return None
    if should_exclude(filepath):
        return None
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except (IsADirectoryError, PermissionError, OSError):
        return None
    return hash_md5.hexdigest()

def get_directory_hash(directory):
    """Get combined hash of all files in directory"""
    if not os.path.exists(directory):
        return None
    file_hashes = []
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            filepath = os.path.join(root, file)
            h = get_file_hash(filepath)
            if h:
                file_hashes.append(h)
    return hashlib.md5("".join(file_hashes).encode()).hexdigest() if file_hashes else None

def download_from_hf(local_dir, retries=MAX_RETRIES):
    """Download entire dataset from Hugging Face"""
    for attempt in range(retries):
        try:
            print(f"[{datetime.now()}] Downloading from HF Dataset (attempt {attempt + 1}/{retries})...")
            
            # Create local directory if it doesn't exist
            os.makedirs(local_dir, exist_ok=True)
            
            # Download using snapshot_download (skip runtime/logs dirs)
            snapshot_download(
                repo_id=dataset_id,
                repo_type="dataset",
                local_dir=local_dir,
                ignore_patterns=[f"{d}/*" for d in EXCLUDE_DIRS] + [f"{d}/**/*" for d in EXCLUDE_DIRS]
            )
            
            print(f"[{datetime.now()}] ✅ Successfully downloaded from HF Dataset")
            return True
            
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Download attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"[{datetime.now()}] Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"[{datetime.now()}] ❌ All download attempts failed")
                return False

def upload_to_hf(local_dir, retries=MAX_RETRIES):
    """Upload entire directory to Hugging Face"""
    for attempt in range(retries):
        try:
            print(f"[{datetime.now()}] Uploading to HF Dataset (attempt {attempt + 1}/{retries})...")
            
            # Upload using upload_folder (skip runtime/logs dirs)
            hf_api.upload_folder(
                repo_id=dataset_id,
                repo_type="dataset",
                folder_path=local_dir,
                commit_message=f"Auto-sync backup {datetime.now().isoformat()}",
                ignore_patterns=[f"{d}/*" for d in EXCLUDE_DIRS] + [f"{d}/**/*" for d in EXCLUDE_DIRS]
            )
            
            print(f"[{datetime.now()}] ✅ Successfully uploaded to HF Dataset")
            return True
            
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Upload attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"[{datetime.now()}] Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print(f"[{datetime.now()}] ❌ All upload attempts failed")
                return False

def ensure_dataset_exists():
    """Ensure the dataset repository exists"""
    try:
        hf_api.repo_info(repo_id=dataset_id, repo_type="dataset")
        print(f"[{datetime.now()}] Dataset {dataset_id} already exists")
    except Exception as e:
        print(f"[{datetime.now()}] Dataset {dataset_id} does not exist, creating...")
        try:
            hf_api.create_repo(
                repo_id=dataset_id,
                repo_type="dataset",
                private=True,
                exist_ok=True
            )
            print(f"[{datetime.now()}] ✅ Created dataset {dataset_id}")
        except Exception as create_error:
            print(f"[{datetime.now()}] ❌ Failed to create dataset: {create_error}")

def main():
    # Validate required environment variables
    if not HF_TOKEN:
        print(f"[{datetime.now()}] ⚠️ HF_TOKEN not set, sync service will be disabled")
        print(f"[{datetime.now()}] To enable sync, set HF_TOKEN environment variable")
        return
    
    print(f"[{datetime.now()}] Starting 9Router auto-sync service...")
    print(f"[{datetime.now()}] DATA_DIR: {DATA_DIR}")
    print(f"[{datetime.now()}] Dataset: {dataset_id}")
    print(f"[{datetime.now()}] Sync interval: {SYNC_INTERVAL} seconds")
    
    # Ensure dataset exists
    ensure_dataset_exists()
    
    # Initial download on startup
    print(f"[{datetime.now()}] Performing initial download...")
    if download_from_hf(DATA_DIR):
        print(f"[{datetime.now()}] Initial download completed")
    else:
        print(f"[{datetime.now()}] Initial download failed, starting with empty state")
    
    # Track last hash for change detection
    last_hash = get_directory_hash(DATA_DIR)
    print(f"[{datetime.now()}] Initial directory hash: {last_hash}")
    
    # Main sync loop
    while True:
        try:
            time.sleep(SYNC_INTERVAL)
            
            # Check for changes
            current_hash = get_directory_hash(DATA_DIR)
            if current_hash != last_hash:
                print(f"[{datetime.now()}] Changes detected in DATA_DIR")
                print(f"[{datetime.now()}] Previous hash: {last_hash}")
                print(f"[{datetime.now()}] Current hash: {current_hash}")
                
                # Upload changes
                if upload_to_hf(DATA_DIR):
                    last_hash = current_hash
                    print(f"[{datetime.now()}] ✅ Sync completed successfully")
                else:
                    print(f"[{datetime.now()}] ❌ Sync failed, will retry next cycle")
            else:
                print(f"[{datetime.now()}] No changes detected, skipping sync")
                
        except KeyboardInterrupt:
            print(f"[{datetime.now()}] Shutting down sync service...")
            break
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Error in sync loop: {e}")
            print(f"[{datetime.now()}] Continuing sync loop...")

if __name__ == "__main__":
    main()