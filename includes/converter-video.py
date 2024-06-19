import os
import sys
import ffmpeg

# Lista dei formati supportati
supported_formats = {
    "video": ["mp4", "avi", "mkv"]
}

def get_options(question_mapping):
    options = {}
    for option_name, question in question_mapping.items():
        options[option_name] = input(f"{question}: ")
    return options

def convert_video(input_path, output_format, options=None):
    try:
        output_path = ".".join(input_path.split(".")[:-1]) + f".{output_format}"
        ffmpeg.input(input_path).output(output_path, **(options or {})).run(overwrite_output=True)
    except ffmpeg.Error as e:
        print(f"Errore durante la conversione video: {str(e)}")
        sys.exit(1)

def main():
    if len(sys.argv) < 3:
        print("Usage: py video_converter.py <input_path> <output_format> [use_options]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_format = sys.argv[2]
    use_options = len(sys.argv) >= 4 and sys.argv[3].lower() == 'true'

    format_options = {
        'mp4': {
            'video_bitrate': "Imposta un bitrate video (esempio: 1000k)",
            'vf': "Imposta i filtri video (esempio: 'scale=640:480')"
            # altri parametri per video
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
    
    convert_video(input_path, output_format, options)

if __name__ == "__main__":
    main()
