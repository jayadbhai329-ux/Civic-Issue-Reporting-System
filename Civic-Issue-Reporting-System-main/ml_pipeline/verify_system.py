"""
End-to-End Verification Test Suite
Tests text classifier, computer vision defect localization, perceptual hashing,
blur evaluation, AI generation detection, decision policy, and Flask API integration.
"""

import os
import sys
import tempfile
import unittest
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

# Add app directory to path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, base_dir)

from ai_detector import (
    classify_complaint_text,
    compute_dhash,
    hamming_distance,
    compute_blur_metrics,
    check_ai_generated_image,
    analyze_image_defects,
    validate_civic_complaint
)
from app import app, get_db

class TestCivicAIEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create temp fixtures
        cls.tmp_dir = tempfile.mkdtemp()

        # 1. Authentic Pothole fixture (textured asphalt with localized jagged crater)
        np.random.seed(42)
        base = np.random.randint(70, 95, (300, 300, 3), dtype=np.uint8)
        pothole_img = Image.fromarray(base)
        draw = ImageDraw.Draw(pothole_img)
        # Draw dark jagged cavity
        draw.polygon([(100, 100), (190, 85), (220, 180), (160, 230), (80, 190)], fill=(20, 20, 22))
        # Draw high contrast fractured rim
        draw.polygon([(95, 95), (195, 80), (225, 185), (165, 235), (75, 195)], outline=(210, 210, 215), width=3)
        cls.pothole_path = os.path.join(cls.tmp_dir, "pothole_test.jpg")
        pothole_img.save(cls.pothole_path, quality=95)

        # 2. Blurry Pothole fixture
        blurry_img = pothole_img.filter(ImageFilter.GaussianBlur(radius=8.0))
        cls.blurry_path = os.path.join(cls.tmp_dir, "blurry_test.jpg")
        blurry_img.save(cls.blurry_path, quality=95)

        # 3. Clean Road fixture (smooth asphalt with no crater)
        clean_base = np.random.randint(90, 105, (300, 300, 3), dtype=np.uint8)
        clean_img = Image.fromarray(clean_base).filter(ImageFilter.GaussianBlur(radius=1.0))
        cls.clean_path = os.path.join(cls.tmp_dir, "clean_road.jpg")
        clean_img.save(cls.clean_path, quality=95)

        # 4. AI-Generated image simulation
        ai_img = Image.new("RGB", (1024, 1024), color=(120, 130, 140))
        ai_draw = ImageDraw.Draw(ai_img)
        ai_draw.rectangle([200, 200, 800, 800], fill=(130, 140, 150))
        cls.ai_path = os.path.join(cls.tmp_dir, "synthetic_ai.png")
        ai_img.save(cls.ai_path)

    def test_01_text_classifier(self):
        print("\n--- Test 1: Text Classifier ---")
        res = classify_complaint_text("Deep pothole in the middle of the road causing tire damage to vehicles")
        self.assertTrue(res["is_available"])
        self.assertIn("Pothole", res["predicted_issue_type"])
        self.assertEqual(res["predicted_app_category"], "Road & Potholes")
        self.assertGreater(res["confidence"], 50.0)
        print(f"Text prediction: {res['predicted_issue_type']} -> {res['predicted_app_category']} (Conf: {res['confidence']}%)")

    def test_02_perceptual_hash_and_duplicates(self):
        print("\n--- Test 2: Perceptual Hashing & Duplicate Detection ---")
        im = Image.open(self.pothole_path)
        h1 = compute_dhash(im)
        self.assertEqual(len(h1), 16)

        # Exact duplicate
        h2 = compute_dhash(im)
        self.assertEqual(hamming_distance(h1, h2), 0)

        # Duplicate detection within validation
        res = validate_civic_complaint(
            self.pothole_path,
            description="Hazardous pothole on 5th avenue",
            user_category="Road & Potholes",
            existing_hashes=[h1]
        )
        self.assertTrue(res["is_duplicate"])
        self.assertEqual(res["decision"], "MANUAL_REVIEW")
        print(f"Duplicate image correctly flagged as MANUAL_REVIEW: {res['explanation']}")

    def test_03_blur_detection(self):
        print("\n--- Test 3: Blur Quality Detection ---")
        res = validate_civic_complaint(
            self.blurry_path,
            description="Deep pothole on the avenue",
            user_category="Road & Potholes"
        )
        self.assertTrue(res["is_blurry"])
        self.assertEqual(res["decision"], "MANUAL_REVIEW")
        print(f"Blurry image correctly flagged as MANUAL_REVIEW: Sharpness score={res['blur_score']}")

    def test_04_defect_detection_and_bounding_boxes(self):
        print("\n--- Test 4: Defect Localization & Bounding Boxes ---")
        res = validate_civic_complaint(
            self.pothole_path,
            description="Deep pothole in the asphalt near central square",
            user_category="Road & Potholes"
        )
        self.assertEqual(res["decision"], "ACCEPT")
        self.assertGreater(len(res["boxes"]), 0)
        box = res["boxes"][0]
        self.assertEqual(box["class"], "pothole")
        self.assertEqual(len(box["box_norm"]), 4)
        print(f"Bounding box generated: {box['box']} -> normalized: {box['box_norm']}")

    def test_05_clean_infrastructure_rejection(self):
        print("\n--- Test 5: Clean Infrastructure Rejection ---")
        res = validate_civic_complaint(
            self.clean_path,
            description="Pothole complaint on good road",
            user_category="Road & Potholes"
        )
        self.assertEqual(res["decision"], "REJECT")
        print(f"Clean road correctly rejected: {res['explanation']}")

    def test_06_text_image_mismatch(self):
        print("\n--- Test 6: Text-Image Cross-Modal Mismatch ---")
        res = validate_civic_complaint(
            self.pothole_path,
            description="Loud street noise and music late at night",
            user_category="Noise Complaints"
        )
        self.assertTrue(res["is_mismatch"])
        self.assertEqual(res["decision"], "MANUAL_REVIEW")
        print(f"Mismatch correctly flagged: {res['explanation']}")

    def test_07_api_endpoint(self):
        print("\n--- Test 7: Flask /api/ai-detect-image Endpoint ---")
        client = app.test_client()
        with open(self.pothole_path, "rb") as f:
            response = client.post(
                "/api/ai-detect-image",
                data={
                    "image": f,
                    "description": "Large pothole in the asphalt",
                    "category": "Road & Potholes"
                },
                content_type="multipart/form-data"
            )
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertTrue(json_data["success"])
        self.assertIn(json_data["decision"], ["ACCEPT", "MANUAL_REVIEW", "REJECT"])
        self.assertIn("boxes", json_data)
        print(f"API Response Decision: {json_data['decision']}, Boxes count: {len(json_data['boxes'])}")

if __name__ == "__main__":
    unittest.main()
