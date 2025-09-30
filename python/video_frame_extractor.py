import subprocess
import sys
import os
import argparse

# Install opencv-python
subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])

import cv2


def main():
    parser = argparse.ArgumentParser(description='Extract frames from video at specified intervals or timestamps')
    parser.add_argument('input_file', help='Path to the input video file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for extracted frames (default: ./)')
    parser.add_argument('-i', '--interval', type=float, default=1.0,
                        help='Interval in seconds between frames to extract (default: 1.0)')
    parser.add_argument('-t', '--timestamps',
                        help='Comma-separated list of timestamps (in seconds) to extract specific frames')

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

    # Determine which frames to extract
    frames_to_extract = []

    if args.timestamps:
        # Extract specific timestamps
        try:
            timestamps = [float(t.strip()) for t in args.timestamps.split(',')]
            frames_to_extract = [(ts, int(ts * fps)) for ts in timestamps if 0 <= ts <= duration]
            print(f"\nExtracting frames at specific timestamps: {[ts for ts, _ in frames_to_extract]}")
        except ValueError as e:
            print(f"Error parsing timestamps: {e}")
            cap.release()
            sys.exit(1)
    else:
        # Extract frames at regular intervals
        current_time = 0
        while current_time <= duration:
            frame_num = int(current_time * fps)
            frames_to_extract.append((current_time, frame_num))
            current_time += args.interval
        print(f"\nExtracting frames every {args.interval} seconds")
        print(f"Total frames to extract: {len(frames_to_extract)}")

    # Extract frames
    extracted_count = 0
    try:
        for timestamp, frame_num in frames_to_extract:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = cap.read()

            if ret:
                output_filename = f"{base_name}_frame_{timestamp:.2f}s.jpg"
                output_path = os.path.join(args.output_dir, output_filename)
                cv2.imwrite(output_path, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                extracted_count += 1
                print(f"Extracted frame at {timestamp:.2f}s -> {output_filename}")
            else:
                print(f"Warning: Could not read frame at {timestamp:.2f}s")

    except Exception as e:
        print(f"Error extracting frames: {e}")
    finally:
        cap.release()

    print(f"\nFrame extraction completed!")
    print(f"Successfully extracted {extracted_count} frames to: {args.output_dir}")


if __name__ == "__main__":
    main()