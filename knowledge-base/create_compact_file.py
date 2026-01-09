#!/usr/bin/env python3
"""
Create a compact knowledge base file guaranteed to fit Claude Projects.
Target: Under 4 MB while maximizing value.
"""

import json
import os
from collections import defaultdict

KB_DIR = "/home/user/abdorichards/knowledge-base"
OUTPUT_FILE = os.path.join(KB_DIR, "claude-projects-compact.jsonl")

def load_all_topics():
    """Load all topic JSONL files."""
    topics_dir = os.path.join(KB_DIR, "topics")
    all_records = []

    for topic_folder in os.listdir(topics_dir):
        topic_path = os.path.join(topics_dir, topic_folder)
        if os.path.isdir(topic_path):
            for filename in os.listdir(topic_path):
                if filename.endswith('.jsonl'):
                    filepath = os.path.join(topic_path, filename)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        for line in f:
                            if line.strip():
                                record = json.loads(line)
                                all_records.append(record)
    return all_records

def truncate_text(text, max_chars=1500):
    """Truncate text to max characters, keeping complete sentences."""
    if not text or len(text) <= max_chars:
        return text
    truncated = text[:max_chars]
    # Try to end at a sentence
    last_period = truncated.rfind('.')
    last_question = truncated.rfind('?')
    last_end = max(last_period, last_question)
    if last_end > max_chars * 0.7:
        return truncated[:last_end + 1]
    return truncated + "..."

def create_compact_record(record):
    """Create a compact but useful record."""
    return {
        "id": record.get('thread_id'),
        "url": record.get('url'),
        "date": record.get('date', '')[:10],  # Just date, no time
        "year": record.get('year'),
        "topic": record.get('primary_topic', '').replace('-', ' ').split(' ', 1)[-1][:30],  # Shortened topic
        "engagement": record.get('engagement_tier', '')[0] if record.get('engagement_tier') else 'l',  # h/m/l
        "content": truncate_text(record.get('full_thread_text', ''))
    }

def main():
    print("Loading all records...")
    all_records = load_all_topics()
    print(f"Total records: {len(all_records)}")

    # Sort by engagement score
    all_records.sort(key=lambda x: x.get('engagement_score', 0), reverse=True)

    # Take top 4000 records (all high + medium + some low)
    high = [r for r in all_records if r.get('engagement_tier') == 'high']
    medium = [r for r in all_records if r.get('engagement_tier') == 'medium']
    low = [r for r in all_records if r.get('engagement_tier') == 'low']

    # All high (2109), all medium (3037) = 5146, then top low to reach ~4500
    needed_low = max(0, 4500 - len(high) - len(medium))
    selected = high + medium + low[:needed_low]

    print(f"High: {len(high)}, Medium: {len(medium)}, Low: {min(needed_low, len(low))}")
    print(f"Selected: {len(selected)}")

    # Create compact records
    compact = [create_compact_record(r) for r in selected]

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for record in compact:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"\nOutput: {OUTPUT_FILE}")
    print(f"Size: {size_mb:.2f} MB")
    print(f"Records: {len(compact)}")

    # If still too big, create even smaller version
    if size_mb > 4.5:
        print("\nCreating smaller version...")
        smaller_file = os.path.join(KB_DIR, "claude-projects-small.jsonl")
        # Just high + half of medium
        selected_small = high + medium[:1500]
        compact_small = [create_compact_record(r) for r in selected_small]
        with open(smaller_file, 'w', encoding='utf-8') as f:
            for record in compact_small:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        size_small = os.path.getsize(smaller_file) / (1024 * 1024)
        print(f"Smaller file: {smaller_file}")
        print(f"Size: {size_small:.2f} MB")
        print(f"Records: {len(compact_small)}")

if __name__ == "__main__":
    main()
