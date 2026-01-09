# Data Provenance & Source Documentation

## Source Information

| Field | Value |
|-------|-------|
| **Source Platform** | Facebook |
| **Group Name** | Uncaged Clinician |
| **Group ID** | 113576786080229 |
| **Group URL** | https://www.facebook.com/groups/uncagedcliniciangroup |
| **Extraction Date** | 2026-01-08 |
| **Extraction Tool** | Facebook Post Scraper (Apify) |

## Dataset Characteristics

| Metric | Value |
|--------|-------|
| **Total Posts** | 9,567 |
| **Total Comments Captured** | 74,894 |
| **Top Comments per Post** | 2-3 (not full threads) |
| **Unique Post Authors** | ~2,067 |
| **Unique Comment Authors** | ~2,437 |
| **Date Range** | May 11, 2022 - January 7, 2026 |
| **Time Span** | 3.7 years |

## Data Quality

### Completeness
- **Valid Posts**: 9,567 (99.98%)
- **Error Items**: 2 (authorization failures, excluded)
- **Posts with Text**: 100%
- **Posts with Comments**: 79.3%
- **Posts with Attachments**: 15.6% (content not extracted)

### Comment Capture
The dataset includes "top comments" (2-3 highest-engagement comments per post), not complete comment threads. This means:
- Full discussion context may be incomplete for posts with many comments
- Comment responses/replies to other comments are not captured
- Total comment count is provided even when full threads aren't available

### Limitations
1. **Attachment Content**: Images, files, and links in attachments are referenced but not extracted
2. **Full Comment Threads**: Only top comments captured, not entire discussions
3. **Share Data**: Share counts are recorded as 0 (not captured by scraper)
4. **Reaction Types**: Only total reaction count, not breakdown by type (like, love, etc.)
5. **Edits**: Post edit history not captured

## Processing Pipeline

### Step 1: Raw Data Ingestion
- Original JSON file preserved in `/raw/original-data.json`
- No data loss from source

### Step 2: Topic Classification
- Keyword-based classification using comprehensive taxonomy
- 16 topic categories covering PT entrepreneurship
- Posts assigned primary topic + up to 2 secondary topics
- Classification based on post text AND top comment text

### Step 3: Enrichment
- Engagement scores calculated: `reactions + (comments × 2) + (shares × 3)`
- Engagement tiers assigned: high, medium, low
- Temporal metadata: year, quarter, formatted dates
- Content hashes for deduplication tracking
- Thread IDs extracted from URLs

### Step 4: Output Generation
- JSONL files per topic for AI consumption
- Markdown summaries for human reference
- Consolidated upload packs for Claude Projects
- Searchable indexes

## Citation Guidelines

When citing insights from this knowledge base:

### For Academic/Formal Use
```
Uncaged Clinician Community Discussion, [Topic], [Date],
Thread ID: [thread_id], Retrieved via Facebook Post Scraper
```

### For Casual Reference
```
"According to discussions in the Uncaged Clinician group (2024)..."
```

### Key Fields for Provenance
Each record includes:
- `thread_id`: Unique post identifier
- `url`: Direct link to original Facebook post
- `date`: Timestamp of original post
- `engagement_score`: Community validation metric
- `engagement_tier`: high/medium/low classification

## Ethical Considerations

1. **Privacy**: Author names are not included in processed data; only anonymized IDs
2. **Context**: Content is from a professional community discussing business practices
3. **Recency**: Information may become outdated; always check dates
4. **Validation**: High-engagement posts have more community validation but may not be definitive

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-09 | Initial knowledge base creation |

---

*Document last updated: 2026-01-09*
