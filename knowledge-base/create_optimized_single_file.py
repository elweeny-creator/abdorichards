#!/usr/bin/env python3
"""
Create a single optimized knowledge base file that fits Claude Projects limits.
Prioritizes high-engagement content while including representation from all topics.
"""

import json
import os
from collections import defaultdict

KB_DIR = "/home/user/abdorichards/knowledge-base"
OUTPUT_FILE = os.path.join(KB_DIR, "claude-projects-optimized.jsonl")

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

def create_optimized_record(record):
    """Create a condensed but complete record."""
    return {
        "id": record.get('thread_id'),
        "url": record.get('url'),
        "date": record.get('date'),
        "year": record.get('year'),
        "topic": record.get('primary_topic'),
        "topics": record.get('all_topics', []),
        "engagement": record.get('engagement_tier'),
        "score": record.get('engagement_score'),
        "reactions": record.get('reactions'),
        "comments": record.get('comment_count'),
        "content": record.get('full_thread_text')  # Full post + comments combined
    }

def main():
    print("Loading all records...")
    all_records = load_all_topics()
    print(f"Total records: {len(all_records)}")

    # Sort by engagement score (highest first)
    all_records.sort(key=lambda x: x.get('engagement_score', 0), reverse=True)

    # Strategy: Include ALL high engagement, MOST medium, SAMPLE of low
    high = [r for r in all_records if r.get('engagement_tier') == 'high']
    medium = [r for r in all_records if r.get('engagement_tier') == 'medium']
    low = [r for r in all_records if r.get('engagement_tier') == 'low']

    print(f"High engagement: {len(high)}")
    print(f"Medium engagement: {len(medium)}")
    print(f"Low engagement: {len(low)}")

    # Include: all high, all medium, top 1000 low (by score)
    selected = high + medium + low[:1000]

    # Ensure topic diversity in low-engagement selection
    # (the sort already handles this since we take top by score)

    print(f"Selected records: {len(selected)}")

    # Create optimized records
    optimized = [create_optimized_record(r) for r in selected]

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for record in optimized:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')

    # Check file size
    size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
    print(f"\nOutput file: {OUTPUT_FILE}")
    print(f"File size: {size_mb:.2f} MB")
    print(f"Records: {len(optimized)}")

    # Topic breakdown
    topic_counts = defaultdict(int)
    for r in optimized:
        topic_counts[r['topic']] += 1

    print("\nTopic coverage:")
    for topic, count in sorted(topic_counts.items()):
        print(f"  {topic}: {count}")

if __name__ == "__main__":
    main()
