import subprocess
import sys
import os
import argparse
import json

# Install opencv-python
subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])

import cv2


def main():
    parser = argparse.ArgumentParser(description='Extract metadata from video files (duration, resolution, codec, etc.)')
    parser.add_argument('input_file', help='Path to the input video file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for metadata JSON file (default: ./)')
    parser.add_argument('-j', '--json', action='store_true',
                        help='Save metadata as JSON file')

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

    # Get file size
    file_size = os.path.getsize(input_file)

    # Open the video
    try:
        cap = cv2.VideoCapture(input_file)
        if not cap.isOpened():
            print(f"Error: Could not open video file: {input_file}")
            sys.exit(1)

        # Extract video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = frame_count / fps if fps > 0 else 0

        # Get codec information (fourcc)
        fourcc_int = int(cap.get(cv2.CAP_PROP_FOURCC))
        codec = "".join([chr((fourcc_int >> 8 * i) & 0xFF) for i in range(4)])

        # Get bitrate estimate (if available)
        bitrate = cap.get(cv2.CAP_PROP_BITRATE)

        # Create metadata dictionary
        metadata = {
            "filename": os.path.basename(input_file),
            "filepath": os.path.abspath(input_file),
            "file_size_bytes": file_size,
            "file_size_mb": round(file_size / (1024 * 1024), 2),
            "duration_seconds": round(duration, 2),
            "duration_formatted": f"{int(duration // 60)}m {int(duration % 60)}s",
            "resolution": f"{width}x{height}",
            "width": width,
            "height": height,
            "aspect_ratio": round(width / height, 2) if height > 0 else 0,
            "fps": round(fps, 2),
            "frame_count": frame_count,
            "codec_fourcc": codec,
            "bitrate": bitrate if bitrate > 0 else "N/A"
        }

        cap.release()

        print("\n" + "="*60)
        print(f"VIDEO METADATA: {metadata['filename']}")
        print("="*60)
        print(f"File Size:       {metadata['file_size_mb']} MB ({metadata['file_size_bytes']:,} bytes)")
        print(f"Duration:        {metadata['duration_formatted']} ({metadata['duration_seconds']}s)")
        print(f"Resolution:      {metadata['resolution']}")
        print(f"Aspect Ratio:    {metadata['aspect_ratio']}:1")
        print(f"Frame Rate:      {metadata['fps']} fps")
        print(f"Total Frames:    {metadata['frame_count']:,}")
        print(f"Codec (FourCC):  {metadata['codec_fourcc']}")
        print(f"Bitrate:         {metadata['bitrate']}")
        print("="*60)

        # Save as JSON if requested
        if args.json:
            os.makedirs(args.output_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_filename = f"{base_name}_metadata.json"
            output_path = os.path.join(args.output_dir, output_filename)

            with open(output_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            print(f"\nMetadata saved to: {output_path}")

    except Exception as e:
        print(f"Error extracting metadata: {e}")
        sys.exit(1)

    print("\nMetadata extraction completed!")


if __name__ == "__main__":
    main()