import os
import tarfile

def extract_tar_files(source_dir, dest_dir, num_files='all'):
    """
    解压指定目录下的 .tar 文件到目标目录
    
    参数：
    source_dir (str): 需要解压的目录（如 train, test, valid）
    dest_dir (str): 解压文件的目标目录
    num_files (int or 'all'): 要解压的文件数量，'all' 表示解压所有文件
    """
    # 获取目录下所有 .tar 文件
    tar_files = [f for f in os.listdir(source_dir) if f.endswith('.tar')]
    
    if not tar_files:
        print(f"No .tar files found in {source_dir}")
        return
    
    # 限制解压的文件数量
    if num_files != 'all':
        tar_files = tar_files[:num_files]

    # 遍历并解压指定数量的 .tar 文件
    for i, tar_file in enumerate(tar_files, 1):
        tar_path = os.path.join(source_dir, tar_file)
        print(f"Extracting {tar_file} ({i}/{len(tar_files)})")
        
        with tarfile.open(tar_path, 'r') as tar:
            tar.extractall(path=dest_dir)

        print(f"{tar_file} extracted to {dest_dir}")
        
    print("Extraction complete!")

# 示例用法
source_directory = './datasets--atom-in-the-universe--FSD50K/snapshots/99674ac439dadccd6248475ad68180a82c40a730/valid'
destination_directory = './'
# 解压1个文件
extract_tar_files(source_directory, destination_directory, num_files=1)
# 解压所有文件
# extract_tar_files(source_directory, destination_directory, num_files='all')
