import subprocess
import sys
import os
import argparse

# Install pydub
subprocess.check_call([sys.executable, "-m", "pip", "install", "pydub"])

from pydub import AudioSegment
from pydub.effects import normalize


def main():
    parser = argparse.ArgumentParser(description='Normalize audio volume levels to a consistent loudness')
    parser.add_argument('input_file', help='Path to the input audio file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for normalized audio (default: ./)')
    parser.add_argument('-t', '--target-dbfs', type=float, default=-20.0,
                        help='Target dBFS level (default: -20.0, range: -50.0 to 0.0)')

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

    # Validate target dBFS
    if args.target_dbfs < -50.0 or args.target_dbfs > 0.0:
        print(f"Error: Target dBFS must be between -50.0 and 0.0 (got {args.target_dbfs})")
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
        print(f"Current dBFS: {audio.dBFS:.2f}")
    except Exception as e:
        print(f"Error loading audio file: {e}")
        sys.exit(1)

    # Normalize the audio
    try:
        print(f"\nNormalizing audio...")
        print(f"  Original peak dBFS: {audio.max_dBFS:.2f}")
        print(f"  Original RMS dBFS: {audio.dBFS:.2f}")

        # First, normalize to bring audio to consistent level
        normalized_audio = normalize(audio)

        # Then adjust to target dBFS
        change_in_dBFS = args.target_dbfs - normalized_audio.dBFS
        print(f"  Adjustment needed: {change_in_dBFS:.2f} dB")

        final_audio = normalized_audio.apply_gain(change_in_dBFS)

        print(f"  Final RMS dBFS: {final_audio.dBFS:.2f}")
        print(f"  Final peak dBFS: {final_audio.max_dBFS:.2f}")

        if final_audio.max_dBFS > -0.1:
            print(f"  Warning: Audio may be clipping (peak dBFS is {final_audio.max_dBFS:.2f})")
    except Exception as e:
        print(f"Error normalizing audio: {e}")
        sys.exit(1)

    # Generate output filename
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_filename = f"{base_name}_normalized.{input_format}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Export the normalized audio
    try:
        print(f"\nExporting normalized audio...")
        export_kwargs = {}
        if input_format == 'mp3':
            export_kwargs['bitrate'] = '192k'
        elif input_format == 'ogg':
            export_kwargs['codec'] = 'libvorbis'

        final_audio.export(output_path, format=input_format, **export_kwargs)
        print(f"Successfully normalized audio")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error exporting audio: {e}")
        sys.exit(1)

    print("\nAudio normalization completed!")


if __name__ == "__main__":
    main()