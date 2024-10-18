import os
import shutil

def move_folders_to_root(source_base_dir, target_root_dir):
    """
    将解压后的 test, train, valid 文件夹及其内容移动到指定根目录下
    
    参数：
    source_base_dir (str): 解压后文件所在的基础目录，例如 FSD50K/mnt/audio_clip/processed_datasets/FSD50K/
    target_root_dir (str): 目标根目录，例如 FSD50K
    """
    # 定义需要移动的文件夹名称
    folders_to_move = ['test', 'train', 'valid']
    
    for folder in folders_to_move:
        source_folder = os.path.join(source_base_dir, folder)
        target_folder = os.path.join(target_root_dir, folder)
        
        if os.path.exists(source_folder):
            print(f"Moving {folder} from {source_folder} to {target_folder}")
            
            # 如果目标文件夹已经存在，删除它
            if os.path.exists(target_folder):
                shutil.rmtree(target_folder)
            
            # 移动整个文件夹
            shutil.move(source_folder, target_folder)
            
            print(f"{folder} moved successfully!")
        else:
            print(f"{folder} folder not found in {source_base_dir}")

# 示例用法
source_base_directory = './mnt/audio_clip/processed_datasets/FSD50K'
target_root_directory = './'

# 调用函数移动文件夹
move_folders_to_root(source_base_directory, target_root_directory)