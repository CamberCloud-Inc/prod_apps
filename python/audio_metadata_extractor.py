import subprocess
import sys
import os
import argparse
import json

# Install mutagen
subprocess.check_call([sys.executable, "-m", "pip", "install", "mutagen"])

from mutagen import File as MutagenFile
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3


def main():
    parser = argparse.ArgumentParser(description='Extract metadata (ID3 tags, artist, album info) from audio files')
    parser.add_argument('input_file', help='Path to the input audio file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for metadata JSON file (default: ./)')

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

    # Load the audio file with mutagen
    try:
        audio = MutagenFile(input_file)
        if audio is None:
            print(f"Error: Could not read metadata from file (unsupported format or no metadata)")
            sys.exit(1)

        print(f"Successfully loaded audio file: {input_file}")
        print(f"File type: {type(audio).__name__}")
    except Exception as e:
        print(f"Error loading audio file: {e}")
        sys.exit(1)

    # Extract metadata
    metadata = {}

    # Basic file information
    metadata['filename'] = os.path.basename(input_file)
    metadata['file_size'] = os.path.getsize(input_file)
    metadata['file_format'] = os.path.splitext(input_file)[1][1:].upper()

    # Audio properties
    if hasattr(audio, 'info'):
        info = audio.info
        metadata['duration_seconds'] = getattr(info, 'length', None)
        metadata['bitrate'] = getattr(info, 'bitrate', None)
        metadata['sample_rate'] = getattr(info, 'sample_rate', None)
        metadata['channels'] = getattr(info, 'channels', None)

    # Extract tags
    tags = {}
    if audio.tags:
        print("\nExtracting metadata tags...")

        # Common tags to extract
        common_tags = [
            'title', 'artist', 'album', 'albumartist', 'date', 'genre',
            'tracknumber', 'discnumber', 'composer', 'performer', 'copyright',
            'encodedby', 'bpm', 'lyrics', 'comment', 'isrc'
        ]

        for key in audio.tags.keys():
            value = audio.tags[key]
            # Convert to string representation
            if isinstance(value, (list, tuple)) and len(value) > 0:
                tags[str(key)] = str(value[0])
            else:
                tags[str(key)] = str(value)

    metadata['tags'] = tags

    # Print extracted metadata
    print("\n" + "="*60)
    print("EXTRACTED METADATA")
    print("="*60)
    print(f"\nFile Information:")
    print(f"  Filename: {metadata['filename']}")
    print(f"  Format: {metadata['file_format']}")
    print(f"  Size: {metadata['file_size']} bytes ({metadata['file_size'] / (1024*1024):.2f} MB)")

    if 'duration_seconds' in metadata and metadata['duration_seconds']:
        duration = metadata['duration_seconds']
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        print(f"  Duration: {minutes}:{seconds:02d} ({duration:.2f} seconds)")

    if 'bitrate' in metadata and metadata['bitrate']:
        print(f"  Bitrate: {metadata['bitrate']} bps ({metadata['bitrate'] / 1000:.0f} kbps)")

    if 'sample_rate' in metadata and metadata['sample_rate']:
        print(f"  Sample Rate: {metadata['sample_rate']} Hz")

    if 'channels' in metadata and metadata['channels']:
        print(f"  Channels: {metadata['channels']}")

    if tags:
        print(f"\nTags Found: {len(tags)}")
        for key, value in sorted(tags.items()):
            print(f"  {key}: {value}")
    else:
        print("\nNo tags found in audio file")

    # Save metadata to JSON file
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_filename = f"{base_name}_metadata.json"
    output_path = os.path.join(args.output_dir, output_filename)

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"\nMetadata saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error saving metadata: {e}")
        sys.exit(1)

    print("\nAudio metadata extraction completed!")


if __name__ == "__main__":
    main()