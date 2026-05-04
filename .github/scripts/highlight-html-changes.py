#!/usr/bin/env python3
"""
Script to compare rendered HTML files and highlight changed sections.
This compares the PR's rendered HTML with the published version from gh-pages.
"""

import os
import sys
import re
import difflib
import subprocess
from pathlib import Path
from html import escape, unescape

class HTMLDiffer:
    """Compare HTML files and inject highlighting for changed sections."""
    
    def __init__(self, local_html_dir, base_html_dir=None):
        self.local_html_dir = Path(local_html_dir)
        self.base_html_dir = Path(base_html_dir) if base_html_dir else None
        
    def fetch_base_html(self, filepath):
        """Get the base (published) HTML for comparison."""
        if not self.base_html_dir:
            return None
            
        # Get the relative path and construct base path
        relative_path = filepath.relative_to(self.local_html_dir)
        base_path = self.base_html_dir / relative_path
        
        if not base_path.exists():
            # Try alternate paths
            alt_base_path = self.base_html_dir / "_site" / relative_path
            if alt_base_path.exists():
                base_path = alt_base_path
            else:
                print(f"  Base file not found: {base_path}", file=sys.stderr)
                return None
        
        try:
            with open(base_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"  Could not read {base_path}: {e}", file=sys.stderr)
            return None
    
    def extract_main_content(self, html):
        """Extract the main content section from HTML, ignoring navigation and metadata."""
        # Find the main content area (typically in <main> or specific div)
        main_match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
        if main_match:
            return main_match.group(1)
        
        # Fallback: look for common content containers
        content_match = re.search(r'<div[^>]*class="[^"]*content[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
        if content_match:
            return content_match.group(1)
        
        return html
    
    def normalize_html(self, html):
        """Normalize HTML for better comparison (remove extra whitespace, etc.)."""
        # Remove extra whitespace
        html = re.sub(r'\s+', ' ', html)
        # Remove comments
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        return html.strip()
    
    def extract_text_from_element(self, element_html):
        """Extract plain text from an HTML element, preserving basic structure."""
        # Remove inner HTML tags but keep the text
        text = re.sub(r'<[^>]+>', '', element_html)
        return unescape(text).strip()
    
    def highlight_html_diff(self, old_html, new_html):
        """Highlight differences between old and new HTML content, preserving HTML tags."""
        # Extract text for comparison
        old_text = self.extract_text_from_element(f'<div>{old_html}</div>')
        new_text = self.extract_text_from_element(f'<div>{new_html}</div>')
        
        if not old_text or not new_text:
            return new_html
        
        # Split into words for both text versions
        old_words = re.findall(r'\S+|\s+', old_text)
        new_words = re.findall(r'\S+|\s+', new_text)
        
        # Use SequenceMatcher to find differences at word level
        matcher = difflib.SequenceMatcher(None, old_words, new_words)
        
        # Build a set of word positions that changed
        changed_ranges = []
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag in ('replace', 'insert'):
                start_pos = len(''.join(new_words[:j1]))
                end_pos = len(''.join(new_words[:j2]))
                changed_ranges.append((start_pos, end_pos, tag))
        
        if not changed_ranges:
            return new_html
        
        # Parse HTML into tokens (tags and text)
        html_tokens = re.findall(r'(<[^>]+>|[^<]+)', new_html)
        
        result = []
        text_pos = 0
        
        for token in html_tokens:
            if token.startswith('<'):
                result.append(token)
            else:
                token_len = len(token)
                token_end = text_pos + token_len
                highlighted = self.apply_highlights_to_text(token, text_pos, changed_ranges)
                result.append(highlighted)
                text_pos = token_end
        
        return ''.join(result)
    
    def apply_highlights_to_text(self, text, text_start_pos, changed_ranges):
        """Apply highlight marks to a text segment based on changed ranges."""
        if not text.strip():
            return text
        
        text_end_pos = text_start_pos + len(text)
        overlapping = []
        
        for start, end, change_type in changed_ranges:
            if start < text_end_pos and end > text_start_pos:
                overlap_start = max(0, start - text_start_pos)
                overlap_end = min(len(text), end - text_start_pos)
                overlapping.append((overlap_start, overlap_end, change_type))
        
        if not overlapping:
            return text
        
        overlapping.sort()
        
        result = []
        last_end = 0
        
        for overlap_start, overlap_end, change_type in overlapping:
            if overlap_start > last_end:
                result.append(text[last_end:overlap_start])
            
            highlighted_text = text[overlap_start:overlap_end]
            if change_type == 'replace':
                result.append(f'<mark class="preview-text-changed">{highlighted_text}</mark>')
            elif change_type == 'insert':
                result.append(f'<mark class="preview-text-added">{highlighted_text}</mark>')
            
            last_end = overlap_end
        
        if last_end < len(text):
            result.append(text[last_end:])
        
        return ''.join(result)
    
    def highlight_changed_elements(self, old_html, new_html):
        """Find and highlight changed paragraphs and sections in the HTML."""
        if not old_html:
            return new_html, 0
        
        SIMILARITY_THRESHOLD_MIN = 0.5
        SIMILARITY_THRESHOLD_MAX = 0.99
        
        old_content = self.extract_main_content(old_html)
        new_content = self.extract_main_content(new_html)
        
        COMPARABLE_ELEMENTS = 'p|h[1-6]|li|blockquote'
        element_pattern = f'(<(?:{COMPARABLE_ELEMENTS})[^>]*>.*?</(?:{COMPARABLE_ELEMENTS})>)'
        
        old_elements = re.findall(element_pattern, old_content, re.DOTALL)
        new_elements = re.findall(element_pattern, new_content, re.DOTALL)
        
        old_elem_list = []
        for elem in old_elements:
            text = self.extract_text_from_element(elem)
            if text:
                old_elem_list.append((text, elem))
        
        used_old_indices = set()
        highlighted_new_html = new_html
        changes_made = 0
        
        for new_elem in new_elements:
            new_text = self.extract_text_from_element(new_elem)
            if not new_text:
                continue
            
            best_match_idx = None
            best_ratio = 0.0
            
            for idx, (old_text, old_elem) in enumerate(old_elem_list):
                if idx in used_old_indices:
                    continue
                    
                ratio = difflib.SequenceMatcher(None, old_text, new_text).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_match_idx = idx
            
            if best_match_idx is not None and best_ratio > SIMILARITY_THRESHOLD_MIN and best_ratio < SIMILARITY_THRESHOLD_MAX:
                used_old_indices.add(best_match_idx)
                old_text, old_elem = old_elem_list[best_match_idx]
                
                tag_match = re.match(r'(<[^>]+>)(.*)(</[^>]+>)', new_elem, re.DOTALL)
                if tag_match:
                    open_tag, inner_content, close_tag = tag_match.groups()
                    
                    old_tag_match = re.match(r'(<[^>]+>)(.*)(</[^>]+>)', old_elem, re.DOTALL)
                    old_inner_content = old_tag_match.group(2) if old_tag_match else ""
                    
                    highlighted_inner = self.highlight_html_diff(old_inner_content, inner_content)
                    highlighted_elem = f'{open_tag}{highlighted_inner}{close_tag}'
                    
                    highlighted_new_html = highlighted_new_html.replace(new_elem, highlighted_elem, 1)
                    changes_made += 1
            
            elif (best_match_idx is None or best_ratio < SIMILARITY_THRESHOLD_MIN) and new_text:
                tag_match = re.match(r'(<[^>]+>)(.*)(</[^>]+>)', new_elem, re.DOTALL)
                if tag_match:
                    open_tag, inner_content, close_tag = tag_match.groups()
                    highlighted_elem = f'{open_tag}<mark class="preview-element-added">{inner_content}</mark>{close_tag}'
                    
                    highlighted_new_html = highlighted_new_html.replace(new_elem, highlighted_elem, 1)
                    changes_made += 1
        
        return highlighted_new_html, changes_made
    
    def find_changed_sections(self, old_html, new_html):
        """Find sections that changed between old and new HTML."""
        if not old_html:
            return None, 0
        
        old_content = self.normalize_html(self.extract_main_content(old_html))
        new_content = self.normalize_html(self.extract_main_content(new_html))
        
        similarity = difflib.SequenceMatcher(None, old_content, new_content).ratio()
        
        if similarity > 0.95:
            return None, similarity
        
        old_lines = old_content.split('\n')
        new_lines = new_content.split('\n')
        
        differ = difflib.unified_diff(old_lines, new_lines, lineterm='')
        diff_lines = list(differ)
        
        changes = sum(1 for line in diff_lines if line.startswith('+') or line.startswith('-'))
        
        return diff_lines if changes > 0 else None, similarity
    
    def inject_combined_banner(self, html, num_changes, similarity, filename):
        """Add a combined banner about all changes to the HTML."""
        change_pct = int((1 - similarity) * 100)
        
        notice = f'''
<div class="preview-combined-banner">
    <p style="margin: 0;">
        <strong>📝 Preview Changes:</strong> This page has been modified in this pull request (~{change_pct}% of content changed).
        <br>
        <strong>🎨 Highlighting Legend:</strong> 
        <mark class="preview-text-changed" style="display: inline; padding: 1px 3px;">Modified text (yellow)</mark> shows changed words/phrases, 
        <mark class="preview-text-added" style="display: inline; padding: 1px 3px;">added text (green)</mark> shows new content, and 
        <mark class="preview-element-added" style="display: inline; padding: 1px 3px;">new sections (blue)</mark> highlight entirely new paragraphs.
    </p>
</div>
'''
        
        placeholder_pattern = r'<div class="preview-changed-banner"[^>]*>.*?PREVIEW_BANNER_PLACEHOLDER.*?</div>'
        if re.search(placeholder_pattern, html, re.DOTALL):
            html = re.sub(placeholder_pattern, notice, html, flags=re.DOTALL)
        else:
            main_match = re.search(r'(<main[^>]*>)', html)
            if main_match:
                insertion_point = main_match.end()
                html = html[:insertion_point] + notice + html[insertion_point:]
        
        return html
    
    def process_file(self, local_filepath):
        """Process a single HTML file: fetch old version, compare, and highlight."""
        print(f"Processing {local_filepath}...")
        
        with open(local_filepath, 'r', encoding='utf-8') as f:
            new_html = f.read()
        
        has_placeholder = 'PREVIEW_BANNER_PLACEHOLDER' in new_html
        
        old_html = self.fetch_base_html(local_filepath)
        
        if old_html:
            diff_lines, similarity = self.find_changed_sections(old_html, new_html)
            
            print(f"  Checking for inline changes (overall similarity: {similarity:.2%})...")
            highlighted_html, inline_changes = self.highlight_changed_elements(old_html, new_html)
            
            if inline_changes > 0:
                print(f"  ✓ Highlighted {inline_changes} changed element(s) inline")
                new_html = highlighted_html
            else:
                print(f"  No inline changes detected")
            
            if diff_lines or has_placeholder:
                num_changes = len([l for l in diff_lines if l.startswith('+') or l.startswith('-')]) if diff_lines else 0
                print(f"  Adding combined banner (changes: {num_changes}, similarity: {similarity:.2%})")
                new_html = self.inject_combined_banner(new_html, num_changes, similarity, local_filepath)
            
            if diff_lines or has_placeholder or inline_changes > 0:
                print(f"  Writing changes back to file...")
                with open(local_filepath, 'w', encoding='utf-8') as f:
                    f.write(new_html)
                print(f"  ✓ Updated {local_filepath}")
            else:
                print(f"  No changes to write")
        elif has_placeholder:
            print(f"  Could not fetch base version (file may be new)")
            new_html = self.inject_combined_banner(new_html, 1, 0.0, local_filepath)
            with open(local_filepath, 'w', encoding='utf-8') as f:
                f.write(new_html)
            print(f"  ✓ Updated {local_filepath}")
        else:
            print(f"  Could not fetch base version (file may be new)")


def checkout_base_html(base_ref='origin/gh-pages', target_dir='/tmp/base-html'):
    """Check out the base HTML files from gh-pages for comparison."""
    target_path = Path(target_dir)
    target_path.mkdir(parents=True, exist_ok=True)
    
    try:
        subprocess.run(['git', 'fetch', 'origin', 'gh-pages:gh-pages'], 
                      check=False, capture_output=True)
        
        result = subprocess.run(
            ['git', 'ls-tree', '-r', '--name-only', base_ref],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            files = [f for f in result.stdout.split('\n') if f.endswith('.html')]
            
            for file in files:
                output_path = target_path / file
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'wb') as f:
                    subprocess.run(
                        ['git', 'show', f'{base_ref}:{file}'],
                        stdout=f,
                        check=False
                    )
            
            return target_path if files else None
        
        return None
    except Exception as e:
        print(f"Could not check out base HTML: {e}", file=sys.stderr)
        return None

def main():
    html_dir = os.getenv('HTML_DIR', './_site')
    changed_files = os.getenv('PREVIEW_CHANGED_CHAPTERS', '').strip()
    
    if not changed_files:
        print("No changed files to process")
        return
    
    print("Checking out base HTML from gh-pages...")
    base_html_dir = checkout_base_html()
    
    if not base_html_dir:
        print("Warning: Could not check out base HTML, will skip content comparison")
    else:
        print(f"Base HTML checked out to {base_html_dir}")
    
    # changed_files contains chapter IDs - convert to HTML paths
    html_files = []
    for chapter_id in changed_files.split('\n'):
        chapter_id = chapter_id.strip()
        if chapter_id:
            html_file = f"{chapter_id}.html"
            html_path = Path(html_dir) / "chapters" / html_file
            if html_path.exists():
                html_files.append(html_path)
    
    if not html_files:
        print("No HTML files to process")
        return
    
    differ = HTMLDiffer(html_dir, base_html_dir)
    
    for html_file in html_files:
        differ.process_file(html_file)

if __name__ == '__main__':
    main()
