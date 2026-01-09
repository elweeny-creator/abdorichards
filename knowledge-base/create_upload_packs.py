#!/usr/bin/env python3
"""
Create optimized upload packs for Claude Projects and ChatGPT.
Consolidates topics into manageable chunks with full context.
"""

import json
import os
from datetime import datetime
from collections import defaultdict

KB_DIR = "/home/user/abdorichards/knowledge-base"
UPLOAD_DIR = os.path.join(KB_DIR, "upload-packs")

# Topic groupings for logical upload packs
UPLOAD_PACKS = {
    "business-foundations": {
        "description": "Starting, pricing, and growing your PT practice",
        "topics": [
            "01-starting-your-practice",
            "02-pricing-revenue-compensation",
            "10-growth-scaling-exit"
        ]
    },
    "billing-insurance-finance": {
        "description": "Insurance, billing, reimbursement, taxes, and financial management",
        "topics": [
            "03-insurance-billing-reimbursement",
            "09-finance-taxes-accounting"
        ]
    },
    "marketing-acquisition": {
        "description": "Marketing strategies and client acquisition",
        "topics": [
            "04-marketing-client-acquisition",
            "15-networking-community"
        ]
    },
    "operations-staffing": {
        "description": "Day-to-day operations, systems, and team management",
        "topics": [
            "05-operations-systems-tools",
            "06-staffing-hiring-team"
        ]
    },
    "clinical-specialties": {
        "description": "Clinical practice, specialties, and continuing education",
        "topics": [
            "07-clinical-practice-specialties",
            "14-continuing-education-ceus"
        ]
    },
    "legal-compliance": {
        "description": "Legal, compliance, regulations, and risk management",
        "topics": [
            "08-legal-compliance-regulations"
        ]
    },
    "service-models": {
        "description": "Telehealth, mobile PT, and home health services",
        "topics": [
            "12-telehealth-virtual-care",
            "13-mobile-home-health"
        ]
    },
    "mindset-community": {
        "description": "Work-life balance, burnout prevention, and general advice",
        "topics": [
            "11-work-life-mindset-burnout",
            "16-general-qa-advice"
        ]
    }
}


def load_topic_data(topic_id: str) -> list:
    """Load JSONL data for a topic."""
    topic_dir = os.path.join(KB_DIR, "topics", topic_id)
    jsonl_file = os.path.join(topic_dir, f"{topic_id}.jsonl")

    records = []
    if os.path.exists(jsonl_file):
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    records.append(json.loads(line))
    return records


def create_consolidated_markdown(pack_name: str, pack_info: dict, all_records: list) -> str:
    """Create a consolidated markdown file for AI consumption."""

    # Sort by engagement
    sorted_records = sorted(all_records, key=lambda x: x.get('engagement_score', 0), reverse=True)

    md = f"""# PT Entrepreneurship: {pack_info['description']}

## Overview
This document contains {len(all_records):,} community discussions from the Uncaged Clinician group.

**Topics Covered:**
"""

    # Add topic breakdown
    topic_counts = defaultdict(int)
    for r in all_records:
        topic_counts[r['primary_topic']] += 1

    for topic_id, count in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True):
        md += f"- {topic_id}: {count:,} posts\n"

    md += f"""
**Engagement Summary:**
- High engagement: {sum(1 for r in all_records if r.get('engagement_tier') == 'high'):,}
- Medium engagement: {sum(1 for r in all_records if r.get('engagement_tier') == 'medium'):,}

---

## High-Value Discussions

Below are the community discussions, organized by engagement level. Each entry includes the original post, community responses, and metadata for context.

"""

    # Add all posts with full context
    for i, record in enumerate(sorted_records, 1):
        engagement_badge = ""
        if record.get('engagement_tier') == 'high':
            engagement_badge = "[HIGH ENGAGEMENT] "
        elif record.get('engagement_tier') == 'medium':
            engagement_badge = "[MEDIUM ENGAGEMENT] "

        md += f"""### Discussion {i}: {engagement_badge}

**Date:** {record.get('date', 'Unknown')} | **Topic:** {record.get('primary_topic', 'General')}
**Engagement:** {record.get('reactions', 0)} reactions, {record.get('comment_count', 0)} comments
**Source:** {record.get('url', 'N/A')}

**Original Post:**
{record.get('post_text', '')}

"""

        # Add comments
        comments = record.get('comments', [])
        if comments:
            md += "**Community Responses:**\n\n"
            for j, comment in enumerate(comments, 1):
                comment_text = comment.get('text', '')
                if comment_text:
                    md += f"> **Response {j}:** {comment_text}\n\n"

        md += "---\n\n"

    md += f"""
*Generated: {datetime.now().strftime('%Y-%m-%d')}*
*Source: Uncaged Clinician Facebook Group*
"""

    return md


def create_jsonl_pack(all_records: list) -> str:
    """Create JSONL output for a pack."""
    lines = []
    for record in all_records:
        lines.append(json.dumps(record, ensure_ascii=False))
    return '\n'.join(lines)


def main():
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    print("Creating Upload Packs for Claude Projects")
    print("=" * 50)

    pack_summary = []

    for pack_name, pack_info in UPLOAD_PACKS.items():
        print(f"\nProcessing: {pack_name}")

        # Collect all records for this pack
        all_records = []
        for topic_id in pack_info['topics']:
            records = load_topic_data(topic_id)
            all_records.extend(records)
            print(f"  - {topic_id}: {len(records)} posts")

        print(f"  Total: {len(all_records)} posts")

        # Create pack directory
        pack_dir = os.path.join(UPLOAD_DIR, pack_name)
        os.makedirs(pack_dir, exist_ok=True)

        # Write JSONL file
        jsonl_content = create_jsonl_pack(all_records)
        jsonl_path = os.path.join(pack_dir, f"{pack_name}.jsonl")
        with open(jsonl_path, 'w', encoding='utf-8') as f:
            f.write(jsonl_content)

        # Write Markdown file (for those who prefer it)
        md_content = create_consolidated_markdown(pack_name, pack_info, all_records)
        md_path = os.path.join(pack_dir, f"{pack_name}.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        # Get file sizes
        jsonl_size = os.path.getsize(jsonl_path) / (1024 * 1024)  # MB
        md_size = os.path.getsize(md_path) / (1024 * 1024)  # MB

        pack_summary.append({
            "name": pack_name,
            "description": pack_info['description'],
            "posts": len(all_records),
            "jsonl_size_mb": round(jsonl_size, 2),
            "md_size_mb": round(md_size, 2),
            "topics": pack_info['topics']
        })

        print(f"  Output: {jsonl_size:.2f} MB (JSONL), {md_size:.2f} MB (MD)")

    # Create high-engagement-only pack
    print("\nCreating High-Engagement Pack...")
    high_engagement_records = []
    for pack_info in UPLOAD_PACKS.values():
        for topic_id in pack_info['topics']:
            records = load_topic_data(topic_id)
            high_records = [r for r in records if r.get('engagement_tier') == 'high']
            high_engagement_records.extend(high_records)

    high_dir = os.path.join(UPLOAD_DIR, "high-engagement-all-topics")
    os.makedirs(high_dir, exist_ok=True)

    # Write high engagement files
    jsonl_content = create_jsonl_pack(high_engagement_records)
    with open(os.path.join(high_dir, "high-engagement-all-topics.jsonl"), 'w', encoding='utf-8') as f:
        f.write(jsonl_content)

    md_content = create_consolidated_markdown(
        "high-engagement-all-topics",
        {"description": "High-engagement discussions across all PT entrepreneurship topics"},
        high_engagement_records
    )
    with open(os.path.join(high_dir, "high-engagement-all-topics.md"), 'w', encoding='utf-8') as f:
        f.write(md_content)

    high_jsonl_size = os.path.getsize(os.path.join(high_dir, "high-engagement-all-topics.jsonl")) / (1024 * 1024)
    high_md_size = os.path.getsize(os.path.join(high_dir, "high-engagement-all-topics.md")) / (1024 * 1024)

    pack_summary.append({
        "name": "high-engagement-all-topics",
        "description": "High-engagement discussions across all topics",
        "posts": len(high_engagement_records),
        "jsonl_size_mb": round(high_jsonl_size, 2),
        "md_size_mb": round(high_md_size, 2),
        "topics": ["all"]
    })

    print(f"  High Engagement Pack: {len(high_engagement_records)} posts, {high_jsonl_size:.2f} MB")

    # Write pack summary
    summary_path = os.path.join(UPLOAD_DIR, "pack-summary.json")
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            "generated": datetime.now().isoformat(),
            "total_packs": len(pack_summary),
            "packs": pack_summary
        }, f, indent=2)

    # Create upload guide
    guide_content = f"""# Upload Pack Guide for Claude Projects

## Quick Start

For the best experience, upload files based on your needs:

### Option 1: Comprehensive Coverage (Recommended)
Upload the **high-engagement-all-topics** pack for the best insights across all topics.
- File: `high-engagement-all-topics/high-engagement-all-topics.jsonl`
- Size: {high_jsonl_size:.2f} MB
- Posts: {len(high_engagement_records):,} high-quality discussions

### Option 2: Topic-Specific Deep Dives
Upload individual packs based on your focus area:

| Pack | Description | Posts | Size (MB) |
|------|-------------|-------|-----------|
"""

    for pack in pack_summary:
        if pack['name'] != 'high-engagement-all-topics':
            guide_content += f"| {pack['name']} | {pack['description']} | {pack['posts']:,} | {pack['jsonl_size_mb']} |\n"

    guide_content += f"""

## Recommended Combinations

### Starting a Practice
- `business-foundations.jsonl`
- `legal-compliance.jsonl`

### Growing Your Practice
- `marketing-acquisition.jsonl`
- `operations-staffing.jsonl`

### Financial Decisions
- `billing-insurance-finance.jsonl`
- `business-foundations.jsonl`

### Clinical Development
- `clinical-specialties.jsonl`
- `service-models.jsonl`

## File Format Notes

**JSONL files** are optimized for AI consumption:
- One JSON object per line
- Full thread context included
- Engagement scores for credibility weighting

**Markdown files** are human-readable alternatives:
- Can be used if you prefer reading the content
- Same information, different format

## Sample Prompts After Upload

1. "What pricing strategies do successful cash-pay PTs use?"
2. "How do practitioners recommend handling insurance billing?"
3. "What are the common mistakes when starting a PT practice?"
4. "Compare telehealth vs in-person practice models"
5. "What marketing strategies work best for new practices?"

---

*Generated: {datetime.now().strftime('%Y-%m-%d')}*
"""

    with open(os.path.join(UPLOAD_DIR, "UPLOAD-GUIDE.md"), 'w', encoding='utf-8') as f:
        f.write(guide_content)

    print("\n" + "=" * 50)
    print("Upload Packs Created Successfully!")
    print(f"Location: {UPLOAD_DIR}")
    print("=" * 50)


if __name__ == "__main__":
    main()
