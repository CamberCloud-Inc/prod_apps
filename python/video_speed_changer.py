import subprocess
import sys
import os
import argparse

# Install moviepy
subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])

from moviepy.editor import VideoFileClip


def main():
    parser = argparse.ArgumentParser(description='Speed up or slow down video playback')
    parser.add_argument('input_file', help='Path to the input video file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for speed-modified video (default: ./)')
    parser.add_argument('-s', '--speed', type=float, default=1.0,
                        help='Speed factor (0.5 = half speed, 2.0 = double speed, default: 1.0)')

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

    # Validate speed factor
    if args.speed <= 0:
        print(f"Error: Speed factor must be greater than 0")
        sys.exit(1)

    if args.speed < 0.1 or args.speed > 10.0:
        print(f"Warning: Extreme speed factors may result in poor quality or errors")

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_filename = f"{base_name}_{args.speed}x.mp4"
    output_path = os.path.join(args.output_dir, output_filename)

    try:
        print(f"\nLoading video: {input_file}")
        video = VideoFileClip(input_file)

        # Get video properties
        original_duration = video.duration
        fps = video.fps
        size = video.size

        print(f"Original video properties:")
        print(f"  Resolution: {size[0]}x{size[1]}")
        print(f"  Duration: {original_duration:.2f} seconds")
        print(f"  FPS: {fps}")

        print(f"\nChanging video speed by {args.speed}x...")

        # Change speed using speedx method
        # speedx automatically adjusts both video and audio
        modified_video = video.speedx(factor=args.speed)

        new_duration = modified_video.duration
        print(f"New duration: {new_duration:.2f} seconds")

        # Write modified video
        modified_video.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            bitrate='2000k',
            audio_bitrate='192k',
            preset='medium',
            threads=4
        )

        video.close()
        modified_video.close()

        # Get output file size
        output_file_size = os.path.getsize(output_path)

        print(f"\nVideo speed change completed!")
        print(f"Output saved to: {output_path}")
        print(f"Speed factor: {args.speed}x")
        print(f"Original duration: {original_duration:.2f}s -> New duration: {new_duration:.2f}s")
        print(f"Output file size: {output_file_size / (1024*1024):.2f} MB")

    except Exception as e:
        print(f"Error changing video speed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()