# PT Entrepreneurship Knowledge Base

A comprehensive, AI-optimized knowledge base derived from the Uncaged Clinician community - the premier Facebook group for Physical Therapy practice owners and entrepreneurs.

## Overview

| Metric | Value |
|--------|-------|
| **Total Posts** | 9,567 |
| **Total Comments** | 74,894 |
| **Unique Topics** | 16 categories |
| **Date Range** | May 2022 - January 2026 |
| **High Engagement Posts** | 2,109 |
| **Source** | Uncaged Clinician Facebook Group |

## Purpose

This knowledge base is designed for:
- **Conversational Q&A** - Ask questions about PT business ownership
- **Content Generation** - Create articles, guides, and social posts
- **Business Analysis** - Research pricing, marketing, hiring trends
- **Decision Support** - Get real-world insights from practitioners

## Directory Structure

```
knowledge-base/
├── README.md                          # This file
├── process_knowledge_base.py          # Processing script
├── indexes/
│   ├── master-index.json              # Overall statistics and topic breakdown
│   ├── high-engagement-index.jsonl    # Top posts by engagement
│   └── searchable-index.jsonl         # Quick-reference index of all posts
├── metadata/
│   └── taxonomy.json                  # Topic classification rules
├── topics/
│   ├── 01-starting-your-practice/
│   ├── 02-pricing-revenue-compensation/
│   ├── 03-insurance-billing-reimbursement/
│   ├── 04-marketing-client-acquisition/
│   ├── 05-operations-systems-tools/
│   ├── 06-staffing-hiring-team/
│   ├── 07-clinical-practice-specialties/
│   ├── 08-legal-compliance-regulations/
│   ├── 09-finance-taxes-accounting/
│   ├── 10-growth-scaling-exit/
│   ├── 11-work-life-mindset-burnout/
│   ├── 12-telehealth-virtual-care/
│   ├── 13-mobile-home-health/
│   ├── 14-continuing-education-ceus/
│   ├── 15-networking-community/
│   └── 16-general-qa-advice/
└── raw/
    └── original-data.json             # Preserved original dataset
```

## Topic Categories

### 1. Starting Your Practice (528 posts)
Business formation, initial setup, location decisions, first clients, making the leap from employment.

### 2. Pricing, Revenue & Compensation (709 posts)
Session pricing, package rates, salary discussions, cash-pay rates, revenue strategies.

### 3. Insurance, Billing & Reimbursement (1,190 posts)
Medicare/Medicaid, private insurance, credentialing, billing processes, coding, claims, cash vs insurance models.

### 4. Marketing & Client Acquisition (978 posts)
Getting patients, referrals, advertising, social media, physician relationships, gym partnerships.

### 5. Operations, Systems & Tools (577 posts)
EHR/EMR systems, scheduling, documentation, software recommendations, workflow optimization.

### 6. Staffing, Hiring & Team (443 posts)
Hiring employees, contractors, PTAs, front desk, team management, compensation structures.

### 7. Clinical Practice & Specialties (801 posts)
Treatment approaches, specialty niches (pelvic floor, dry needling, sports), patient outcomes.

### 8. Legal, Compliance & Regulations (319 posts)
Malpractice insurance, HIPAA, ADA, state regulations, contracts, liability.

### 9. Finance, Taxes & Accounting (145 posts)
Bookkeeping, tax strategies, retirement planning, loans, financial planning.

### 10. Growth, Scaling & Exit (113 posts)
Expanding practice, multiple locations, selling business, partnerships, exit strategies.

### 11. Work-Life Balance, Mindset & Burnout (195 posts)
Avoiding burnout, time management, entrepreneurial mindset, boundaries.

### 12. Telehealth & Virtual Care (63 posts)
Virtual visits, telehealth platforms, regulations, billing for telehealth.

### 13. Mobile PT & Home Health (385 posts)
Mobile practice, home visits, home health agencies, travel considerations.

### 14. Continuing Education & CEUs (245 posts)
CEU requirements, certifications, courses, specialty training, conferences.

### 15. Networking & Community (218 posts)
Professional networking, community connections, collaborations, mentorship.

### 16. General Q&A & Advice (2,658 posts)
General questions, recommendations, polls, discussions that span multiple topics.

## File Formats

### JSONL Files (AI-Optimized)
Each topic folder contains a `.jsonl` file with one JSON object per line. Each record includes:

```json
{
  "thread_id": "123456789",
  "url": "https://www.facebook.com/groups/uncagedcliniciangroup/permalink/...",
  "date": "2024-03-15 14:30:22",
  "year": 2024,
  "quarter": "2024 Q1",
  "post_text": "The original post content...",
  "comments": [
    {"text": "Comment 1...", "date": "2024-03-15 15:00:00"},
    {"text": "Comment 2...", "date": "2024-03-15 16:30:00"}
  ],
  "comment_count": 15,
  "primary_topic": "02-pricing-revenue-compensation",
  "all_topics": ["02-pricing-revenue-compensation", "03-insurance-billing-reimbursement"],
  "reactions": 12,
  "engagement_score": 42,
  "engagement_tier": "high",
  "full_thread_text": "POST: The original post...\n\nCOMMENT 1: First comment..."
}
```

### Markdown Summaries (Human-Readable)
Each topic folder contains a `-summary.md` file with:
- Topic statistics
- Top 10 most engaged posts
- Year-by-year breakdown
- Quick reference for the topic

## How to Use with AI Projects

### Claude Projects
1. Create a new project in Claude
2. Upload the topic JSONL files relevant to your questions
3. For comprehensive coverage, upload:
   - `indexes/master-index.json` (always)
   - `indexes/high-engagement-index.jsonl` (for best content)
   - Topic-specific JSONL files as needed

**Recommended upload strategy:**
- For specific questions: Upload 2-3 relevant topic files
- For broad analysis: Upload high-engagement index + 5-6 key topics
- Maximum coverage: Upload all topic files (may hit token limits)

### ChatGPT Projects
Same approach as Claude - upload JSONL files to your project's knowledge base.

### Example Queries

**Pricing Strategy:**
> "Based on the community discussions, what's the optimal pricing strategy for a cash-based PT in a suburban area? Include specific price points mentioned."

**Marketing on a Budget:**
> "What are the most recommended low-cost marketing strategies for getting first clients? Prioritize advice with high engagement scores."

**Insurance vs Cash:**
> "Summarize the community's experience with transitioning from insurance-based to cash-based practice. Include timeline expectations and challenges."

**Hiring First Employee:**
> "What does the community recommend for hiring your first PTA? Include salary ranges, contract considerations, and red flags to avoid."

## Engagement Tiers

Posts are classified into engagement tiers for credibility weighting:

| Tier | Criteria | Count |
|------|----------|-------|
| **High** | 10+ reactions OR 15+ comments | 2,109 |
| **Medium** | 5+ reactions OR 5+ comments | 3,037 |
| **Low** | Below medium thresholds | 4,421 |

**Engagement Score Formula:**
```
score = reactions + (comments × 2) + (shares × 3)
```

## Provenance & Citations

Every record maintains full provenance:
- **thread_id**: Unique Facebook post identifier
- **url**: Direct link to original post
- **date**: Exact timestamp of the post
- **quarter**: Year and quarter for temporal context

When citing insights, reference the thread_id and date:
> "According to a high-engagement discussion from 2024 Q2 (thread: 789123456), practitioners reported..."

## Data Quality Notes

- **Completeness**: 99.98% valid posts (2 errors in 9,569 items)
- **Comment Coverage**: Top 2-3 comments per post (not full threads)
- **Attachments**: Limited - image/file content not extracted
- **Updates**: Dataset current through January 2026

## Processing Details

The knowledge base was generated using `process_knowledge_base.py` which:
1. Loads raw Facebook group export
2. Classifies posts using keyword-based taxonomy
3. Calculates engagement scores
4. Enriches records with metadata
5. Outputs organized JSONL and Markdown files
6. Creates searchable indexes

To reprocess with updated data:
```bash
python3 process_knowledge_base.py
```

---

*Knowledge Base Version: 1.0*
*Generated: 2026-01-09*
*Source: Uncaged Clinician Facebook Group (2022-2026)*
