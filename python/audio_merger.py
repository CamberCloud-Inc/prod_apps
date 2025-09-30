import subprocess
import sys
import os
import argparse
import glob

# Install pydub
subprocess.check_call([sys.executable, "-m", "pip", "install", "pydub"])

from pydub import AudioSegment


def main():
    parser = argparse.ArgumentParser(description='Combine multiple audio files into one')
    parser.add_argument('input_pattern', help='Pattern or directory to match audio files (e.g., "*.mp3" or directory path)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for merged audio (default: ./)')
    parser.add_argument('-n', '--output-name', default='merged_audio',
                        help='Output filename without extension (default: merged_audio)')
    parser.add_argument('-f', '--format', default='mp3',
                        help='Output format (default: mp3)')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Contents of current directory:")
    for item in os.listdir("."):
        print(f"  {item}")

    print(f"\nReceived input_pattern argument: {args.input_pattern}")

    # Expand user path if provided
    input_pattern = os.path.expanduser(args.input_pattern)

    # Find matching audio files
    audio_files = []

    # Check if input_pattern is a directory
    if os.path.isdir(input_pattern):
        print(f"Input is a directory: {input_pattern}")
        # Find all audio files in the directory
        for ext in ['*.mp3', '*.wav', '*.flac', '*.ogg', '*.m4a', '*.aac']:
            pattern = os.path.join(input_pattern, ext)
            audio_files.extend(glob.glob(pattern))
            # Also check uppercase extensions
            pattern_upper = os.path.join(input_pattern, ext.upper())
            audio_files.extend(glob.glob(pattern_upper))
    else:
        # Use glob to find files matching the pattern
        audio_files = glob.glob(input_pattern)

    # Remove duplicates and sort
    audio_files = sorted(list(set(audio_files)))

    if not audio_files:
        print(f"Error: No audio files found matching pattern: {input_pattern}")
        print("\nTip: Make sure you're using a valid pattern like '*.mp3' or a directory containing audio files")
        sys.exit(1)

    print(f"\nFound {len(audio_files)} audio file(s) to merge:")
    for i, file in enumerate(audio_files, 1):
        file_size = os.path.getsize(file)
        print(f"  {i}. {os.path.basename(file)} ({file_size / (1024*1024):.2f} MB)")

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Load and merge audio files
    print(f"\nMerging audio files...")
    merged_audio = None
    total_duration = 0

    for i, file in enumerate(audio_files, 1):
        try:
            # Detect format from file extension
            file_format = os.path.splitext(file)[1][1:].lower()
            print(f"\nLoading file {i}/{len(audio_files)}: {os.path.basename(file)}")

            audio = AudioSegment.from_file(file, format=file_format)
            duration = len(audio) / 1000
            print(f"  Duration: {duration:.2f} seconds")
            print(f"  Format: {file_format}, Channels: {audio.channels}, Rate: {audio.frame_rate} Hz")

            if merged_audio is None:
                merged_audio = audio
            else:
                merged_audio = merged_audio + audio

            total_duration += duration
        except Exception as e:
            print(f"  Error loading file {file}: {e}")
            print(f"  Skipping this file...")
            continue

    if merged_audio is None:
        print("\nError: No audio files could be loaded successfully")
        sys.exit(1)

    print(f"\nMerge complete!")
    print(f"  Total files merged: {len(audio_files)}")
    print(f"  Total duration: {total_duration:.2f} seconds ({total_duration / 60:.2f} minutes)")
    print(f"  Final channels: {merged_audio.channels}")
    print(f"  Final frame rate: {merged_audio.frame_rate} Hz")

    # Generate output filename
    output_filename = f"{args.output_name}.{args.format}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Export the merged audio
    try:
        print(f"\nExporting merged audio to {args.format.upper()}...")
        export_kwargs = {}
        if args.format == 'mp3':
            export_kwargs['bitrate'] = '192k'
        elif args.format == 'ogg':
            export_kwargs['codec'] = 'libvorbis'
        elif args.format == 'aac':
            export_kwargs['codec'] = 'aac'
            export_kwargs['bitrate'] = '192k'

        merged_audio.export(output_path, format=args.format, **export_kwargs)
        print(f"Successfully merged audio files")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes ({os.path.getsize(output_path) / (1024*1024):.2f} MB)")
    except Exception as e:
        print(f"Error exporting audio: {e}")
        sys.exit(1)

    print("\nAudio merging completed!")


if __name__ == "__main__":
    main()