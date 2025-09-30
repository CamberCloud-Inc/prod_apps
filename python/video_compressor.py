import subprocess
import sys
import os
import argparse

# Install moviepy
subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])

from moviepy.editor import VideoFileClip


def main():
    parser = argparse.ArgumentParser(description='Compress video files with quality control')
    parser.add_argument('input_file', help='Path to the input video file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for compressed video (default: ./)')
    parser.add_argument('-q', '--quality', choices=['low', 'medium', 'high'], default='medium',
                        help='Compression quality level (default: medium)')

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

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_filename = f"{base_name}_compressed.mp4"
    output_path = os.path.join(args.output_dir, output_filename)

    # Map quality to bitrate settings
    quality_settings = {
        'low': {'video_bitrate': '500k', 'audio_bitrate': '64k'},
        'medium': {'video_bitrate': '1000k', 'audio_bitrate': '128k'},
        'high': {'video_bitrate': '2000k', 'audio_bitrate': '192k'}
    }

    settings = quality_settings[args.quality]

    try:
        print(f"\nLoading video: {input_file}")
        video = VideoFileClip(input_file)

        # Get video properties
        duration = video.duration
        fps = video.fps
        size = video.size
        original_size = os.path.getsize(input_file)

        print(f"Video properties:")
        print(f"  Duration: {duration:.2f} seconds")
        print(f"  FPS: {fps}")
        print(f"  Resolution: {size[0]}x{size[1]}")
        print(f"  Original size: {original_size / (1024*1024):.2f} MB")

        print(f"\nCompressing video with {args.quality} quality...")
        print(f"  Video bitrate: {settings['video_bitrate']}")
        print(f"  Audio bitrate: {settings['audio_bitrate']}")

        # Write compressed video
        video.write_videofile(
            output_path,
            bitrate=settings['video_bitrate'],
            audio_bitrate=settings['audio_bitrate'],
            codec='libx264',
            audio_codec='aac',
            preset='medium',
            threads=4
        )

        video.close()

        # Get output file size
        compressed_size = os.path.getsize(output_path)
        compression_ratio = (1 - compressed_size / original_size) * 100

        print(f"\nVideo compression completed!")
        print(f"Output saved to: {output_path}")
        print(f"Compressed size: {compressed_size / (1024*1024):.2f} MB")
        print(f"Compression ratio: {compression_ratio:.1f}% reduction")

    except Exception as e:
        print(f"Error compressing video: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()