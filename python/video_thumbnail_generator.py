import subprocess
import sys
import os
import argparse

# Install opencv-python
subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])

import cv2


def main():
    parser = argparse.ArgumentParser(description='Generate thumbnail images from video at specified timestamps')
    parser.add_argument('input_file', help='Path to the input video file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for thumbnails (default: ./)')
    parser.add_argument('-t', '--timestamps', default='0',
                        help='Comma-separated list of timestamps (in seconds) for thumbnails (default: 0)')
    parser.add_argument('-w', '--width', type=int, default=320,
                        help='Thumbnail width in pixels (default: 320)')
    parser.add_argument('-q', '--quality', type=int, default=90,
                        help='JPEG quality (1-100, default: 90)')

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
        cap = cv2.VideoCapture(input_file)
        if not cap.isOpened():
            print(f"Error: Could not open video file: {input_file}")
            sys.exit(1)

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(f"Successfully opened video: {input_file}")
        print(f"Video properties: {width}x{height}, {fps:.2f} fps, {frame_count} frames, {duration:.2f}s duration")
    except Exception as e:
        print(f"Error opening video: {e}")
        sys.exit(1)

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # Parse timestamps
    try:
        timestamps = [float(t.strip()) for t in args.timestamps.split(',')]
        # Filter timestamps within video duration
        valid_timestamps = [ts for ts in timestamps if 0 <= ts <= duration]

        if len(valid_timestamps) < len(timestamps):
            print(f"Warning: Some timestamps are outside video duration ({duration:.2f}s) and were skipped")

        print(f"\nGenerating thumbnails at timestamps: {valid_timestamps}")
        print(f"Thumbnail width: {args.width}px (height will be proportional)")
    except ValueError as e:
        print(f"Error parsing timestamps: {e}")
        cap.release()
        sys.exit(1)

    # Calculate thumbnail height to maintain aspect ratio
    aspect_ratio = width / height
    thumbnail_width = args.width
    thumbnail_height = int(thumbnail_width / aspect_ratio)

    # Generate thumbnails
    generated_count = 0
    try:
        for timestamp in valid_timestamps:
            frame_num = int(timestamp * fps)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()

            if ret:
                # Resize frame to thumbnail size
                thumbnail = cv2.resize(frame, (thumbnail_width, thumbnail_height), interpolation=cv2.INTER_AREA)

                output_filename = f"{base_name}_thumbnail_{timestamp:.2f}s.jpg"
                output_path = os.path.join(args.output_dir, output_filename)

                cv2.imwrite(output_path, thumbnail, [cv2.IMWRITE_JPEG_QUALITY, args.quality])
                generated_count += 1

                file_size = os.path.getsize(output_path)
                print(f"Generated thumbnail at {timestamp:.2f}s -> {output_filename} ({thumbnail_width}x{thumbnail_height}, {file_size} bytes)")
            else:
                print(f"Warning: Could not read frame at {timestamp:.2f}s")

    except Exception as e:
        print(f"Error generating thumbnails: {e}")
    finally:
        cap.release()

    print(f"\nThumbnail generation completed!")
    print(f"Successfully generated {generated_count} thumbnails to: {args.output_dir}")


if __name__ == "__main__":
    main()