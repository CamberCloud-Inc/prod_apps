import subprocess
import sys
import os
import argparse

# Install moviepy
subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])

from moviepy.editor import VideoFileClip


def main():
    parser = argparse.ArgumentParser(description='Extract audio track from video files')
    parser.add_argument('input_file', help='Path to the input video file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for audio file (default: ./)')
    parser.add_argument('-f', '--format', choices=['mp3', 'wav', 'aac', 'flac'], default='mp3',
                        help='Output audio format (default: mp3)')
    parser.add_argument('-b', '--bitrate', default='192k',
                        help='Audio bitrate for lossy formats (default: 192k)')

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
        print(f"Error: Video file not found at: {input_file}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Open the video
    try:
        print(f"\nLoading video file...")
        video = VideoFileClip(input_file)

        print(f"Successfully loaded video: {input_file}")
        print(f"Video properties: {video.size[0]}x{video.size[1]}, {video.fps:.2f} fps, {video.duration:.2f}s duration")

        # Check if video has audio
        if video.audio is None:
            print(f"Error: Video file does not contain an audio track")
            video.close()
            sys.exit(1)

        print(f"Audio track detected: {video.audio.fps} Hz, {video.audio.nchannels} channel(s)")

    except Exception as e:
        print(f"Error loading video: {e}")
        sys.exit(1)

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_filename = f"{base_name}.{args.format}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Extract audio
    try:
        print(f"\nExtracting audio track to {args.format.upper()} format...")
        print(f"Bitrate: {args.bitrate}")
        print(f"This may take a while depending on the video duration...")

        # Set codec and parameters based on format
        codec_map = {
            'mp3': 'libmp3lame',
            'wav': 'pcm_s16le',
            'aac': 'aac',
            'flac': 'flac'
        }

        codec = codec_map.get(args.format, 'libmp3lame')

        # Write audio file
        if args.format in ['mp3', 'aac']:
            video.audio.write_audiofile(output_path, codec=codec, bitrate=args.bitrate, logger=None)
        else:
            # For lossless formats (wav, flac), bitrate is not used
            video.audio.write_audiofile(output_path, codec=codec, logger=None)

        file_size = os.path.getsize(output_path)
        print(f"\nSuccessfully extracted audio: {output_filename}")
        print(f"Output path: {output_path}")
        print(f"Audio format: {args.format.upper()}")
        print(f"File size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")

    except Exception as e:
        print(f"Error extracting audio: {e}")
        video.close()
        sys.exit(1)
    finally:
        video.close()

    print("\nAudio extraction completed!")


if __name__ == "__main__":
    main()