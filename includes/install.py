import os
import sys

# Get current abs path folder
current_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.path.dirname(current_path)
# Get python path from environment variable
python_path = sys.executable
print(f"Python path: {python_path}")

# Supported formats and corresponding converters
supported_formats = {
    "audio": ["mp3", "wav", "aiff", "ogg"],
    "video": ["mp4", "avi", "mkv"],
    "image": ["jpg", "png", "gif", "txt"],
    "document": ["docx", "pdf", "txt"],
    "sheet": ["xlsx", "xls", "csv", "rtf", "txt"]
}

converters = {
    "audio": os.path.join(current_path, "converter-audio.py"),
    "video": os.path.join(current_path, "converter-video.py"),
    "image": os.path.join(current_path, "converter-image.py"),
    "document": os.path.join(current_path, "converter-document.py"),
    "sheet": os.path.join(current_path, "converter-sheet.py")
}

def generate_remove_from_menu_reg():
    reg_content = "Windows Registry Editor Version 5.00\n\n"
    for type, formats in supported_formats.items():
        for format in formats:
            reg_content += (
                r'[-HKEY_CLASSES_ROOT\SystemFileAssociations\.{format}\shell\{type}_convert]'
                '\n'
                r'[-HKEY_CLASSES_ROOT\SystemFileAssociations\.{format}\shell\{type}_convert_custom]'
                '\n\n'
            ).format(format=format, type=type)

    with open(os.path.join(project_path, "remove_from_menu.reg"), 'w', encoding='utf-16') as file:
        file.write(reg_content)

def generate_add_to_menu_reg():
    def generate_template_reg(main_format, type):
        script_path = converters[type]
        escaped_python = python_path.replace("\\", "\\\\")
        escaped_script = script_path.replace("\\", "\\\\")

        template = (
            r'[HKEY_CLASSES_ROOT\SystemFileAssociations\.{main_format}\shell\{type}_convert]' '\n'
            r'"MUIVerb"="Convert to"' '\n'
            r'"SubCommands"=""' '\n\n'
            r'[HKEY_CLASSES_ROOT\SystemFileAssociations\.{main_format}\shell\{type}_convert_custom]' '\n'
            r'"MUIVerb"="Convert to (custom)"' '\n'
            r'"SubCommands"=""' '\n\n'
        ).format(main_format=main_format, type=type)

        for convert_format in supported_formats[type]:
            template += (
                r'[HKEY_CLASSES_ROOT\SystemFileAssociations\.{main_format}\shell\{type}_convert\shell\{convert_format}]' '\n'
                r'"MUIVerb"="{convert_format}"' '\n\n'
                r'[HKEY_CLASSES_ROOT\SystemFileAssociations\.{main_format}\shell\{type}_convert\shell\{convert_format}\command]' '\n'
                r'@="\"{python_path}\" \"{script_path}\" \"%1\" {convert_format}"' '\n\n'
                r'[HKEY_CLASSES_ROOT\SystemFileAssociations\.{main_format}\shell\{type}_convert_custom\shell\{convert_format}]' '\n'
                r'"MUIVerb"="{convert_format}"' '\n\n'
                r'[HKEY_CLASSES_ROOT\SystemFileAssociations\.{main_format}\shell\{type}_convert_custom\shell\{convert_format}\command]' '\n'
                r'@="\"{python_path}\" \"{script_path}\" \"%1\" {convert_format} true"' '\n\n'
            ).format(
                main_format=main_format,
                type=type,
                convert_format=convert_format,
                python_path=escaped_python,
                script_path=escaped_script,
            )
        return template

    reg_content = "Windows Registry Editor Version 5.00\n\n"

    for type, formats in supported_formats.items():
        for format in formats:
            reg_content += generate_template_reg(format, type)

    with open(os.path.join(project_path, "add_to_menu.reg"), 'w', encoding='utf-16') as file:
        file.write(reg_content)

    return reg_content

def main():
    input("Generate .reg files to add/remove from context menu. Press Enter to continue...")
    generate_add_to_menu_reg()
    generate_remove_from_menu_reg()

    print('Added .reg files in the directory')
    sys.exit(0)

if __name__ == "__main__":
    main()
