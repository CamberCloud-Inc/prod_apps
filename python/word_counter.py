import argparse
import os
import sys
import re


def main():
    parser = argparse.ArgumentParser(description='Count words, characters, and lines in text documents')
    parser.add_argument('input_file', help='Path to the input text file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for statistics report (default: ./)')

    args = parser.parse_args()

    print(f"Current working directory: {os.getcwd()}")
    print(f"Received input_file argument: {args.input_file}")

    # Expand user path if provided
    input_path = os.path.expanduser(args.input_file)
    print(f"Expanded input_path: {input_path}")

    if not os.path.exists(input_path):
        print(f"Error: Input file not found at: {input_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Read the input file
    print(f"Reading input file: {input_path}")
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Calculate statistics
    print("Analyzing text...")
    
    # Count characters
    char_count = len(content)
    char_count_no_spaces = len(content.replace(' ', '').replace('\n', '').replace('\t', ''))
    
    # Count lines
    lines = content.split('\n')
    line_count = len(lines)
    non_empty_lines = [line for line in lines if line.strip()]
    non_empty_line_count = len(non_empty_lines)
    
    # Count words
    words = re.findall(r'\b\w+\b', content)
    word_count = len(words)
    
    # Count unique words (case-insensitive)
    unique_words = set(word.lower() for word in words)
    unique_word_count = len(unique_words)
    
    # Calculate average word length
    if words:
        avg_word_length = sum(len(word) for word in words) / len(words)
    else:
        avg_word_length = 0
    
    # Count sentences (rough approximation)
    sentences = re.split(r'[.!?]+', content)
    sentence_count = len([s for s in sentences if s.strip()])
    
    # Count paragraphs (separated by blank lines)
    paragraphs = re.split(r'\n\s*\n', content)
    paragraph_count = len([p for p in paragraphs if p.strip()])

    # Print statistics to console
    print("\n" + "="*50)
    print("TEXT STATISTICS")
    print("="*50)
    print(f"Characters (total):        {char_count:,}")
    print(f"Characters (no spaces):    {char_count_no_spaces:,}")
    print(f"Words:                     {word_count:,}")
    print(f"Unique words:              {unique_word_count:,}")
    print(f"Average word length:       {avg_word_length:.2f}")
    print(f"Lines (total):             {line_count:,}")
    print(f"Lines (non-empty):         {non_empty_line_count:,}")
    print(f"Sentences (approx):        {sentence_count:,}")
    print(f"Paragraphs:                {paragraph_count:,}")
    print("="*50 + "\n")

    # Generate output filename
    input_filename = os.path.basename(input_path)
    name_without_ext = os.path.splitext(input_filename)[0]
    output_filename = f"{name_without_ext}_stats.txt"
    output_path = os.path.join(args.output_dir, output_filename)

    # Write the statistics report
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("="*50 + "\n")
            f.write("TEXT STATISTICS REPORT\n")
            f.write("="*50 + "\n")
            f.write(f"File: {input_filename}\n")
            f.write(f"\n")
            f.write(f"Characters (total):        {char_count:,}\n")
            f.write(f"Characters (no spaces):    {char_count_no_spaces:,}\n")
            f.write(f"Words:                     {word_count:,}\n")
            f.write(f"Unique words:              {unique_word_count:,}\n")
            f.write(f"Average word length:       {avg_word_length:.2f}\n")
            f.write(f"Lines (total):             {line_count:,}\n")
            f.write(f"Lines (non-empty):         {non_empty_line_count:,}\n")
            f.write(f"Sentences (approx):        {sentence_count:,}\n")
            f.write(f"Paragraphs:                {paragraph_count:,}\n")
            f.write("="*50 + "\n")
        
        print(f"Statistics report saved to: {output_path}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    print("Word counting completed!")


if __name__ == "__main__":
    main()
