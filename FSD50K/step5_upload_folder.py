from huggingface_hub import HfApi, create_repo



api = HfApi()



api.upload_folder(
    folder_path="./data",
    repo_id="CLAPv2/FSD50K",
    repo_type="dataset",
)