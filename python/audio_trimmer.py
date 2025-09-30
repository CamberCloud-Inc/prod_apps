import subprocess
import sys
import os
import argparse

# Install pydub
subprocess.check_call([sys.executable, "-m", "pip", "install", "pydub"])

from pydub import AudioSegment


def parse_timestamp(timestamp):
    """Convert timestamp string (HH:MM:SS or MM:SS or SS) to milliseconds"""
    parts = timestamp.split(':')
    parts = [float(p) for p in parts]

    if len(parts) == 1:  # SS
        return int(parts[0] * 1000)
    elif len(parts) == 2:  # MM:SS
        return int((parts[0] * 60 + parts[1]) * 1000)
    elif len(parts) == 3:  # HH:MM:SS
        return int((parts[0] * 3600 + parts[1] * 60 + parts[2]) * 1000)
    else:
        raise ValueError(f"Invalid timestamp format: {timestamp}")


def main():
    parser = argparse.ArgumentParser(description='Trim audio files by start and end timestamps')
    parser.add_argument('input_file', help='Path to the input audio file')
    parser.add_argument('-s', '--start', default='0',
                        help='Start timestamp (format: HH:MM:SS or MM:SS or SS, default: 0)')
    parser.add_argument('-e', '--end', default=None,
                        help='End timestamp (format: HH:MM:SS or MM:SS or SS, default: end of file)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for trimmed audio (default: ./)')

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
        print(f"Total duration: {len(audio) / 1000:.2f} seconds")
        print(f"Channels: {audio.channels}")
        print(f"Frame rate: {audio.frame_rate} Hz")
    except Exception as e:
        print(f"Error loading audio file: {e}")
        sys.exit(1)

    # Parse timestamps
    try:
        start_ms = parse_timestamp(args.start)
        if args.end:
            end_ms = parse_timestamp(args.end)
        else:
            end_ms = len(audio)

        print(f"\nTrimming audio:")
        print(f"  Start: {start_ms / 1000:.2f} seconds")
        print(f"  End: {end_ms / 1000:.2f} seconds")
        print(f"  Duration: {(end_ms - start_ms) / 1000:.2f} seconds")

        # Validate timestamps
        if start_ms < 0:
            print("Error: Start time cannot be negative")
            sys.exit(1)
        if end_ms > len(audio):
            print(f"Warning: End time exceeds audio duration, using end of file")
            end_ms = len(audio)
        if start_ms >= end_ms:
            print("Error: Start time must be before end time")
            sys.exit(1)
    except ValueError as e:
        print(f"Error parsing timestamps: {e}")
        sys.exit(1)

    # Trim the audio
    try:
        trimmed_audio = audio[start_ms:end_ms]
        print(f"\nTrimmed audio duration: {len(trimmed_audio) / 1000:.2f} seconds")
    except Exception as e:
        print(f"Error trimming audio: {e}")
        sys.exit(1)

    # Generate output filename
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_filename = f"{base_name}_trimmed.{input_format}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Export the trimmed audio
    try:
        print(f"\nExporting trimmed audio...")
        export_kwargs = {}
        if input_format == 'mp3':
            export_kwargs['bitrate'] = '192k'

        trimmed_audio.export(output_path, format=input_format, **export_kwargs)
        print(f"Successfully trimmed audio")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error exporting audio: {e}")
        sys.exit(1)

    print("\nAudio trimming completed!")


if __name__ == "__main__":
    main()