import os
import sys

# Get current abs path folder
current_path = os.path.dirname(os.path.abspath(__file__))
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
    "document": os.path.join(current_path, "converter-documents.py"),
    "sheet": os.path.join(current_path, "converter-sheets.py")
}

def generate_remove_from_menu_reg():
    template_remove = r'''[-HKEY_CLASSES_ROOT\SystemFileAssociations\.{format}\shell\{type}_convert]
[-HKEY_CLASSES_ROOT\SystemFileAssociations\.{format}\shell\{type}_convert_custom]
    '''
    reg_content = "Windows Registry Editor Version 5.00\n\n"  # Add header only once
    for type, formats in supported_formats.items():
        for format in formats:
            reg_content += template_remove.format(format=format, type=type)
    
    with open("remove_from_menu.reg", 'w') as file:
        file.write(reg_content)

def generate_add_to_menu_reg():
    def generate_template_reg(main_format, type):
        script_path = converters[type]
        template = r'''
            [HKEY_CLASSES_ROOT\SystemFileAssociations\.{main_format}\shell\{type}_convert]
            "MUIVerb"="Convert to"
            "SubCommands"=""

            [HKEY_CLASSES_ROOT\SystemFileAssociations\.{main_format}\shell\{type}_convert_custom]
            "MUIVerb"="Convert to (custom)"
            "SubCommands"=""
        '''.format(
            main_format=main_format, 
            type=type
        )
        
        for convert_format in supported_formats[type]:
            template += r'''
                [HKEY_CLASSES_ROOT\SystemFileAssociations\.{main_format}\shell\{type}_convert\shell\{convert_format}]
                "MUIVerb"="{convert_format}"
                
                [HKEY_CLASSES_ROOT\SystemFileAssociations\.{main_format}\shell\{type}_convert\shell\{convert_format}\command]
                @="\"{python_path}\" \"{script_path}\" \"%1\" {convert_format}"

                [HKEY_CLASSES_ROOT\SystemFileAssociations\.{main_format}\shell\{type}_convert_custom\shell\{convert_format}]
                "MUIVerb"="{convert_format}"
                
                [HKEY_CLASSES_ROOT\SystemFileAssociations\.{main_format}\shell\{type}_convert_custom\shell\{convert_format}\command]
                @="\"{python_path}\" \"{script_path}\" \"%1\" {convert_format} true"
            '''.format(
                main_format=main_format,
                type=type,
                convert_format=convert_format,
                python_path=python_path.replace("\\", "\\\\"),
                script_path=script_path.replace("\\", "\\\\")
            )
        return template

    reg_content = "Windows Registry Editor Version 5.00\n\n"  # Add header only once
    
    for type, formats in supported_formats.items():
        for format in formats:
            reg_content += generate_template_reg(format, type)

    with open("add_to_menu.reg", 'w', encoding='utf-16') as file:
        file.write(reg_content)
    
    return reg_content

def main():
    input("Generate .reg files to add/remove from context menu. Press Enter to continue...")
    generate_add_to_menu_reg()
    generate_remove_from_menu_reg()

    print('Added .reg files in the directory')
    sys.exit(1)

if __name__ == "__main__":
    main()
