import os
import json
import pandas as pd
import soundfile as sf
from datasets import Dataset, Features, Value, Audio, Sequence

# 定义函数，获取音频长度
def get_audio_length(audio_file):
    audio_data, sr = sf.read(audio_file)
    return len(audio_data) / sr  # 计算音频时长（秒）

# 定义函数，处理每个文件夹
def process_directory(directory_path, datasetname):
    data = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.flac'):
                audio_path = os.path.join(root, file)
                json_path = audio_path.replace('.flac', '.json')

                # 读取音频数据和采样率
                audio_data, sample_rate = sf.read(audio_path)
                audio_len = len(audio_data) / sample_rate  # 计算音频时长（秒）

                # 读取对应的JSON文件
                if os.path.exists(json_path):
                    with open(json_path, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                else:
                    metadata = {}

                # 生成唯一的index，去掉文件名，仅使用文件夹路径 + 序列号
                audio_id = file.split('.')[0]  # 获取音频编号
                index = os.path.join(root, audio_id)  # 使用音频文件路径 + 编号生成index

                # 创建单个音频文件的记录
                record = {
                    'index': index,  # 唯一标识符
                    'datasetname': datasetname,  # 固定的数据集名称
                    'audio': {
                        'array': audio_data,  # 嵌入实际的音频数据
                        'sampling_rate': sample_rate  # 采样率
                    },
                    'audio_len': audio_len  # 音频长度
                }

                # 从JSON文件获取text（如果有）
                record['text'] = metadata.get('text', [""])[0] if 'text' in metadata else ''

                # raw_text从original_data中获取（如果有）
                raw_text = []
                if 'original_data' in metadata:
                    original_data = metadata['original_data']
                    for key, value in original_data.items():
                        raw_text.append(f"{key.capitalize()}: {value}")
                record['raw_text'] = raw_text

                data.append(record)
    
    return data

# 定义函数，保存为 .parquet 文件，每100条一份
def save_parquet_files(data, output_dir, datasetname, subdir):
    chunk_size = 100
    total_records = len(data)
    
    # 确保输出子目录存在
    output_subdir = os.path.join(output_dir, subdir)
    os.makedirs(output_subdir, exist_ok=True)
    
    for i in range(0, total_records, chunk_size):
        # 生成分段数据
        chunk_data = data[i:i + chunk_size]
        
        # 获取当前分段的起止 index 值用于命名
        first_index = os.path.basename(chunk_data[0]['index'])
        last_index = os.path.basename(chunk_data[-1]['index'])
        
        # 生成文件名，例如：train-0-train-100.parquet
        filename = f"{subdir}-{first_index}-{last_index}.parquet"
        output_path = os.path.join(output_subdir, filename)
        
        # 转换为 DataFrame
        df = pd.DataFrame(chunk_data)
        
        # 定义 Hugging Face datasets 的 features
        features = Features({
            'index': Value('string'),
            'datasetname': Value('string'),
            'audio': Audio(),  # audio字段定义为Hugging Face的audio类型，内嵌音频数据
            'audio_len': Value('float32'),  # 音频长度（秒）
            'text': Value('string'),
            'raw_text': Sequence(Value('string'))  # raw_text定义为sequence类型
        })

        # 转换为 Huggingface Dataset 格式
        dataset = Dataset.from_pandas(df, features=features)

        # 保存为 .parquet 文件
        dataset.to_parquet(output_path)
        print(f"Saved {output_path}")

# 定义主函数
def main(input_dirs, output_dir, datasetname="FSD50K"):
    for input_dir in input_dirs:
        # 获取当前处理的目录名 (train, test, valid)
        subdir = os.path.basename(input_dir.rstrip("/"))
        
        # 处理每个输入目录
        data = process_directory(input_dir, datasetname)
        
        # 保存为分块的 .parquet 文件
        save_parquet_files(data, output_dir, datasetname, subdir)

# 使用方法
if __name__ == "__main__":
    input_dirs = ["./train", "./test", "./valid"]  # 指定你的输入目录
    output_dir = "./data/data"  # 指定输出目录
    main(input_dirs, output_dir)
