import os
from huggingface_hub import HfApi
from datetime import datetime

# HF credentials
HF_TOKEN = "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"
HF_USERNAME = "otakcoding"

# Generate timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Repository names
space_name = f"9router-space-{timestamp}"
dataset_name = f"9router-config-{timestamp}"

print(f"Creating repositories with timestamp: {timestamp}")
print(f"Space name: {space_name}")
print(f"Dataset name: {dataset_name}")

# Initialize HF API
api = HfApi(token=HF_TOKEN)

try:
    # Create Space repository (Docker SDK, Private)
    print(f"\nCreating Space repository: {space_name}...")
    space_id = api.create_repo(
        repo_id=f"{HF_USERNAME}/{space_name}",
        repo_type="space",
        space_sdk="docker",
        private=True,
        exist_ok=True
    )
    print(f"✅ Space created: {space_id}")

    # Create Dataset repository (Private)
    print(f"\nCreating Dataset repository: {dataset_name}...")
    dataset_id = api.create_repo(
        repo_id=f"{HF_USERNAME}/{dataset_name}",
        repo_type="dataset",
        private=True,
        exist_ok=True
    )
    print(f"✅ Dataset created: {dataset_id}")

    # Save repository info to file
    with open("hf_repo_info.txt", "w") as f:
        f.write(f"SPACE_REPO={HF_USERNAME}/{space_name}\n")
        f.write(f"DATASET_REPO={HF_USERNAME}/{dataset_name}\n")
        f.write(f"TIMESTAMP={timestamp}\n")
        f.write(f"SPACE_URL=https://huggingface.co/spaces/{HF_USERNAME}/{space_name}\n")
        f.write(f"DATASET_URL=https://huggingface.co/datasets/{HF_USERNAME}/{dataset_name}\n")

    print(f"\n✅ Repository information saved to hf_repo_info.txt")
    print(f"\nSpace URL: https://huggingface.co/spaces/{HF_USERNAME}/{space_name}")
    print(f"Dataset URL: https://huggingface.co/datasets/{HF_USERNAME}/{dataset_name}")

except Exception as e:
    print(f"❌ Error creating repositories: {e}")
    exit(1)