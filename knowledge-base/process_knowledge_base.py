#!/usr/bin/env python3
"""
PT Entrepreneurship Knowledge Base Processor
=============================================
Processes raw Facebook group data into an organized, AI-optimized knowledge base.

Features:
- Multi-topic classification using keyword taxonomy
- Engagement scoring and tiering
- Full provenance tracking (URLs, dates, thread IDs)
- JSONL output for AI consumption
- Markdown summaries for human readability
- Comprehensive indexes
"""

import json
import os
import re
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Any, Set, Tuple
import hashlib

# Configuration
BASE_DIR = "/home/user/abdorichards"
KB_DIR = os.path.join(BASE_DIR, "knowledge-base")
RAW_FILE = os.path.join(BASE_DIR, "dataset_facebook-post-scraper_2026-01-08_06-15-54-528 (2).json")
TAXONOMY_FILE = os.path.join(KB_DIR, "metadata", "taxonomy.json")

# Topic directory mapping
TOPIC_DIRS = {
    "01-starting-your-practice": "01-starting-your-practice",
    "02-pricing-revenue-compensation": "02-pricing-revenue-compensation",
    "03-insurance-billing-reimbursement": "03-insurance-billing-reimbursement",
    "04-marketing-client-acquisition": "04-marketing-client-acquisition",
    "05-operations-systems-tools": "05-operations-systems-tools",
    "06-staffing-hiring-team": "06-staffing-hiring-team",
    "07-clinical-practice-specialties": "07-clinical-practice-specialties",
    "08-legal-compliance-regulations": "08-legal-compliance-regulations",
    "09-finance-taxes-accounting": "09-finance-taxes-accounting",
    "10-growth-scaling-exit": "10-growth-scaling-exit",
    "11-work-life-mindset-burnout": "11-work-life-mindset-burnout",
    "12-telehealth-virtual-care": "12-telehealth-virtual-care",
    "13-mobile-home-health": "13-mobile-home-health",
    "14-continuing-education-ceus": "14-continuing-education-ceus",
    "15-networking-community": "15-networking-community",
    "16-general-qa-advice": "16-general-qa-advice"
}


def load_taxonomy() -> Dict:
    """Load the topic taxonomy from JSON file."""
    with open(TAXONOMY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_raw_data() -> List[Dict]:
    """Load raw Facebook group data."""
    print("Loading raw data...")
    with open(RAW_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Loaded {len(data)} items")
    return data


def unix_to_datetime(timestamp: int) -> datetime:
    """Convert Unix timestamp to datetime."""
    try:
        return datetime.fromtimestamp(timestamp)  # Seconds (not milliseconds)
    except (ValueError, TypeError, OSError):
        return None


def format_date(dt: datetime) -> str:
    """Format datetime for display."""
    if dt:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return "Unknown"


def get_year_quarter(dt: datetime) -> str:
    """Get year and quarter from datetime."""
    if dt:
        quarter = (dt.month - 1) // 3 + 1
        return f"{dt.year} Q{quarter}"
    return "Unknown"


def calculate_engagement_score(post: Dict) -> float:
    """
    Calculate engagement score for a post.
    Weights: reactions (1x), comments (2x), shares (3x)
    """
    reactions = post.get('reactionCount', 0) or 0
    comments = post.get('commentCount', 0) or 0
    shares = post.get('shareCount', 0) or 0
    return reactions + (comments * 2) + (shares * 3)


def get_engagement_tier(score: float, reactions: int, comments: int) -> str:
    """Determine engagement tier based on score and counts."""
    if reactions >= 10 or comments >= 15:
        return "high"
    elif reactions >= 5 or comments >= 5:
        return "medium"
    return "low"


def extract_thread_id(url: str) -> str:
    """Extract thread/post ID from Facebook URL."""
    if not url:
        return None
    # Pattern: /permalink/XXXXX or /posts/XXXXX
    match = re.search(r'/(?:permalink|posts)/(\d+)', url)
    if match:
        return match.group(1)
    return None


def generate_content_hash(text: str) -> str:
    """Generate a short hash for content deduplication."""
    if not text:
        return None
    return hashlib.md5(text.encode('utf-8')).hexdigest()[:12]


def classify_post(text: str, taxonomy: Dict) -> List[Tuple[str, int]]:
    """
    Classify a post into topics based on keyword matching.
    Returns list of (topic_id, match_count) sorted by relevance.
    """
    if not text:
        return [("16-general-qa-advice", 0)]

    text_lower = text.lower()
    topic_scores = {}

    for topic_id, topic_data in taxonomy['categories'].items():
        keywords = topic_data.get('keywords', [])
        exclude_keywords = topic_data.get('exclude_keywords', [])

        # Count keyword matches
        match_count = 0
        for keyword in keywords:
            # Use word boundary matching for better accuracy
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            matches = len(re.findall(pattern, text_lower))
            match_count += matches

        # Subtract for exclude keywords
        for exclude in exclude_keywords:
            pattern = r'\b' + re.escape(exclude.lower()) + r'\b'
            if re.search(pattern, text_lower):
                match_count = max(0, match_count - 5)  # Penalty for excluded terms

        if match_count > 0:
            topic_scores[topic_id] = match_count

    # Sort by match count descending
    sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1], reverse=True)

    # If no matches, classify as general Q&A
    if not sorted_topics:
        return [("16-general-qa-advice", 0)]

    return sorted_topics


def process_post(post: Dict, taxonomy: Dict) -> Dict:
    """
    Process a single post into enriched knowledge base format.
    """
    # Skip error items
    if 'error' in post:
        return None

    # Extract basic info
    text = post.get('text', '')
    url = post.get('url', '')
    created_at = post.get('createdAt')
    user = post.get('user', {})

    # Parse datetime
    dt = unix_to_datetime(created_at)

    # Calculate engagement
    reactions = post.get('reactionCount', 0) or 0
    comments = post.get('commentCount', 0) or 0
    shares = post.get('shareCount', 0) or 0
    engagement_score = calculate_engagement_score(post)
    engagement_tier = get_engagement_tier(engagement_score, reactions, comments)

    # Classify into topics
    all_text = text
    top_comments = post.get('topComments', [])
    for comment in top_comments:
        comment_text = comment.get('text', '')
        if comment_text:
            all_text += " " + comment_text

    topic_classifications = classify_post(all_text, taxonomy)
    primary_topic = topic_classifications[0][0] if topic_classifications else "16-general-qa-advice"

    # Process comments
    processed_comments = []
    for comment in top_comments:
        comment_dt = unix_to_datetime(comment.get('createdAt'))
        author = comment.get('author', {})
        processed_comments.append({
            "text": comment.get('text', ''),
            "date": format_date(comment_dt),
            "author_id": author.get('id', ''),
            "comment_url": comment.get('url', '')
        })

    # Build enriched record
    enriched = {
        # Provenance
        "thread_id": extract_thread_id(url),
        "url": url,
        "content_hash": generate_content_hash(text),

        # Temporal
        "date": format_date(dt),
        "year": dt.year if dt else None,
        "quarter": get_year_quarter(dt),
        "timestamp": created_at,

        # Content
        "post_text": text,
        "comments": processed_comments,
        "comment_count": comments,
        "has_attachments": bool(post.get('attachments')),

        # Classification
        "primary_topic": primary_topic,
        "all_topics": [t[0] for t in topic_classifications[:3]],  # Top 3 topics
        "topic_scores": {t[0]: t[1] for t in topic_classifications[:5]},

        # Engagement
        "reactions": reactions,
        "shares": shares,
        "engagement_score": engagement_score,
        "engagement_tier": engagement_tier,

        # Author (anonymized)
        "author_id": user.get('id', ''),

        # Full thread text for AI context
        "full_thread_text": create_thread_text(text, processed_comments)
    }

    return enriched


def create_thread_text(post_text: str, comments: List[Dict]) -> str:
    """Create a readable full thread text for AI consumption."""
    parts = [f"POST: {post_text}"]

    for i, comment in enumerate(comments, 1):
        if comment.get('text'):
            parts.append(f"COMMENT {i}: {comment['text']}")

    return "\n\n".join(parts)


def write_jsonl(records: List[Dict], filepath: str):
    """Write records to JSONL file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + '\n')


def generate_topic_summary(topic_id: str, records: List[Dict], taxonomy: Dict) -> str:
    """Generate a markdown summary for a topic."""
    topic_info = taxonomy['categories'].get(topic_id, {})
    topic_name = topic_info.get('name', topic_id)
    topic_desc = topic_info.get('description', '')

    # Statistics
    total_posts = len(records)
    high_engagement = sum(1 for r in records if r['engagement_tier'] == 'high')
    medium_engagement = sum(1 for r in records if r['engagement_tier'] == 'medium')
    total_comments = sum(r['comment_count'] for r in records)

    # Date range
    dates = [r['year'] for r in records if r['year']]
    date_range = f"{min(dates)}-{max(dates)}" if dates else "Unknown"

    # Top posts by engagement
    top_posts = sorted(records, key=lambda x: x['engagement_score'], reverse=True)[:10]

    # Build markdown
    md = f"""# {topic_name}

## Overview
{topic_desc}

## Statistics
- **Total Posts:** {total_posts:,}
- **Total Comments:** {total_comments:,}
- **Date Range:** {date_range}
- **High Engagement Posts:** {high_engagement:,}
- **Medium Engagement Posts:** {medium_engagement:,}

## Top 10 Most Engaged Posts

"""

    for i, post in enumerate(top_posts, 1):
        preview = post['post_text'][:200] + "..." if len(post['post_text']) > 200 else post['post_text']
        preview = preview.replace('\n', ' ')
        md += f"""### {i}. [{post['date']}] (Engagement: {post['engagement_score']:.0f})
> {preview}

- **Reactions:** {post['reactions']} | **Comments:** {post['comment_count']}
- **URL:** {post['url']}
- **Thread ID:** {post['thread_id']}

"""

    # Year breakdown
    year_counts = defaultdict(int)
    for r in records:
        if r['year']:
            year_counts[r['year']] += 1

    md += """## Posts by Year

| Year | Count |
|------|-------|
"""
    for year in sorted(year_counts.keys()):
        md += f"| {year} | {year_counts[year]:,} |\n"

    md += f"""

---
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Source: Uncaged Clinician Facebook Group*
"""

    return md


def create_master_index(all_records: List[Dict], taxonomy: Dict) -> Dict:
    """Create master index with statistics."""
    index = {
        "generated": datetime.now().isoformat(),
        "total_posts": len(all_records),
        "total_comments": sum(r['comment_count'] for r in all_records),
        "date_range": {
            "start": min(r['date'] for r in all_records if r['date']),
            "end": max(r['date'] for r in all_records if r['date'])
        },
        "topics": {},
        "engagement_summary": {
            "high": sum(1 for r in all_records if r['engagement_tier'] == 'high'),
            "medium": sum(1 for r in all_records if r['engagement_tier'] == 'medium'),
            "low": sum(1 for r in all_records if r['engagement_tier'] == 'low')
        },
        "yearly_breakdown": defaultdict(int)
    }

    # Topic breakdown
    topic_counts = defaultdict(int)
    for r in all_records:
        topic_counts[r['primary_topic']] += 1
        if r['year']:
            index['yearly_breakdown'][r['year']] += 1

    for topic_id, count in sorted(topic_counts.items()):
        topic_name = taxonomy['categories'].get(topic_id, {}).get('name', topic_id)
        index['topics'][topic_id] = {
            "name": topic_name,
            "count": count,
            "percentage": round(count / len(all_records) * 100, 2)
        }

    index['yearly_breakdown'] = dict(index['yearly_breakdown'])

    return index


def create_high_engagement_index(all_records: List[Dict]) -> List[Dict]:
    """Create index of high-engagement posts."""
    high_engagement = [r for r in all_records if r['engagement_tier'] == 'high']
    high_engagement.sort(key=lambda x: x['engagement_score'], reverse=True)

    # Create condensed index entries
    index_entries = []
    for r in high_engagement:
        index_entries.append({
            "thread_id": r['thread_id'],
            "url": r['url'],
            "date": r['date'],
            "primary_topic": r['primary_topic'],
            "engagement_score": r['engagement_score'],
            "reactions": r['reactions'],
            "comments": r['comment_count'],
            "preview": r['post_text'][:150] + "..." if len(r['post_text']) > 150 else r['post_text']
        })

    return index_entries


def main():
    """Main processing pipeline."""
    print("=" * 60)
    print("PT ENTREPRENEURSHIP KNOWLEDGE BASE PROCESSOR")
    print("=" * 60)

    # Load taxonomy
    print("\n[1/7] Loading taxonomy...")
    taxonomy = load_taxonomy()
    print(f"  Loaded {len(taxonomy['categories'])} topic categories")

    # Load raw data
    print("\n[2/7] Loading raw data...")
    raw_data = load_raw_data()

    # Process all posts
    print("\n[3/7] Processing and classifying posts...")
    all_records = []
    error_count = 0

    for i, post in enumerate(raw_data):
        if i % 1000 == 0:
            print(f"  Processing post {i}/{len(raw_data)}...")

        processed = process_post(post, taxonomy)
        if processed:
            all_records.append(processed)
        else:
            error_count += 1

    print(f"  Processed {len(all_records)} posts ({error_count} errors skipped)")

    # Organize by topic
    print("\n[4/7] Organizing posts by topic...")
    topic_records = defaultdict(list)
    for record in all_records:
        topic_records[record['primary_topic']].append(record)

    # Write topic files
    print("\n[5/7] Writing topic files...")
    for topic_id, records in topic_records.items():
        topic_dir = os.path.join(KB_DIR, "topics", TOPIC_DIRS.get(topic_id, topic_id))
        os.makedirs(topic_dir, exist_ok=True)

        # Write JSONL
        jsonl_path = os.path.join(topic_dir, f"{topic_id}.jsonl")
        write_jsonl(records, jsonl_path)

        # Write summary
        summary_path = os.path.join(topic_dir, f"{topic_id}-summary.md")
        summary = generate_topic_summary(topic_id, records, taxonomy)
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)

        print(f"  {topic_id}: {len(records)} posts")

    # Create indexes
    print("\n[6/7] Creating indexes...")

    # Master index
    master_index = create_master_index(all_records, taxonomy)
    with open(os.path.join(KB_DIR, "indexes", "master-index.json"), 'w', encoding='utf-8') as f:
        json.dump(master_index, f, indent=2, ensure_ascii=False)

    # High engagement index
    high_engagement_index = create_high_engagement_index(all_records)
    write_jsonl(high_engagement_index, os.path.join(KB_DIR, "indexes", "high-engagement-index.jsonl"))

    # Full searchable index (all posts, condensed)
    print("  Creating full searchable index...")
    searchable_index = []
    for r in all_records:
        searchable_index.append({
            "thread_id": r['thread_id'],
            "url": r['url'],
            "date": r['date'],
            "year": r['year'],
            "quarter": r['quarter'],
            "primary_topic": r['primary_topic'],
            "all_topics": r['all_topics'],
            "engagement_score": r['engagement_score'],
            "engagement_tier": r['engagement_tier'],
            "reactions": r['reactions'],
            "comments": r['comment_count'],
            "post_preview": r['post_text'][:300] if r['post_text'] else ""
        })
    write_jsonl(searchable_index, os.path.join(KB_DIR, "indexes", "searchable-index.jsonl"))

    # Copy raw data
    print("\n[7/7] Preserving raw data...")
    import shutil
    raw_dest = os.path.join(KB_DIR, "raw", "original-data.json")
    shutil.copy(RAW_FILE, raw_dest)

    # Final statistics
    print("\n" + "=" * 60)
    print("PROCESSING COMPLETE")
    print("=" * 60)
    print(f"\nTotal posts processed: {len(all_records):,}")
    print(f"Total comments: {sum(r['comment_count'] for r in all_records):,}")
    print(f"Topics created: {len(topic_records)}")
    print(f"\nEngagement breakdown:")
    print(f"  High:   {master_index['engagement_summary']['high']:,}")
    print(f"  Medium: {master_index['engagement_summary']['medium']:,}")
    print(f"  Low:    {master_index['engagement_summary']['low']:,}")
    print(f"\nTop topics by post count:")
    sorted_topics = sorted(master_index['topics'].items(), key=lambda x: x[1]['count'], reverse=True)
    for topic_id, info in sorted_topics[:5]:
        print(f"  {info['name']}: {info['count']:,} ({info['percentage']}%)")

    print(f"\nOutput location: {KB_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
