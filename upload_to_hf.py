#!/usr/bin/env python3
"""
Upload data lokal 9Router ke HuggingFace Dataset
Jalankan ini SEBELUM deploy ke Render supaya data Railway terbawa
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# ── Config (sama persis dengan sync.py) ──────────────────────────
HF_TOKEN      = os.environ.get("HF_TOKEN", "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")
HF_USERNAME   = os.environ.get("HF_USERNAME", "otakcoding")
DATASET_NAME  = os.environ.get("HF_DATASET_NAME", "9router-data-backup")

# Path data lokal (folder 9router-data di workspace)
SCRIPT_DIR = Path(__file__).parent
DATA_DIR   = SCRIPT_DIR / "9router-data"

# Folder yang tidak perlu dibackup (runtime besar, tidak perlu)
EXCLUDE_PATTERNS = [
    "runtime/*",
    "runtime/**/*",
    "logs/*",
    "cache/*",
    "*.pid",
    "*.lock",
    "*.tmp",
    ".git/*",
    "node_modules/*",
    "node_modules/**/*",
]
# ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  Upload 9Router Data -> HuggingFace Dataset")
    print("=" * 55)
    print(f"  DATA_DIR  : {DATA_DIR}")
    print(f"  Dataset   : {HF_USERNAME}/{DATASET_NAME}")
    print(f"  Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

    # Cek data lokal ada
    if not DATA_DIR.exists():
        print(f"\n❌ Folder tidak ditemukan: {DATA_DIR}")
        sys.exit(1)

    # Cek file penting
    sqlite_path = DATA_DIR / "db" / "data.sqlite"
    if sqlite_path.exists():
        size_mb = sqlite_path.stat().st_size / 1024 / 1024
        print(f"\n✅ Database ditemukan: data.sqlite ({size_mb:.2f} MB)")
    else:
        print(f"\n⚠️  data.sqlite tidak ditemukan di {sqlite_path}")
        print("   Mungkin 9Router belum pernah dijalankan secara lokal.")

    # Install huggingface_hub kalau belum ada
    try:
        from huggingface_hub import HfApi
    except ImportError:
        print("\n📦 Menginstall huggingface_hub...")
        os.system(f"{sys.executable} -m pip install huggingface_hub -q")
        from huggingface_hub import HfApi

    api = HfApi(token=HF_TOKEN)
    dataset_id = f"{HF_USERNAME}/{DATASET_NAME}"

    # Pastikan repo HF ada
    print(f"\n🔍 Cek dataset {dataset_id}...")
    try:
        api.repo_info(repo_id=dataset_id, repo_type="dataset")
        print(f"✅ Dataset sudah ada")
    except Exception:
        print(f"📁 Dataset belum ada, membuat baru (private)...")
        try:
            api.create_repo(repo_id=dataset_id, repo_type="dataset", private=True, exist_ok=True)
            print(f"✅ Dataset berhasil dibuat")
        except Exception as e:
            print(f"❌ Gagal membuat dataset: {e}")
            sys.exit(1)

    # Upload folder
    print(f"\n⬆️  Mengupload {DATA_DIR} ke HuggingFace...")
    print("   (Folder 'runtime' & 'node_modules' di-skip karena besar)\n")

    try:
        api.upload_folder(
            repo_id=dataset_id,
            repo_type="dataset",
            folder_path=str(DATA_DIR),
            commit_message=f"Manual backup dari lokal - {datetime.now().isoformat()}",
            ignore_patterns=EXCLUDE_PATTERNS,
        )
        print("\n✅ SUKSES! Data berhasil diupload ke HuggingFace.")
        print(f"\n🔗 Cek di: https://huggingface.co/datasets/{dataset_id}")
        print("\n📋 Langkah selanjutnya:")
        print("   1. Push repo ini ke GitHub")
        print("   2. Connect ke Render → New Web Service")
        print("   3. Saat Render boot, sync.py otomatis download data ini")
        print("   4. Semua provider, API key, combos langsung tersedia!")

    except Exception as e:
        print(f"\n❌ Upload gagal: {e}")
        print("\n💡 Tips:")
        print("   - Pastikan HF_TOKEN valid")
        print("   - Pastikan koneksi internet aktif")
        sys.exit(1)

if __name__ == "__main__":
    main()
