import os
from PIL import Image

def get_image_details(directory='.'):
    # Common image extensions
    valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    
    print(f"{'Filename':<50} | {'Resolution':<15} | {'Size (MB)':<10}")
    print("-" * 80)

    for filename in os.listdir(directory):
        if filename.lower().endswith(valid_extensions):
            file_path = os.path.join(directory, filename)
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    resolution = f"{width}x{height}"
                    
                    # File size in Megabytes
                    file_size = os.path.getsize(file_path) / (1024 * 1024)
                    
                    print(f"{filename:<50} | {resolution:<15} | {file_size:<10.2f}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    get_image_details()
