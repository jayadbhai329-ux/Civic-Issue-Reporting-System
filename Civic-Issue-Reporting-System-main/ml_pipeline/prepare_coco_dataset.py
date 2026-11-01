"""
COCO Civic Issue Dataset Preparation & Validation
--------------------------------------------------
Loads and validates the civic issue COCO annotations from `civic_issue_dataset-master`.
Inspects categories, bounding boxes, image references, and checks for physical image availability on disk.

Civic Issue Target Classes:
- crack
- blurline
- garbage
- pothole
- manhole

Requirements:
- Validate COCO bounding boxes [x, y, w, h].
- Map image paths and category IDs.
- Convert bounding boxes to normalized YOLO format.
- Check for missing image files and invalid annotations.
- Split data into train/val/test splits without data leakage.
- If images are missing, STOP before training and explain how to obtain them. Do not fabricate images or labels.
"""

import os
import json
from collections import defaultdict, Counter


TARGET_CLASSES = [
    "crack",
    "blurline",
    "garbage",
    "pothole",
    "manhole"
]

CLASS_TO_ID = {name: idx for idx, name in enumerate(TARGET_CLASSES)}


def inspect_and_prepare_coco_dataset(coco_root_dir, output_dir=None):
    """
    Validates COCO JSON files and checks physical image availability on disk.
    """
    json_files = [
        "garbage_coco.json",
        "pothole_coco.json",
        "road_coco.json",
        "new_images_coco.json"
    ]
    
    report = {
        "files_checked": [],
        "target_classes": TARGET_CLASSES,
        "class_mapping": CLASS_TO_ID,
        "total_referenced_images": 0,
        "total_civic_annotations": 0,
        "class_annotation_counts": Counter(),
        "available_images_count": 0,
        "missing_images_count": 0,
        "missing_image_samples": [],
        "invalid_bboxes_count": 0,
        "status": "INCOMPLETE"
    }
    
    unique_images = {}
    image_annotations = defaultdict(list)
    
    print("="*65)
    print("INSPECTING COCO CIVIC ISSUE DATASET ANNOTATIONS")
    print("="*65)
    
    for jname in json_files:
        jpath = os.path.join(coco_root_dir, jname)
        if not os.path.exists(jpath):
            print(f"[WARNING] File not found: {jpath}")
            continue
            
        with open(jpath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        cats = {c['id']: c['name'] for c in data.get('categories', [])}
        images = data.get('images', [])
        annotations = data.get('annotations', [])
        
        report["files_checked"].append(jname)
        
        # Track images
        for img in images:
            img_id = img['id']
            if img_id not in unique_images:
                unique_images[img_id] = img
                
        # Track annotations for target civic classes
        civic_ann_count = 0
        for ann in annotations:
            cid = ann.get('category_id')
            cname = cats.get(cid, '')
            if cname in CLASS_TO_ID:
                bbox = ann.get('bbox', [])
                # Validate bbox [x, y, w, h]
                if len(bbox) == 4 and bbox[2] > 0 and bbox[3] > 0:
                    image_annotations[ann['image_id']].append({
                        "category_name": cname,
                        "category_id": CLASS_TO_ID[cname],
                        "bbox": bbox
                    })
                    report["class_annotation_counts"][cname] += 1
                    civic_ann_count += 1
                else:
                    report["invalid_bboxes_count"] += 1
                    
        print(f"[{jname}] Images: {len(images)} | Civic Annotations: {civic_ann_count}")
        
    report["total_referenced_images"] = len(unique_images)
    report["total_civic_annotations"] = sum(report["class_annotation_counts"].values())
    
    print("\nCivic Class Annotation Breakdown:")
    for cname, count in report["class_annotation_counts"].items():
        print(f"  - {cname} (Class ID {CLASS_TO_ID[cname]}): {count} bounding boxes")
        
    # Check physical image existence on disk
    print("\nVerifying physical image files on disk...")
    existing_images = []
    missing_images = []
    
    for img_id, img_info in unique_images.items():
        rel_path = img_info.get('file_name', '')
        # Check relative to coco_root_dir and parent directories
        candidate_paths = [
            os.path.join(coco_root_dir, rel_path),
            os.path.join(os.path.dirname(coco_root_dir), rel_path),
            os.path.join(coco_root_dir, os.path.basename(rel_path))
        ]
        
        found = False
        for p in candidate_paths:
            if os.path.exists(p):
                existing_images.append(p)
                found = True
                break
                
        if not found:
            missing_images.append(rel_path)
            
    report["available_images_count"] = len(existing_images)
    report["missing_images_count"] = len(missing_images)
    report["missing_image_samples"] = missing_images[:10]
    
    print(f"\nImage Availability Summary:")
    print(f"  Referenced in COCO JSONs: {len(unique_images)}")
    print(f"  Found on Local Disk:       {len(existing_images)}")
    print(f"  Missing from Local Disk:   {len(missing_images)}")
    
    if len(missing_images) > 0:
        print("\n[CRITICAL NOTE - IMAGE DATASET INCOMPLETE]")
        print("The COCO annotations exist, but the physical image files (e.g. garbage/, pothole/, road/) are missing on disk.")
        print(f"Sample missing files: {missing_images[:5]}")
        print("According to civic_issue_dataset-master/README.md:")
        print("  Images were hosted on: https://drive.google.com/open?id=1fvXn-SHSCu5jY4LPy79jeSdWrMhPkYPo")
        print("  (However, the Google Drive link currently returns HTTP 404 / unavailable).")
        print("Per instructions: STOPPING before model training to avoid fabricating fake images or labels.")
        report["status"] = "IMAGES_MISSING_STOPPED"
    else:
        report["status"] = "READY_FOR_TRAINING"
        print("\nAll referenced images exist on disk. Ready for training!")

    # Save validation report
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        report_path = os.path.join(output_dir, "coco_dataset_validation_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            # Convert Counter to dict for JSON serialization
            report_copy = dict(report)
            report_copy["class_annotation_counts"] = dict(report["class_annotation_counts"])
            json.dump(report_copy, f, indent=2)
        print(f"\nValidation report saved to: {report_path}")

    return report


if __name__ == "__main__":
    coco_dir = r"C:\Users\Asus\Downloads\civic_issue_dataset-master\civic_issue_dataset-master"
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trained_models")
    inspect_and_prepare_coco_dataset(coco_dir, out_dir)

