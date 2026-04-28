# 🔬 UV Fluorescence Microplastics Detection

> A cost-effective, dye-free microplastics detection system combining 
> UV-induced fluorescence imaging with YOLOv8 OBB deep learning — 
> designed for field deployment on edge hardware.

---

##  Overview

Microplastic contamination in water is a critical environmental and 
public health challenge. Existing detection methods (FTIR, Raman 
Spectroscopy, Nile Red staining) are expensive, lab-dependent, and 
require chemical reagents.

This project proposes a fully integrated, low-cost alternative:
- **UV-induced natural fluorescence** — no chemical dyes needed
- **Custom hardware pipeline** — portable and field-deployable
- **YOLOv8 OBB** — deep learning with oriented bounding boxes
- **Edge computing** — runs on Jetson Nano

---

##  Hardware Setup

| Component | Purpose |
|-----------|---------|
| UV Light Source | Induces fluorescence in microplastics |
| Polarizer Filter | Eliminates UV glare, improves contrast |
| Camera Module | Captures fluorescence images |
| Acrylic Sample Chamber | Holds water samples |
| Jetson Nano | Edge computing platform |
| Dark Box | Eliminates ambient light interference |

---

##  Dataset

| Property | Details |
|----------|---------|
| Total Images | 1,850 |
| Microplastic Classes | 5 (1mm, 2mm, 3mm, 4mm, 5mm) |
| Non-plastic Class | 1 |
| Annotation Tool | Label Studio |
| Annotation Type | Oriented Bounding Box (OBB) |
| Dataset Origin | **Entirely original — built from scratch** |

>  This dataset does not exist anywhere else. 
> It was designed, collected, and annotated specifically for this research.

---

##  Model

| Property | Details |
|----------|---------|
| Architecture | YOLOv8n-OBB |
| Training Images | 140 (initial subset) |
| Epochs | 50 |
| Image Size | 640×640 |
| Hardware | MacBook → Jetson Nano |

---

## Results (Initial Model)

| Metric | Score |
|--------|-------|
| **mAP@50** | **99.5%** |
| **mAP@50-95** | **~85%** |
| **Precision** | **100%** |
| **Recall** | **97.8%** |
| **F1 Score** | **1.00** |

> Note: Results on initial 140-image subset. 
> Final model training on full 1850-image dataset in progress.
> <img width="533" height="232" alt="image" src="https://github.com/user-attachments/assets/3590b8c5-aaf4-41da-8188-74f0f44e0ba6" />

---

## Pipeline




