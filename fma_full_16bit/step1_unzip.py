import os
import tarfile

PROCESSED_FILE_RECORD = "unziped_record.txt"

def load_processed_files(record_file):
    """
    Load the list of already processed tar files from the record file.
    """
    if os.path.exists(record_file):
        with open(record_file, 'r') as f:
            return set(f.read().splitlines())
    return set()

def save_processed_file(record_file, file_name):
    """
    Save a processed tar file name to the record file.
    """
    with open(record_file, 'a') as f:
        f.write(file_name + '\n')

def extract_tar_files_in_batches(directory, batch_size=5, record_file=PROCESSED_FILE_RECORD):
    """
    Extract .tar files in a directory in batches, with checkpointing to avoid re-extracting already processed files.
    """
    # Load already processed tar files
    processed_files = load_processed_files(record_file)

    tar_files = [f for f in os.listdir(directory) if f.endswith('.tar') and f not in processed_files]
    
    total_files = len(tar_files)
    if total_files == 0:
        print(f"No new tar files to process in {directory}.")
        return

    # Processing files in batches
    for i in range(0, total_files, batch_size):
        batch_files = tar_files[i:i+batch_size]
        print(f"Extracting batch {i//batch_size + 1}: {batch_files}")
        
        for tar_file in batch_files:
            tar_path = os.path.join(directory, tar_file)
            try:
                with tarfile.open(tar_path, 'r') as tar:
                    tar.extractall(path=directory)
                print(f"Extracted {tar_file} successfully.")
                # Record the processed file
                save_processed_file(record_file, tar_file)
            except Exception as e:
                print(f"Error extracting {tar_file}: {e}")

def process_directories(base_directory, batch_size=5):
    """
    Process train, test, and valid directories if they exist and extract their tar files.
    """
    for sub_dir in ['train', 'test', 'valid']:
        full_path = os.path.join(base_directory, sub_dir)
        if os.path.isdir(full_path):
            print(f"Processing directory: {full_path}")
            extract_tar_files_in_batches(full_path, batch_size=batch_size)
        else:
            print(f"Directory {full_path} not found.")

if __name__ == "__main__":
    # Replace this with the path to the base directory
    base_dir = "./"
    
    process_directories(base_dir)

