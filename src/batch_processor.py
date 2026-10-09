"""Folder processing orchestration."""
from pathlib import Path
import cv2

from src.image_loader import SUPPORTED_EXTENSIONS, load_image
from src.quality_metrics import assess_quality
from src.enhancement import enhance_image
from src.report_generator import append_csv_row


def process_batch(input_dir, output_dir, mode="balanced"):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    if not input_path.exists() or not input_path.is_dir():
        raise ValueError(f"Input must be an existing directory: {input_path}")
    output_path.mkdir(parents=True, exist_ok=True)
    csv_path = output_path / "batch_report.csv"
    processed, failed, errors = 0, 0, []
    fieldnames = [
        "input", "output", "mode", "before_brightness", "after_brightness",
        "before_contrast_std", "after_contrast_std", "before_laplacian_variance",
        "after_laplacian_variance", "status", "error"
    ]
    images = sorted(p for p in input_path.iterdir()
                    if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS)
    if not images:
        raise ValueError(f"No supported images found in: {input_path}")

    for image_path in images:
        try:
            image = load_image(image_path)
            before = assess_quality(image)
            enhanced = enhance_image(image, mode=mode)
            target = output_path / f"{image_path.stem}_enhanced.png"
            if not cv2.imwrite(str(target), enhanced):
                raise OSError(f"Could not write output image: {target}")
            after = assess_quality(enhanced)
            append_csv_row(csv_path, {
                "input": str(image_path), "output": str(target), "mode": mode,
                "before_brightness": before["mean_brightness"],
                "after_brightness": after["mean_brightness"],
                "before_contrast_std": before["intensity_std"],
                "after_contrast_std": after["intensity_std"],
                "before_laplacian_variance": before["laplacian_variance"],
                "after_laplacian_variance": after["laplacian_variance"],
                "status": "success", "error": ""
            }, fieldnames)
            processed += 1
        except (ValueError, OSError, FileNotFoundError) as exc:
            failed += 1
            errors.append(f"{image_path.name}: {exc}")
            append_csv_row(csv_path, {
                "input": str(image_path), "output": "", "mode": mode,
                "status": "failed", "error": str(exc)
            }, fieldnames)
    return {"processed": processed, "failed": failed, "errors": errors, "csv_path": str(csv_path)}
