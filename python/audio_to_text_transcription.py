import subprocess
import sys
import os
import argparse

# Install openai-whisper
subprocess.check_call([sys.executable, "-m", "pip", "install", "openai-whisper"])

import whisper


def main():
    parser = argparse.ArgumentParser(description='Transcribe audio files using OpenAI Whisper')
    parser.add_argument('input_file', help='Path to the input audio/video file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for transcription (default: ./)')
    parser.add_argument('-m', '--model', choices=['tiny', 'base', 'small', 'medium', 'large'],
                        default='base',
                        help='Whisper model size (default: base)')
    parser.add_argument('-l', '--language', default='en',
                        help='Language code (e.g., en, es, fr, de, auto for auto-detect)')
    parser.add_argument('-f', '--format', choices=['txt', 'srt', 'vtt', 'json'], default='txt',
                        help='Output format (default: txt)')

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

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    try:
        print(f"\nLoading Whisper model: {args.model}")
        print(f"This may take a moment on first run as the model is downloaded...")
        model = whisper.load_model(args.model)

        print(f"\nTranscribing audio file: {input_file}")
        print(f"Language: {args.language if args.language != 'auto' else 'auto-detect'}")

        # Transcribe
        transcribe_options = {
            'fp16': False  # Use FP32 for better CPU compatibility
        }

        if args.language != 'auto':
            transcribe_options['language'] = args.language

        result = model.transcribe(input_file, **transcribe_options)

        # Extract info
        detected_language = result.get('language', 'unknown')
        text = result['text']
        segments = result.get('segments', [])

        print(f"\nTranscription completed!")
        print(f"Detected language: {detected_language}")
        print(f"Number of segments: {len(segments)}")
        print(f"Total text length: {len(text)} characters")

        # Save output in requested format
        if args.format == 'txt':
            output_path = os.path.join(args.output_dir, f"{base_name}_transcript.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"\nTranscript saved to: {output_path}")

        elif args.format == 'srt':
            output_path = os.path.join(args.output_dir, f"{base_name}_transcript.srt")
            with open(output_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(segments, 1):
                    start = format_timestamp_srt(segment['start'])
                    end = format_timestamp_srt(segment['end'])
                    text = segment['text'].strip()
                    f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
            print(f"\nSRT subtitle file saved to: {output_path}")

        elif args.format == 'vtt':
            output_path = os.path.join(args.output_dir, f"{base_name}_transcript.vtt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("WEBVTT\n\n")
                for segment in segments:
                    start = format_timestamp_vtt(segment['start'])
                    end = format_timestamp_vtt(segment['end'])
                    text = segment['text'].strip()
                    f.write(f"{start} --> {end}\n{text}\n\n")
            print(f"\nWebVTT subtitle file saved to: {output_path}")

        elif args.format == 'json':
            import json
            output_path = os.path.join(args.output_dir, f"{base_name}_transcript.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\nJSON transcript saved to: {output_path}")

        # Also save a preview of the transcript
        preview_lines = text[:500] + "..." if len(text) > 500 else text
        print(f"\nTranscript preview:\n{preview_lines}")

    except Exception as e:
        print(f"Error during transcription: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def format_timestamp_srt(seconds):
    """Format timestamp for SRT format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def format_timestamp_vtt(seconds):
    """Format timestamp for WebVTT format (HH:MM:SS.mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"


if __name__ == "__main__":
    main()