"""ImageClarity command-line entry point."""
import argparse
import sys
import json
from pathlib import Path

from src.image_loader import load_image
from src.quality_metrics import assess_quality
from src.enhancement import enhance_image, create_comparison_image
from src.report_generator import write_json_report, append_csv_row
from src.batch_processor import process_batch


def build_parser():
    parser = argparse.ArgumentParser(
        prog="imageclarity",
        description="Inspect and enhance document images from the command line."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    inspect = sub.add_parser("inspect", help="Calculate image quality indicators.")
    inspect.add_argument("--input", required=True, help="Path to an image.")
    inspect.add_argument("--output", default="outputs", help="Output directory for JSON report.")

    enhance = sub.add_parser("enhance", help="Enhance one document image.")
    enhance.add_argument("--input", required=True, help="Path to an image.")
    enhance.add_argument("--output", default="outputs", help="Output directory.")
    enhance.add_argument("--mode", choices=["balanced", "grayscale", "binary"], default="balanced")

    batch = sub.add_parser("batch", help="Process all supported images in a folder.")
    batch.add_argument("--input", required=True, help="Input folder.")
    batch.add_argument("--output", default="outputs", help="Output directory.")
    batch.add_argument("--mode", choices=["balanced", "grayscale", "binary"], default="balanced")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        if args.command == "inspect":
            image = load_image(args.input)
            metrics = assess_quality(image)
            report_path = output_dir / f"{Path(args.input).stem}_quality.json"
            write_json_report(report_path, {"input": str(Path(args.input)), "metrics": metrics})
            print(json_summary(metrics))
            print(f"Report saved: {report_path}")
        elif args.command == "enhance":
            image = load_image(args.input)
            metrics_before = assess_quality(image)
            result = enhance_image(image, mode=args.mode)
            target = output_dir / f"{Path(args.input).stem}_enhanced.png"
            import cv2
            if not cv2.imwrite(str(target), result):
                raise OSError(f"Could not write output image: {target}")
            
            # Create side-by-side comparison image
            comparison = create_comparison_image(image, result)
            
            comparison_target = output_dir / f"{Path(args.input).stem}_comparison.png"
            
            if not cv2.imwrite(str(comparison_target), comparison):
                raise OSError(f"Could not write comparison image: {comparison_target}")
            metrics_after = assess_quality(result)
            report_path = output_dir / f"{Path(args.input).stem}_comparison.json"
            write_json_report(report_path, {
                "input": str(Path(args.input)),
                "output": str(target),
                "mode": args.mode,
                "before": metrics_before,
                "after": metrics_after,
                "note": "Metrics are indicators, not a guarantee of readability or OCR accuracy."
            })
            print(f"Enhanced image saved: {target}")
            print(f"Comparison image saved: {comparison_target}")
            print(f"Comparison report saved: {report_path}")
            print("Before:", json_summary(metrics_before))
            print("After: ", json_summary(metrics_after))
        elif args.command == "batch":
            summary = process_batch(args.input, output_dir, mode=args.mode)
            print(f"Processed {summary['processed']} image(s); failed: {summary['failed']}.")
            print(f"CSV report saved: {summary['csv_path']}")
            if summary["errors"]:
                print("Some files could not be processed:")
                for error in summary["errors"]:
                    print(f" - {error}")
                return 1
    except (ValueError, FileNotFoundError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 0


def json_summary(metrics):
    return (
        f"width={metrics['width']}, height={metrics['height']}, "
        f"brightness={metrics['mean_brightness']:.2f}, "
        f"contrast_std={metrics['intensity_std']:.2f}, "
        f"laplacian_variance={metrics['laplacian_variance']:.2f}, "
        f"blur_indicator={metrics['blur_indicator']}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
