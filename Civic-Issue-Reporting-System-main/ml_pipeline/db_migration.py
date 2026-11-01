"""
Database Migration for AI Validation Columns
--------------------------------------------
Safely adds validation_status, predicted_category, ai_confidence,
review_decision, image_phash, and ai_explanation to the issues table.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import get_db

def apply_migration():
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SHOW COLUMNS FROM issues")
        existing_cols = {c[0] for c in cursor.fetchall()}
        
        new_cols = [
            ("validation_status", "VARCHAR(50) DEFAULT 'PENDING'"),
            ("predicted_category", "VARCHAR(100)"),
            ("ai_confidence", "FLOAT"),
            ("review_decision", "VARCHAR(50)"),
            ("image_phash", "VARCHAR(64)"),
            ("ai_explanation", "TEXT")
        ]
        
        for col_name, col_type in new_cols:
            if col_name not in existing_cols:
                cursor.execute(f"ALTER TABLE issues ADD COLUMN {col_name} {col_type}")
                print(f"[MIGRATION] Added column '{col_name}' ({col_type})")
            else:
                print(f"[MIGRATION] Column '{col_name}' already exists.")
                
        conn.commit()
        
        cursor.execute("SHOW COLUMNS FROM issues")
        all_cols = [c[0] for c in cursor.fetchall()]
        print("\nCurrent 'issues' columns:", all_cols)
        print("Migration applied successfully!")
        return True
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    apply_migration()

