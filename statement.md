# Project Statement — ImageClarity

## Problem Statement
Photographs of documents may be blurry, poorly illuminated, low contrast, or difficult to read. ImageClarity is a command-line Computer Vision prototype that calculates interpretable image-quality indicators, applies classical image-enhancement operations, and saves reports to help users inspect the effects.

## Scope
The prototype supports image loading and validation, quality-indicator calculation, grayscale/contrast enhancement, adaptive thresholding, optional skew estimation/correction utilities, batch processing, and CSV/JSON reporting. It does not perform OCR, guarantee document readability, or make claims about the semantic correctness of documents.

## Target Users
Students digitising notes, users processing document photographs, and learners studying classical Computer Vision.

## High-Level Features
- Image quality indicators: brightness, intensity variation, Laplacian variance, and heuristic flags.
- Enhancement modes: balanced, grayscale, and binary.
- Batch processing for supported image files.
- CSV and JSON outputs.
- CLI execution and automated tests.

## Originality and Limitations
The code in this repository is an independently assembled educational implementation. Quality thresholds are heuristic and require calibration for a defined dataset. Enhancement can introduce artefacts or make some images less readable; users should compare outputs with originals.
