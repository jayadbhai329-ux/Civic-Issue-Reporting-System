"""
Reproducible Object Detection Training Pipeline for Civic Issues
-----------------------------------------------------------------
Translates COCO annotations from `civic_issue_dataset-master` into YOLOv8 format,
sets up training/validation/test splits, and launches transfer learning.

Target Civic Classes:
0: crack
1: blurline
2: garbage
3: pothole
4: manhole

Usage:
1. Place image directories (`garbage/`, `pothole/`, `road/`, `new_images/`) into the dataset folder:
   C:\\Users\\Asus\\Downloads\\civic_issue_dataset-master\\civic_issue_dataset-master\\
2. Run this script:
   python train_object_detector.py
"""

import os
import sys
import json
import shutil
import random
from collections import defaultdict

TARGET_CLASSES = [
    "crack",
    "blurline",
    "garbage",
    "pothole",
    "manhole"
]
CLASS_TO_ID = {name: idx for idx, name in enumerate(TARGET_CLASSES)}


def convert_coco_to_yolo(coco_dir, dataset_output_dir):
    """
    Parses COCO JSON annotations, verifies image presence, converts bounding boxes
    [x, y, w, h] to normalized YOLO format [class_id, x_c, y_c, w_norm, h_norm],
    and organizes into train/val/test splits (70/15/15).
    """
    print("="*60)
    print("PREPARING DATASET FOR OBJECT DETECTION")
    print("="*60)
    
    json_files = [
        "garbage_coco.json",
        "pothole_coco.json",
        "road_coco.json",
        "new_images_coco.json"
    ]
    
    # Check if images exist before attempting conversion
    sample_images = ["garbage/77770000001.jpg", "pothole/99999000001.jpg"]
    missing = [img for img in sample_images if not os.path.exists(os.path.join(coco_dir, img))]
    if len(missing) == len(sample_images):
        print("\n[STOPPING - IMAGE FILES NOT FOUND]")
        print(f"Error: Physical image directories were not found in: {coco_dir}")
        print("To train this model:")
        print("1. Download the images from the author's drive or external mirror:")
        print("   Drive URL: https://drive.google.com/open?id=1fvXn-SHSCu5jY4LPy79jeSdWrMhPkYPo")
        print("2. Extract the folders ('garbage', 'pothole', 'road', 'new_images') into:")
        print(f"   {coco_dir}")
        print("3. Re-run this training script.\n")
        return False
        
    # Create YOLO directory structure
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(dataset_output_dir, "images", split), exist_ok=True)
        os.makedirs(os.path.join(dataset_output_dir, "labels", split), exist_ok=True)
        
    all_images = {}
    annotations_by_image = defaultdict(list)
    
    for jname in json_files:
        jpath = os.path.join(coco_dir, jname)
        if not os.path.exists(jpath):
            continue
        with open(jpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        cats = {c['id']: c['name'] for c in data.get('categories', [])}
        for img in data.get('images', []):
            all_images[img['id']] = img
            
        for ann in data.get('annotations', []):
            cid = ann.get('category_id')
            cname = cats.get(cid, '')
            if cname in CLASS_TO_ID:
                annotations_by_image[ann['image_id']].append({
                    "class_id": CLASS_TO_ID[cname],
                    "bbox": ann.get('bbox', [])
                })
                
    # Filter to images that actually exist on disk and have civic annotations
    valid_img_ids = []
    for img_id, anns in annotations_by_image.items():
        if not anns:
            continue
        img_info = all_images.get(img_id)
        if not img_info:
            continue
        img_path = os.path.join(coco_dir, img_info['file_name'])
        if os.path.exists(img_path):
            valid_img_ids.append(img_id)
            
    if not valid_img_ids:
        print("[ERROR] No valid images with civic issue annotations found on disk.")
        return False
        
    random.seed(42)
    random.shuffle(valid_img_ids)
    
    n_total = len(valid_img_ids)
    n_train = int(n_total * 0.70)
    n_val = int(n_total * 0.15)
    
    splits = {
        "train": valid_img_ids[:n_train],
        "val": valid_img_ids[n_train:n_train+n_val],
        "test": valid_img_ids[n_train+n_val:]
    }
    
    print(f"Converting annotations: Train={len(splits['train'])}, Val={len(splits['val'])}, Test={len(splits['test'])}")
    
    for split_name, img_ids in splits.items():
        for img_id in img_ids:
            img_info = all_images[img_id]
            src_img = os.path.join(coco_dir, img_info['file_name'])
            dst_img = os.path.join(dataset_output_dir, "images", split_name, f"{img_id}.jpg")
            dst_lbl = os.path.join(dataset_output_dir, "labels", split_name, f"{img_id}.txt")
            
            shutil.copy2(src_img, dst_img)
            
            w_img, h_img = float(img_info['width']), float(img_info['height'])
            
            # Write normalized YOLO label file
            with open(dst_lbl, 'w', encoding='utf-8') as lf:
                for ann in annotations_by_image[img_id]:
                    cid = ann['class_id']
                    x, y, w, h = ann['bbox']
                    # Convert to center normalized coordinates
                    xc = (x + w / 2.0) / w_img
                    yc = (y + h / 2.0) / h_img
                    wn = w / w_img
                    hn = h / h_img
                    # Clamp to [0, 1]
                    xc = max(0.0, min(1.0, xc))
                    yc = max(0.0, min(1.0, yc))
                    wn = max(0.0, min(1.0, wn))
                    hn = max(0.0, min(1.0, hn))
                    lf.write(f"{cid} {xc:.6f} {yc:.6f} {wn:.6f} {hn:.6f}\n")
                    
    # Generate dataset YAML for YOLO
    yaml_path = os.path.join(dataset_output_dir, "civic_issues.yaml")
    with open(yaml_path, 'w', encoding='utf-8') as yf:
        yf.write(f"path: {os.path.abspath(dataset_output_dir)}\n")
        yf.write("train: images/train\n")
        yf.write("val: images/val\n")
        yf.write("test: images/test\n\n")
        yf.write("names:\n")
        for idx, name in enumerate(TARGET_CLASSES):
            yf.write(f"  {idx}: {name}\n")
            
    print(f"Dataset preparation complete! YAML config saved to: {yaml_path}")
    return True


def train_yolo(dataset_yaml, epochs=30, img_size=640, device="cpu"):
    """
    Fine-tunes YOLOv8 with pretrained weights and image augmentation.
    """
    try:
        from ultralytics import YOLO
    except ImportError:
        print("[NOTICE] Ultralytics is not installed. To train, run: pip install ultralytics")
        return None
        
    print(f"Loading pretrained YOLOv8n weights for transfer learning...")
    model = YOLO("yolov8n.pt")
    
    # Train with transfer learning & data augmentations
    results = model.train(
        data=dataset_yaml,
        epochs=epochs,
        imgsz=img_size,
        device=device,
        fliplr=0.5,        # 50% horizontal flip
        flipud=0.0,
        hsv_h=0.015,       # HSV hue shift
        hsv_s=0.7,         # HSV saturation shift
        hsv_v=0.4,         # HSV value shift
        mosaic=1.0,        # Mosaic augmentation
        degrees=10.0,      # Small rotation
        batch=16,
        name="civic_detector_run"
    )
    
    # Evaluate on test set
    metrics = model.val(split="test")
    print(f"Test mAP50: {metrics.box.map50:.4f} | mAP50-95: {metrics.box.map:.4f}")
    
    # Save final model
    output_model_path = os.path.join("trained_models", "civic_detector.pt")
    model.export(format="onnx")
    return results


if __name__ == "__main__":
    coco_root = r"C:\Users\Asus\Downloads\civic_issue_dataset-master\civic_issue_dataset-master"
    yolo_dir = r"C:\Users\Asus\Downloads\civic_issue_dataset-master\yolo_dataset"
    success = convert_coco_to_yolo(coco_root, yolo_dir)
    if success:
        train_yolo(os.path.join(yolo_dir, "civic_issues.yaml"))

