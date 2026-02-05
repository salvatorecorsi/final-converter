import os
import sys
import ffmpeg

# List of supported formats
supported_formats = ["mp3", "wav", "aiff", "ogg"]

def get_options(question_mapping):
	options = {}
	for option_name, question in question_mapping.items():
		options[option_name] = input(f"{question}: ")
	return options

def convert_audio(input_path, output_format, options=None):
	try:
		output_path = os.path.splitext(input_path)[0] + f".{output_format}"
		ffmpeg.input(input_path).output(output_path, **(options or {})).run(overwrite_output=True)
	except ffmpeg.Error as e:
		print(f"Error during audio conversion: {str(e)}")
		sys.exit(1)

def main():
	if len(sys.argv) < 3:
		sys.exit(1)

	input_path = sys.argv[1]
	output_format = sys.argv[2].lower()
	use_options = len(sys.argv) >= 4 and sys.argv[3].lower() == 'true'

	if output_format not in supported_formats:
		print(f"Unsupported output format: {output_format}")
		print(f"Supported formats: {', '.join(supported_formats)}")
		sys.exit(1)

	format_options = {
		'mp3': {
			'audio_bitrate': "Set a bitrate (e.g., 192k)",
		},
		'wav': {
			'ar': "Set a sample rate (e.g., 44100)"
		},
		'aiff': {
			'ar': "Set a sample rate (e.g., 44100)"
		},
		'ogg': {
			'audio_bitrate': "Set a bitrate (e.g., 192k)"
		}
	}

	options = {}
	if use_options:
		question_mapping = format_options.get(output_format, {})

		if question_mapping:
			options = get_options(question_mapping)
	
	convert_audio(input_path, output_format, options)

if __name__ == "__main__":
	main()