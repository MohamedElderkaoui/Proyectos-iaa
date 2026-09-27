# AGENTS.md

## Project identity

This repository is AccessAI, a computer vision prototype for urban accessibility analysis. The project goal is to detect street-accessibility elements such as sidewalks, curb ramps, and other barriers in urban imagery, with a long-term objective of combining detections with geographic information for accessibility mapping.

The source-of-truth project documents are:
- [PLAN.md](PLAN.md)
- [README.md](README.md)

These documents describe the project as a technical prototype, not a production-ready accessibility system. The current model is a generic YOLO model, and the project still needs a task-specific dataset, a trained model, validation metrics, and integration work.

## Mission

An agent working in this repository must help advance AccessAI responsibly and conservatively:

1. Keep the work aligned with the project plan and the README.
2. Preserve the distinction between prototype and trained production-ready system.
3. Prefer reproducible workflows over guesswork.
4. Avoid claiming that detections correspond to real accessibility quality unless the model has been trained and evaluated on a relevant dataset.
5. Favor clear documentation, dataset hygiene, and traceable validation over speculative improvements.

## Core constraints

- Do not invent dataset contents, class definitions, annotations, or performance metrics.
- Do not describe the current YOLO model as “trained for accessibility” unless the repository actually contains such a trained model and evaluation evidence.
- Do not overstate project maturity; the README explicitly describes the current state as a technical prototype.
- Do not fabricate project files, generated presentation outputs, or results unless the script is explicitly run and verified.
- If a required fact is missing, say so clearly and ask the user for the missing detail instead of guessing.

## Repository map

Main project files and responsibilities:

- [README.md](README.md): user-facing project description, setup instructions, limitations, troubleshooting.
- [PLAN.md](PLAN.md): project roadmap, roles, methodology, risks, and next steps.
- [accessai_demo.py](accessai_demo.py): main inference/demo script for running object detection on an image.
- [generate_accessai_pptx.py](generate_accessai_pptx.py): slide deck generator.
- [generate_accessai_pptx_v2_0_2.py](generate_accessai_pptx_v2_0_2.py): updated presentation generator.
- [inspect_theme.py](inspect_theme.py): theme inspection/reference script for presentation styling.
- [Theme3.thmx](Theme3.thmx): Microsoft PowerPoint theme template used for presentation work.
- [DATA/](DATA/): dataset and support files.
- [DATA/ROD-Dataset/](DATA/ROD-Dataset/): dataset candidate/folder used for model experimentation.

## Project context and expected behavior

The project is currently in an early technical prototype phase.

Expected realities:
- The default demo uses a generic YOLO checkpoint such as `yolov8n.pt` or a generic YOLO weight file.
- The project is expected to move toward a custom dataset and a dedicated accessibility model.
- The final model should be trained on a curated accessibility dataset representing sidewalk and curb-ramp classes, or another approved accessibility class schema.
- Validation should include measured metrics such as precision, recall, F1, and mAP for detection tasks.

The agent must respect this progression: prototype first, trained model second, validated system third.

## Working rules for agents

### 1) Before editing code

- Read the relevant project documentation first: [README.md](README.md) and [PLAN.md](PLAN.md).
- Confirm the task is consistent with the project roadmap and prototype phase.
- If the request touches training, dataset definition, or model evaluation, check whether the project already has a dataset, labels, and class schema in [DATA/](DATA/).
- If the required dataset or class definitions are missing, explicitly state what is missing and ask for confirmation before creating assumptions.

### 2) If the task concerns a dataset

- Do not invent class names beyond the project definition unless the user explicitly approves them.
- Prefer the dataset already present in the repository, if it is the actual source for experiments.
- If labels are in a format other than YOLO, handle conversion carefully and document the conversion logic.
- If the data split is missing, define a clear plan for train/validation/test separation and keep evaluation data separate from training data.
- Preserve the principle: no leakage between training and evaluation.

### 3) If the task concerns model training

- Use YOLO-based training as the default path for object detection, consistent with the project’s prototype and methodology.
- Document the model checkpoint, dataset path, class list, image size, confidence threshold, and training configuration.
- Keep a record of training metrics and discuss failure cases, false positives, and false negatives.
- If using augmentation, explain why it is needed and keep it controlled.
- Avoid claiming improvement without actual validation metrics.

### 4) If the task concerns the demo app

- Respect the current CLI pattern in [accessai_demo.py](accessai_demo.py): input image, optional model, confidence threshold, optional output path.
- Preserve the behavior of saving annotated output images.
- Do not silently replace the model path with a generic checkpoint if the project is meant to use a trained accessibility model.
- If automatic output directories are created, keep them consistent with the project’s existing expectations.

### 5) If the task concerns slides or presentation assets

- Respect the presentation scripts and Samsung branding theme files already present in the repository.
- Do not invent slide content not grounded in the project or the current technical state.
- If the deck is meant to summarize a prototype, present it as a prototype status report, not as a final production deployment.

### 6) If the task concerns documentation

- Keep documentation aligned with what the code and dataset actually support.
- Do not turn the README into marketing copy or claim completion that the repo has not actually demonstrated.
- Prefer explicit, evidence-based language: “prototype,” “baseline,” “candidate dataset,” “not yet validated,” etc.

## Required workflow

When making changes, the agent should follow this order:

1. Clarify the task and constraints.
2. Read the relevant project docs and code.
3. Confirm repository state and missing facts.
4. Make the smallest change that addresses the task.
5. Validate the relevant behavior with the most minimal command available.
6. Report exactly what was changed and what was verified.

## Validation expectations

For this project, validation must be minimal but honest.

Examples of acceptable validation actions:
- Run a demo on a single image with the current script when a valid image is available.
- Verify import and script startup behavior for Python scripts.
- Check that the output directory is created and the annotated image file is written.
- Confirm that the repository still parses and shows the expected help output for a CLI script.

Examples of unacceptable validation claims:
- “The model works for accessibility” without a trained model and dataset validation.
- “The project is complete” without actual training or end-to-end evidence.
- “The presentation is final” without running the generator and confirming output generation.

## Tooling and environment

The repo expects Python 3.10+ and a local virtual environment or conda environment.

Use the project environment consistently:
- Prefer the repository’s active virtual environment.
- Avoid broad, uncontrolled dependency changes unless the task specifically requires them.
- Do not install packages globally when a project-local environment is available.

Typical project commands referenced by the docs include:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install ultralytics python-pptx
```

Or in conda:

```powershell
conda activate <environment-name>
```

## Sensitive project truths

These statements are important and should always be preserved in updates, planning, code comments, and generated documentation:

- AccessAI is a prototype.
- The current model is not yet trained for accessibility-specific classes.
- Detection quality must be verified with a relevant dataset and metrics.
- Detections cannot be treated as proof of accessibility or inaccessibility without validation.

## Decision rules for ambiguous requests

If a user request is ambiguous, follow this order:

1. Ask for the missing fact or decision.
2. Prefer the project’s existing technical plan over a new direction.
3. Keep the work grounded in the repo’s actual state and management docs.
4. Do not add new features or claims that are not justified by the project materials.

## Final rule

The agent must act like a careful project collaborator, not an imaginative architect. The job is to support the real AccessAI project as described in [PLAN.md](PLAN.md) and [README.md](README.md), with disciplined evidence, clear caveats, and exact technical honesty.
