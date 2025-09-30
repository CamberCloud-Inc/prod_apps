import subprocess
import sys
import os
import argparse

# Install pydub and moviepy
subprocess.check_call([sys.executable, "-m", "pip", "install", "pydub", "moviepy"])

from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from moviepy.editor import VideoFileClip, concatenate_videoclips
import tempfile


def main():
    parser = argparse.ArgumentParser(description='Remove silent parts from audio/video files')
    parser.add_argument('input_file', help='Path to the input audio or video file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for processed file (default: ./)')
    parser.add_argument('-t', '--threshold', type=int, default=-40,
                        help='Silence threshold in dBFS (default: -40, lower = more sensitive)')
    parser.add_argument('-m', '--min-silence', type=int, default=500,
                        help='Minimum silence length in milliseconds to remove (default: 500)')

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
        print(f"Error: File not found at: {input_file}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Detect file type
    file_ext = os.path.splitext(input_file)[1].lower()
    is_video = file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm']

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    try:
        if is_video:
            print(f"\nProcessing video file: {input_file}")
            output_filename = f"{base_name}_nosilence.mp4"
            output_path = os.path.join(args.output_dir, output_filename)
            process_video(input_file, output_path, args.threshold, args.min_silence)
        else:
            print(f"\nProcessing audio file: {input_file}")
            output_filename = f"{base_name}_nosilence{file_ext}"
            output_path = os.path.join(args.output_dir, output_filename)
            process_audio(input_file, output_path, args.threshold, args.min_silence)

        print(f"\nSilence removal completed!")
        print(f"Output saved to: {output_path}")

    except Exception as e:
        print(f"Error removing silence: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def process_audio(input_file, output_path, threshold, min_silence_len):
    """Process audio file to remove silence"""
    print(f"Loading audio file...")

    # Load audio
    audio = AudioSegment.from_file(input_file)
    original_duration = len(audio) / 1000.0

    print(f"Original duration: {original_duration:.2f} seconds")
    print(f"Detecting non-silent segments (threshold: {threshold} dBFS, min silence: {min_silence_len}ms)...")

    # Detect non-silent chunks
    nonsilent_ranges = detect_nonsilent(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=threshold
    )

    if not nonsilent_ranges:
        print("Warning: No non-silent segments detected. Output will be empty or very short.")
        # Create a very short silent audio
        output_audio = AudioSegment.silent(duration=100)
    else:
        print(f"Found {len(nonsilent_ranges)} non-silent segments")

        # Concatenate non-silent chunks
        output_audio = AudioSegment.empty()
        for i, (start, end) in enumerate(nonsilent_ranges):
            print(f"  Segment {i+1}: {start/1000:.2f}s - {end/1000:.2f}s")
            output_audio += audio[start:end]

    new_duration = len(output_audio) / 1000.0
    time_saved = original_duration - new_duration
    percentage_saved = (time_saved / original_duration) * 100 if original_duration > 0 else 0

    print(f"\nExporting audio...")
    output_audio.export(output_path, format=os.path.splitext(output_path)[1][1:])

    print(f"New duration: {new_duration:.2f} seconds")
    print(f"Time removed: {time_saved:.2f} seconds ({percentage_saved:.1f}%)")


def process_video(input_file, output_path, threshold, min_silence_len):
    """Process video file to remove silence"""
    print(f"Loading video file...")

    # Load video
    video = VideoFileClip(input_file)
    original_duration = video.duration

    print(f"Original duration: {original_duration:.2f} seconds")
    print(f"Resolution: {video.size[0]}x{video.size[1]}")
    print(f"FPS: {video.fps}")

    # Extract audio to temporary file
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
        temp_audio_path = temp_audio.name

    print(f"Extracting audio for analysis...")
    video.audio.write_audiofile(temp_audio_path, logger=None)

    # Load audio with pydub
    audio = AudioSegment.from_wav(temp_audio_path)

    print(f"Detecting non-silent segments (threshold: {threshold} dBFS, min silence: {min_silence_len}ms)...")

    # Detect non-silent chunks
    nonsilent_ranges = detect_nonsilent(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=threshold
    )

    # Clean up temp audio file
    os.unlink(temp_audio_path)

    if not nonsilent_ranges:
        print("Warning: No non-silent segments detected. Creating minimal output.")
        # Create a 1-second clip from the beginning
        output_video = video.subclip(0, min(1, video.duration))
    else:
        print(f"Found {len(nonsilent_ranges)} non-silent segments")

        # Create video subclips for non-silent ranges
        clips = []
        for i, (start_ms, end_ms) in enumerate(nonsilent_ranges):
            start_sec = start_ms / 1000.0
            end_sec = end_ms / 1000.0
            print(f"  Segment {i+1}: {start_sec:.2f}s - {end_sec:.2f}s")

            # Make sure we don't exceed video duration
            end_sec = min(end_sec, video.duration)
            if start_sec < end_sec:
                clips.append(video.subclip(start_sec, end_sec))

        # Concatenate clips
        print(f"\nConcatenating {len(clips)} video segments...")
        output_video = concatenate_videoclips(clips)

    new_duration = output_video.duration
    time_saved = original_duration - new_duration
    percentage_saved = (time_saved / original_duration) * 100 if original_duration > 0 else 0

    print(f"\nExporting video...")
    output_video.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        bitrate='2000k',
        audio_bitrate='192k',
        preset='medium',
        threads=4
    )

    video.close()
    output_video.close()

    print(f"New duration: {new_duration:.2f} seconds")
    print(f"Time removed: {time_saved:.2f} seconds ({percentage_saved:.1f}%)")


if __name__ == "__main__":
    main()