import os
import sys
import ffmpeg
from PIL import Image

# get current abs path folder
current_path = os.path.dirname(os.path.abspath(__file__))

# Lista dei formati supportati
supported_formats = {
    "image": ["jpg", "png", "gif", "txt"]
}

def get_options(question_mapping):
    options = {}
    for option_name, question in question_mapping.items():
        options[option_name] = input(f"{question}: ")
    return options

def convert_image(input_path, output_format, options=None):
    try:
        output_path = ".".join(input_path.split(".")[:-1]) + f".{output_format}"
        ffmpeg.input(input_path).output(output_path, **(options or {})).run(overwrite_output=True)
    except ffmpeg.Error as e:
        print(f"Errore durante la conversione immagine: {str(e)}")
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print("Usage: py image_converter.py <input_path> <output_format> [use_options]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_format = sys.argv[2]
    use_options = len(sys.argv) >= 4 and sys.argv[3].lower() == 'true'

    format_options = {
        'jpg': {
            'qscale:v': "Imposta la qualità dell'immagine (scala da 2 a 31, meno è meglio, esempio: 2)"
            # altri parametri per immagini
        }
        # ... altri formati e relative opzioni ...
    }

    options = {}
    if use_options:
        question_mapping = format_options.get(output_format, {})

        if question_mapping:
            options = get_options(question_mapping)
        else:
            print(f"Nessuna opzione disponibile per il formato {output_format}. Procedo senza opzioni.")
    
    convert_image(input_path, output_format, options)

if __name__ == "__main__":
    main()
