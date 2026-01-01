#!/usr/bin/env python3
"""
Generate Agent Activity Log - Shows all agent operations on resources
"""

import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from lib.supabase_client import get_supabase_client


def generate_activity_log():
    """Generate activity log showing all agent operations"""

    supabase = get_supabase_client()

    # Get all documents with their processing chain
    documents = supabase.table('documents').select(
        'id, title, url, created_at, source_id, sources(name)'
    ).execute()

    # Get all extractions
    extractions = supabase.table('extractions').select(
        'id, document_id, word_count, created_at'
    ).execute()

    # Get all summaries
    summaries = supabase.table('summaries').select(
        'id, extraction_id, model_used, analyzed_at'
    ).execute()

    # Create lookup dictionaries
    extraction_by_doc = {e['document_id']: e for e in extractions.data}
    summary_by_ext = {s['extraction_id']: s for s in summaries.data}

    # Build output
    output = []
    output.append("# Agent Activity Log")
    output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("")
    output.append("This log tracks all agent operations performed on resources in the system.")
    output.append("")

    # Summary statistics
    output.append("## Summary Statistics")
    output.append("")
    output.append(f"- Total documents ingested: {len(documents.data)}")
    output.append(f"- Total extractions created: {len(extractions.data)}")
    output.append(f"- Total summaries generated: {len(summaries.data)}")
    output.append("")

    # Count by source
    source_counts = {}
    for doc in documents.data:
        source_name = doc['sources']['name'] if doc.get('sources') else 'Unknown'
        source_counts[source_name] = source_counts.get(source_name, 0) + 1

    output.append("### Documents by Source")
    for source, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        output.append(f"- {source}: {count} documents")
    output.append("")

    # Detailed log
    output.append("## Detailed Activity Log")
    output.append("")
    output.append("### Format")
    output.append("```")
    output.append("[Timestamp] Agent Name → Action → Resource")
    output.append("            Details: what was done")
    output.append("```")
    output.append("")

    # Process each document
    for i, doc in enumerate(sorted(documents.data, key=lambda x: x['created_at']), 1):
        doc_id = doc['id']
        title = doc['title'][:60]
        source = doc['sources']['name'] if doc.get('sources') else 'Unknown'
        created = doc['created_at'][:19].replace('T', ' ')

        output.append(f"### {i}. {title}")
        output.append("")

        # Stage 1: Ingest
        output.append(f"**[{created}] INGEST AGENT** → Fetched document → `{doc_id[:8]}...`")
        output.append(f"  - Source: {source}")
        output.append(f"  - URL: {doc['url']}")
        output.append("")

        # Stage 2: Extraction
        if doc_id in extraction_by_doc:
            ext = extraction_by_doc[doc_id]
            ext_id = ext['id']
            ext_created = ext['created_at'][:19].replace('T', ' ')
            output.append(f"**[{ext_created}] EXTRACTION AGENT** → Cleaned text → `{ext_id[:8]}...`")
            output.append(f"  - Word count: {ext['word_count']:,} words")
            output.append(f"  - Reading time: {ext['word_count'] // 200} minutes")
            output.append("")

            # Stage 3: Embedding
            output.append(f"**[{ext_created}] EMBEDDING GENERATOR** → Generated vector → `{ext_id[:8]}...`")
            output.append(f"  - Model: text-embedding-3-small")
            output.append(f"  - Dimensions: 1,536")
            output.append("")

            # Stage 4: Analysis
            if ext_id in summary_by_ext:
                summ = summary_by_ext[ext_id]
                summ_id = summ['id']
                analyzed = summ['analyzed_at'][:19].replace('T', ' ') if summ.get('analyzed_at') else ext_created
                output.append(f"**[{analyzed}] ANALYSIS AGENT** → Extracted insights → `{summ_id[:8]}...`")
                output.append(f"  - Model: {summ['model_used']}")
                output.append("")

        output.append("---")
        output.append("")

    # Add regeneration instructions
    output.append("## Regenerating This Log")
    output.append("")
    output.append("To regenerate this log with updated data, run:")
    output.append("")
    output.append("```bash")
    output.append('cd "/Users/JoshR/Desktop/fun/Frontier AI"')
    output.append("python3 scripts/generate_activity_log.py")
    output.append("```")
    output.append("")
    output.append("This will query the database and create an updated AGENT_ACTIVITY_LOG.md file with all agent operations.")

    return "\n".join(output)


def main():
    """Main execution"""
    print("Generating Agent Activity Log...")

    try:
        log_content = generate_activity_log()

        # Write to file
        output_file = Path(__file__).parent.parent / "AGENT_ACTIVITY_LOG.md"
        output_file.write_text(log_content)

        print(f"✅ Activity log written to: {output_file}")
        print(f"   File size: {len(log_content):,} bytes")

    except Exception as e:
        print(f"❌ Error generating activity log: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
