import subprocess
import sys
import os
import argparse

# Install moviepy
subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])

from moviepy.editor import VideoFileClip


def main():
    parser = argparse.ArgumentParser(description='Convert video clips to animated GIFs')
    parser.add_argument('input_file', help='Path to the input video file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for GIF (default: ./)')
    parser.add_argument('-s', '--start', type=float, default=0,
                        help='Start time in seconds (default: 0)')
    parser.add_argument('-e', '--end', type=float, default=None,
                        help='End time in seconds (default: end of video)')
    parser.add_argument('-d', '--duration', type=float, default=None,
                        help='Duration in seconds (alternative to end time)')
    parser.add_argument('-w', '--width', type=int, default=480,
                        help='GIF width in pixels (default: 480)')
    parser.add_argument('-f', '--fps', type=int, default=10,
                        help='Frames per second in GIF (default: 10)')

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
    except Exception as e:
        print(f"Error loading video: {e}")
        sys.exit(1)

    # Determine the clip timing
    start_time = args.start
    if args.duration is not None:
        end_time = start_time + args.duration
    elif args.end is not None:
        end_time = args.end
    else:
        end_time = video.duration

    # Validate timing
    if start_time < 0:
        start_time = 0
    if end_time > video.duration:
        end_time = video.duration
    if start_time >= end_time:
        print(f"Error: Start time ({start_time}s) must be less than end time ({end_time}s)")
        video.close()
        sys.exit(1)

    clip_duration = end_time - start_time
    print(f"\nExtracting clip from {start_time:.2f}s to {end_time:.2f}s (duration: {clip_duration:.2f}s)")

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_filename = f"{base_name}_{start_time:.2f}s-{end_time:.2f}s.gif"
    output_path = os.path.join(args.output_dir, output_filename)

    # Extract and convert clip
    try:
        print(f"Extracting clip...")
        clip = video.subclip(start_time, end_time)

        # Calculate height to maintain aspect ratio
        aspect_ratio = video.size[0] / video.size[1]
        gif_width = args.width
        gif_height = int(gif_width / aspect_ratio)

        print(f"Resizing to {gif_width}x{gif_height} pixels")
        clip_resized = clip.resize(width=gif_width)

        print(f"Converting to GIF at {args.fps} fps...")
        print(f"This may take a while depending on the clip duration...")

        clip_resized.write_gif(output_path, fps=args.fps, program='ffmpeg')

        file_size = os.path.getsize(output_path)
        print(f"\nSuccessfully created GIF: {output_filename}")
        print(f"Output path: {output_path}")
        print(f"GIF properties: {gif_width}x{gif_height}, {args.fps} fps, {clip_duration:.2f}s")
        print(f"File size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")

    except Exception as e:
        print(f"Error creating GIF: {e}")
        video.close()
        sys.exit(1)
    finally:
        clip.close()
        video.close()

    print("\nGIF conversion completed!")


if __name__ == "__main__":
    main()