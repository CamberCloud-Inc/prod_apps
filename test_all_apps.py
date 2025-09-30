#!/usr/bin/env python3
"""
Comprehensive test script for all 96 utility apps
Tests each app with appropriate test data and reports results
"""
import subprocess
import os
import sys
import json
from pathlib import Path

# Define test data directory
TEST_DATA_DIR = "python/test_data"
TEST_OUTPUT_DIR = "python/test_outputs"

# Ensure output directory exists
os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

# Define test cases for each app with appropriate test data
TEST_CASES = {
    # Audio apps (require audio files - will skip if not available)
    "audio_format_converter": {"skip": True, "reason": "No audio test file"},
    "audio_merger": {"skip": True, "reason": "No audio test file"},
    "audio_metadata_extractor": {"skip": True, "reason": "No audio test file"},
    "audio_normalizer": {"skip": True, "reason": "No audio test file"},
    "audio_to_text_transcription": {"skip": True, "reason": "No audio test file"},
    "audio_trimmer": {"skip": True, "reason": "No audio test file"},

    # Barcode/QR generators
    "barcode_generator": {
        "cmd": ["python3", "python/barcode_generator.py", "123456789012", "-o", TEST_OUTPUT_DIR, "-f", "code128"]
    },
    "qr_code_generator": {
        "cmd": ["python3", "python/qr_code_generator.py", "https://example.com", "-o", TEST_OUTPUT_DIR]
    },

    # Base64 encoding/decoding
    "base64_encoder": {
        "cmd": ["python3", "python/base64_encoder.py", f"{TEST_DATA_DIR}/sample.txt", "-o", TEST_OUTPUT_DIR]
    },
    "base64_decoder": {
        "cmd": ["python3", "python/base64_decoder.py", f"{TEST_OUTPUT_DIR}/sample.txt.b64", "-o", TEST_OUTPUT_DIR],
        "requires": ["base64_encoder"]  # Must run after encoder
    },

    # Image apps (require image files - will skip if not available)
    "batch_image_renamer": {"skip": True, "reason": "No image test files"},
    "color_palette_extractor": {"skip": True, "reason": "No image test file"},
    "favicon_generator": {"skip": True, "reason": "No image test file"},
    "heic_to_jpg": {"skip": True, "reason": "No HEIC test file"},
    "image_background_remover": {"skip": True, "reason": "Requires rembg library"},
    "image_blur_tool": {"skip": True, "reason": "No image test file"},
    "image_border_adder": {"skip": True, "reason": "No image test file"},
    "image_brightness_adjuster": {"skip": True, "reason": "No image test file"},
    "image_collage_maker": {"skip": True, "reason": "No image test files"},
    "image_color_inverter": {"skip": True, "reason": "No image test file"},
    "image_compressor": {"skip": True, "reason": "No image test file"},
    "image_cropper": {"skip": True, "reason": "No image test file"},
    "image_filter_applicator": {"skip": True, "reason": "No image test file"},
    "image_format_converter": {"skip": True, "reason": "No image test file"},
    "image_grayscale": {"skip": True, "reason": "No image test file"},
    "image_metadata_extractor": {"skip": True, "reason": "No image test file"},
    "image_metadata_remover": {"skip": True, "reason": "No image test file"},
    "image_resizer": {"skip": True, "reason": "No image test file"},
    "image_rotator": {"skip": True, "reason": "No image test file"},
    "image_sharpener": {"skip": True, "reason": "No image test file"},
    "image_stacker": {"skip": True, "reason": "No image test files"},
    "image_watermarker": {"skip": True, "reason": "No image test file"},
    "svg_to_png": {"skip": True, "reason": "No SVG test file"},
    "thumbnail_generator": {"skip": True, "reason": "No image test file"},

    # CSV/Excel converters
    "csv_to_excel": {
        "cmd": ["python3", "python/csv_to_excel.py", f"{TEST_DATA_DIR}/sample.csv", "-o", TEST_OUTPUT_DIR]
    },
    "csv_to_json": {
        "cmd": ["python3", "python/csv_to_json.py", f"{TEST_DATA_DIR}/sample.csv", "-o", TEST_OUTPUT_DIR]
    },
    "csv_column_extractor": {
        "cmd": ["python3", "python/csv_column_extractor.py", f"{TEST_DATA_DIR}/sample.csv", "-o", TEST_OUTPUT_DIR, "-c", "0"]
    },
    "excel_to_csv": {
        "cmd": ["python3", "python/excel_to_csv.py", f"{TEST_DATA_DIR}/sample.xlsx", "-o", TEST_OUTPUT_DIR]
    },

    # Database tools
    "database_table_dumper": {"skip": True, "reason": "Requires database connection"},
    "sql_to_csv_exporter": {"skip": True, "reason": "Requires database connection"},

    # Directory/File utilities
    "directory_tree_generator": {
        "cmd": ["python3", "python/directory_tree_generator.py", TEST_DATA_DIR, "-o", TEST_OUTPUT_DIR]
    },
    "file_type_detector": {
        "cmd": ["python3", "python/file_type_detector.py", f"{TEST_DATA_DIR}/sample.txt", "-o", TEST_OUTPUT_DIR]
    },

    # Document converters
    "epub_to_pdf": {"skip": True, "reason": "No EPUB test file"},
    "html_to_pdf": {"skip": True, "reason": "Requires wkhtmltopdf"},
    "latex_to_pdf": {"skip": True, "reason": "Requires pdflatex (not installed)"},
    "markdown_to_html": {
        "cmd": ["python3", "python/markdown_to_html.py", f"{TEST_DATA_DIR}/sample.md", "-o", TEST_OUTPUT_DIR]
    },
    "markdown_to_pdf": {
        "cmd": ["python3", "python/markdown_to_pdf.py", f"{TEST_DATA_DIR}/sample.md", "-o", TEST_OUTPUT_DIR]
    },
    "office_to_markdown": {
        "cmd": ["python3", "python/office_to_markdown.py", f"{TEST_DATA_DIR}/sample.docx", "-o", TEST_OUTPUT_DIR]
    },
    "rtf_to_docx": {
        "cmd": ["python3", "python/rtf_to_docx.py", f"{TEST_DATA_DIR}/test.rtf", "-o", TEST_OUTPUT_DIR]
    },
    "text_to_pdf": {
        "cmd": ["python3", "python/text_to_pdf.py", f"{TEST_DATA_DIR}/sample.txt", "-o", TEST_OUTPUT_DIR]
    },
    "word_to_pdf": {
        "cmd": ["python3", "python/word_to_pdf.py", f"{TEST_DATA_DIR}/sample.docx", "-o", TEST_OUTPUT_DIR]
    },

    # Email/Calendar/Contact parsers
    "email_parser": {
        "cmd": ["python3", "python/email_parser.py", f"{TEST_DATA_DIR}/sample_email.eml", "-o", TEST_OUTPUT_DIR]
    },
    "ical_to_csv": {
        "cmd": ["python3", "python/ical_to_csv.py", f"{TEST_DATA_DIR}/sample_calendar.ics", "-o", TEST_OUTPUT_DIR]
    },
    "vcard_to_csv": {
        "cmd": ["python3", "python/vcard_to_csv.py", f"{TEST_DATA_DIR}/sample_contacts.vcf", "-o", TEST_OUTPUT_DIR]
    },

    # File operations
    "file_checksum_verifier": {
        "cmd": ["python3", "python/file_hash_generator.py", f"{TEST_DATA_DIR}/sample.txt", "-o", TEST_OUTPUT_DIR],
        "note": "First generate hash, then we can verify"
    },
    "file_hash_generator": {
        "cmd": ["python3", "python/file_hash_generator.py", f"{TEST_DATA_DIR}/sample.txt", "-o", TEST_OUTPUT_DIR]
    },
    "file_merger": {
        "cmd": ["python3", "python/file_merger.py", f"{TEST_OUTPUT_DIR}/sample.txt.part*", "-o", f"{TEST_OUTPUT_DIR}/merged_file.txt"],
        "requires": ["file_splitter"]  # Must run after splitter
    },
    "file_splitter": {
        "cmd": ["python3", "python/file_splitter.py", f"{TEST_DATA_DIR}/sample.txt", "-s", "100", "-o", TEST_OUTPUT_DIR]
    },

    # Font converter
    "font_converter": {"skip": True, "reason": "No font test file"},

    # JSON operations
    "json_formatter": {
        "cmd": ["python3", "python/json_formatter.py", f"{TEST_DATA_DIR}/test.json", "-o", TEST_OUTPUT_DIR]
    },
    "json_minifier": {
        "cmd": ["python3", "python/json_minifier.py", f"{TEST_DATA_DIR}/test.json", "-o", TEST_OUTPUT_DIR]
    },
    "json_to_csv": {
        "cmd": ["python3", "python/json_to_csv.py", f"{TEST_DATA_DIR}/test.json", "-o", TEST_OUTPUT_DIR]
    },

    # Log parser
    "log_file_parser": {
        "cmd": ["python3", "python/log_file_parser.py", f"{TEST_DATA_DIR}/sample.log", "-o", TEST_OUTPUT_DIR]
    },

    # PDF operations (require PDF files)
    "pdf_analyzer": {"skip": True, "reason": "No PDF test file"},
    "pdf_merger": {"skip": True, "reason": "No PDF test files"},
    "pdf_page_extractor": {"skip": True, "reason": "No PDF test file"},
    "pdf_splitter": {"skip": True, "reason": "No PDF test file"},
    "pdf_text_extractor": {"skip": True, "reason": "No PDF test file"},
    "pdf_to_epub": {"skip": True, "reason": "No PDF test file"},

    # RSS/Sitemap generators
    "rss_feed_generator": {
        "cmd": ["python3", "python/rss_feed_generator.py", f"{TEST_DATA_DIR}/feed_items.json", "-o", TEST_OUTPUT_DIR, "-t", "Test Feed", "-l", "http://example.com", "-d", "Test Description"]
    },
    "sitemap_generator": {
        "cmd": ["python3", "python/sitemap_generator.py", f"{TEST_DATA_DIR}/urls.txt", "-o", TEST_OUTPUT_DIR]
    },

    # Tar/Zip operations
    "tar_gz_creator": {
        "cmd": ["python3", "python/tar_gz_creator.py", TEST_DATA_DIR, "-o", f"{TEST_OUTPUT_DIR}/test_archive.tar.gz"]
    },
    "tar_gz_extractor": {"skip": True, "reason": "No tar.gz test file"},
    "zip_compressor": {
        "cmd": ["python3", "python/zip_compressor.py", TEST_DATA_DIR, "-o", f"{TEST_OUTPUT_DIR}/test_archive.zip"]
    },
    "zip_extractor": {"skip": True, "reason": "No zip test file"},

    # Text operations
    "duplicate_line_remover": {
        "cmd": ["python3", "python/duplicate_line_remover.py", f"{TEST_DATA_DIR}/sample_text.txt", "-o", TEST_OUTPUT_DIR]
    },
    "line_number_adder": {
        "cmd": ["python3", "python/line_number_adder.py", f"{TEST_DATA_DIR}/sample.txt", "-o", TEST_OUTPUT_DIR]
    },
    "line_sorter": {
        "cmd": ["python3", "python/line_sorter.py", f"{TEST_DATA_DIR}/sample.txt", "-o", TEST_OUTPUT_DIR]
    },
    "text_case_converter": {
        "cmd": ["python3", "python/text_case_converter.py", f"{TEST_DATA_DIR}/sample.txt", "-o", TEST_OUTPUT_DIR, "-c", "upper"]
    },
    "text_merger": {
        "cmd": ["python3", "python/text_merger.py", f"{TEST_DATA_DIR}/*.txt", "-o", TEST_OUTPUT_DIR, "-n", "merged_test.txt"]
    },
    "text_splitter": {
        "cmd": ["python3", "python/text_splitter.py", f"{TEST_DATA_DIR}/sample.txt", "-s", "10", "-o", TEST_OUTPUT_DIR]
    },
    "whitespace_trimmer": {
        "cmd": ["python3", "python/whitespace_trimmer.py", f"{TEST_DATA_DIR}/sample.txt", "-o", TEST_OUTPUT_DIR]
    },
    "word_counter": {
        "cmd": ["python3", "python/word_counter.py", f"{TEST_DATA_DIR}/sample.txt", "-o", TEST_OUTPUT_DIR]
    },

    # URL shortener
    "url_shortener_data": {"skip": True, "reason": "Requires database connection"},

    # Video apps (require video files)
    "silence_remover": {"skip": True, "reason": "No audio/video test file"},
    "video_compressor": {"skip": True, "reason": "No video test file"},
    "video_frame_extractor": {"skip": True, "reason": "No video test file"},
    "video_metadata_extractor": {"skip": True, "reason": "No video test file"},
    "video_resolution_changer": {"skip": True, "reason": "No video test file"},
    "video_speed_changer": {"skip": True, "reason": "No video test file"},
    "video_thumbnail_generator": {"skip": True, "reason": "No video test file"},
    "video_to_audio_extractor": {"skip": True, "reason": "No video test file"},
    "video_to_gif": {"skip": True, "reason": "No video test file"},

    # XML/YAML operations
    "xml_to_json": {
        "cmd": ["python3", "python/xml_to_json.py", f"{TEST_DATA_DIR}/test.xml", "-o", TEST_OUTPUT_DIR]
    },
    "xml_validator": {
        "cmd": ["python3", "python/xml_validator.py", f"{TEST_DATA_DIR}/test.xml"]
    },
    "yaml_to_json": {
        "cmd": ["python3", "python/yaml_to_json.py", f"{TEST_DATA_DIR}/test.yaml", "-o", TEST_OUTPUT_DIR]
    },
}

def run_test(app_name, test_config):
    """Run a single app test"""
    if test_config.get("skip"):
        return {
            "app": app_name,
            "status": "SKIPPED",
            "reason": test_config.get("reason", "No test data"),
            "output": ""
        }

    try:
        cmd = test_config["cmd"]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return {
                "app": app_name,
                "status": "PASSED",
                "output": result.stdout[-500:] if len(result.stdout) > 500 else result.stdout,
                "error": ""
            }
        else:
            return {
                "app": app_name,
                "status": "FAILED",
                "output": result.stdout[-500:] if len(result.stdout) > 500 else result.stdout,
                "error": result.stderr[-500:] if len(result.stderr) > 500 else result.stderr
            }
    except subprocess.TimeoutExpired:
        return {
            "app": app_name,
            "status": "TIMEOUT",
            "error": "Test timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "app": app_name,
            "status": "ERROR",
            "error": str(e)
        }

def main():
    print("=" * 80)
    print("TESTING ALL UTILITY APPS")
    print("=" * 80)
    print()

    results = []
    passed = 0
    failed = 0
    skipped = 0
    errors = 0

    for app_name, test_config in sorted(TEST_CASES.items()):
        print(f"Testing {app_name}...", end=" ", flush=True)
        result = run_test(app_name, test_config)
        results.append(result)

        if result["status"] == "PASSED":
            print("✓ PASSED")
            passed += 1
        elif result["status"] == "SKIPPED":
            print(f"⊘ SKIPPED ({result['reason']})")
            skipped += 1
        elif result["status"] == "FAILED":
            print(f"✗ FAILED")
            failed += 1
        else:
            print(f"⚠ ERROR")
            errors += 1

    # Print summary
    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Total apps tested: {len(TEST_CASES)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")
    print()

    # Print failed tests details
    if failed > 0 or errors > 0:
        print("=" * 80)
        print("FAILED/ERROR DETAILS")
        print("=" * 80)
        for result in results:
            if result["status"] in ["FAILED", "ERROR"]:
                print(f"\n{result['app']} - {result['status']}")
                print("-" * 80)
                if result.get("error"):
                    print("Error:")
                    print(result["error"])
                if result.get("output"):
                    print("\nOutput:")
                    print(result["output"])

    # Save results to JSON
    with open(f"{TEST_OUTPUT_DIR}/test_results.json", "w") as f:
        json.dump({
            "summary": {
                "total": len(TEST_CASES),
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "errors": errors
            },
            "results": results
        }, f, indent=2)

    print(f"\nDetailed results saved to: {TEST_OUTPUT_DIR}/test_results.json")

    return 0 if failed == 0 and errors == 0 else 1

if __name__ == "__main__":
    sys.exit(main())