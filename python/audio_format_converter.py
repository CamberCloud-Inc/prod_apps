import subprocess
import sys
import os
import argparse

# Install pydub
subprocess.check_call([sys.executable, "-m", "pip", "install", "pydub"])

from pydub import AudioSegment


def main():
    parser = argparse.ArgumentParser(description='Convert audio files between different formats (MP3/WAV/FLAC/OGG/AAC)')
    parser.add_argument('input_file', help='Path to the input audio file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for converted audio (default: ./)')
    parser.add_argument('-f', '--format', choices=['mp3', 'wav', 'flac', 'ogg', 'aac'], default='mp3',
                        help='Output format (default: mp3)')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Contents of current directory:")
    for item in os.listdir("."):
        print(f"  {item}")

    print(f"\nReceived input_file argument: {args.input_file}")

    # Expand user path if provided
    input_file = os.path.expanduser(args.input_file)
    print(f"Expanded input_file: {input_file}")
    print(f"Absolute input_file: {os.path.abspath(input_file)}")

    if not os.path.exists(input_file):
        print(f"Error: Audio file not found at: {input_file}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Detect input format from file extension
    input_format = os.path.splitext(input_file)[1][1:].lower()
    print(f"Detected input format: {input_format}")

    # Load the audio file
    try:
        audio = AudioSegment.from_file(input_file, format=input_format)
        print(f"Successfully loaded audio: {input_file}")
        print(f"Duration: {len(audio) / 1000:.2f} seconds")
        print(f"Channels: {audio.channels}")
        print(f"Frame rate: {audio.frame_rate} Hz")
        print(f"Sample width: {audio.sample_width} bytes")
    except Exception as e:
        print(f"Error loading audio file: {e}")
        sys.exit(1)

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_filename = f"{base_name}.{args.format}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Export with format-specific settings
    try:
        print(f"\nConverting to {args.format.upper()}...")

        export_kwargs = {}
        if args.format == 'mp3':
            export_kwargs['bitrate'] = '192k'
        elif args.format == 'ogg':
            export_kwargs['codec'] = 'libvorbis'
        elif args.format == 'aac':
            export_kwargs['codec'] = 'aac'
            export_kwargs['bitrate'] = '192k'

        audio.export(output_path, format=args.format, **export_kwargs)
        print(f"Successfully converted audio to {args.format.upper()}")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error exporting audio: {e}")
        sys.exit(1)

    print("\nAudio format conversion completed!")


if __name__ == "__main__":
    main()