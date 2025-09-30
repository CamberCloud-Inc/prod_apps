import subprocess
import sys
import os
import argparse

# Install moviepy
subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])

from moviepy.editor import VideoFileClip


def main():
    parser = argparse.ArgumentParser(description='Change video resolution to standard formats (480p/720p/1080p/4K)')
    parser.add_argument('input_file', help='Path to the input video file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for resized video (default: ./)')
    parser.add_argument('-r', '--resolution', choices=['480p', '720p', '1080p', '4k'], default='720p',
                        help='Target resolution (default: 720p)')

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
    output_filename = f"{base_name}_{args.resolution}.mp4"
    output_path = os.path.join(args.output_dir, output_filename)

    # Map resolution names to dimensions (width, height) - 16:9 aspect ratio
    resolution_map = {
        '480p': (854, 480),
        '720p': (1280, 720),
        '1080p': (1920, 1080),
        '4k': (3840, 2160)
    }

    target_size = resolution_map[args.resolution]

    try:
        print(f"\nLoading video: {input_file}")
        video = VideoFileClip(input_file)

        # Get video properties
        original_size = video.size
        duration = video.duration
        fps = video.fps

        print(f"Original video properties:")
        print(f"  Resolution: {original_size[0]}x{original_size[1]}")
        print(f"  Duration: {duration:.2f} seconds")
        print(f"  FPS: {fps}")

        print(f"\nChanging resolution to {args.resolution} ({target_size[0]}x{target_size[1]})...")

        # Resize video while maintaining aspect ratio
        resized_video = video.resize(newsize=target_size)

        # Write resized video with good quality settings
        resized_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            bitrate='2000k',
            audio_bitrate='192k',
            preset='medium',
            threads=4
        )

        video.close()
        resized_video.close()

        # Get output file size
        output_file_size = os.path.getsize(output_path)

        print(f"\nVideo resolution change completed!")
        print(f"Output saved to: {output_path}")
        print(f"New resolution: {target_size[0]}x{target_size[1]}")
        print(f"Output file size: {output_file_size / (1024*1024):.2f} MB")

    except Exception as e:
        print(f"Error changing video resolution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()