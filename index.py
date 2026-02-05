import os
import sys
import subprocess

# get current abs path folder
current_path = os.path.dirname(os.path.abspath(__file__))
python_path = current_path + r"\Python311\python.exe" if os.path.exists(current_path + r"\Python311\python.exe") else "python"

# Supported formats
supported_formats = {
    "audio": ["mp3", "wav", "aiff", "ogg"],
    "video": ["mp4", "avi", "mkv"],
    "image": ["jpg", "png", "gif"],
    "document": ["pdf", "txt"]
}

# Mapping from format to subscript
subscripts = {
    "audio": "includes/converter-audio.py",
    "video": "includes/converter-video.py",
    "image": "includes/converter-image.py"
}

def get_file_type(extension):
    for type, formats in supported_formats.items():
        if extension in formats:
            return type
    return None

def main():
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1].lower() == 'install'):
        subprocess.run([python_path, os.path.join(current_path, 'includes/install.py')])
        return

    if len(sys.argv) < 3:
        print("Usage: python index.py <input_path> <output_format> [use_options]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_format = sys.argv[2]
    use_options = len(sys.argv) >= 4 and sys.argv[3].lower() == 'true'

    _, input_extension = os.path.splitext(input_path)
    input_extension = input_extension.lstrip(".").lower()
    file_type = get_file_type(input_extension)

    if not file_type:
        print(f"Unsupported input format: {input_extension}")
        sys.exit(1)

    subscript = subscripts.get(file_type)

    if not subscript:
        print(f"No subscript available for file type: {file_type}")
        sys.exit(1)

    subscript_path = os.path.join(current_path, subscript)
    command = [python_path, subscript_path, input_path, output_format]

    if use_options:
        command.append("true")

    subprocess.run(command)

if __name__ == "__main__":
    main()
