from huggingface_hub import snapshot_download

snapshot_download(repo_id="atom-in-the-universe/FSD50K", repo_type="dataset",cache_dir='./')