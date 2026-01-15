# Track Changes in PR Previews

This document explains the track changes functionality implemented for PR previews in the `win` repository.

## Overview

When a pull request is created or updated, the preview workflow automatically:

1. Detects which chapters have changed by comparing with the published version
2. Highlights changed content in HTML with color-coded markers
3. Creates DOCX files with tracked changes enabled
4. Adds a banner to the home page linking to changed chapters
5. Adds banners to changed chapters explaining the highlighting

## How It Works

### Workflow Steps

The `.github/workflows/preview.yml` workflow includes these steps:

1. **Detect Changed Chapters** - Compares rendered HTML/DOCX with gh-pages branch
2. **Inject Preview Metadata** - Adds `preview-changed: true` to changed .qmd files
3. **Re-render** - Re-renders with the metadata to trigger Lua filters
4. **Highlight HTML Changes** - Adds color-coded highlighting to changed content
5. **Create DOCX with Tracked Changes** - Generates DOCX files with revision marks
6. **Add Home Page Banner** - Links to changed chapters from the home page

### Scripts

Located in `.github/scripts/`:

- **detect-changed-chapters.py** - Detects which chapters changed
- **inject-preview-metadata.py** - Adds metadata to .qmd files
- **highlight-html-changes.py** - Highlights changed HTML content
- **create-docx-tracked-changes.py** - Creates DOCX with tracked changes
- **add-home-banner.py** - Adds banner to home page

### Lua Filter

`_extensions/preview-highlight.lua` - Adds a placeholder banner to changed pages that is later replaced with detailed change information.

### CSS Styles

`styles.css` includes styles for:

- `.preview-combined-banner` - Banner on changed chapters
- `.preview-home-changes-banner` - Banner on home page
- `.preview-text-changed` - Yellow highlight for modified text
- `.preview-text-added` - Green highlight for new text
- `.preview-element-added` - Blue highlight for new sections

## Highlighting Legend

- **Modified text (yellow)** - Text that was changed from the published version
- **Added text (green)** - Text that was newly added
- **New sections (blue)** - Entire paragraphs or sections that are new

## Disabling Highlights

If the highlighting is glitchy or causes issues, add the `no-preview-highlights` label to the PR. This will:

- Skip the metadata injection and re-rendering steps
- Skip the HTML highlighting step
- Still detect changes and show the home page banner
- Still create DOCX with tracked changes (if available)

## DOCX Tracked Changes

For chapters with DOCX output, the workflow creates `-tracked-changes.docx` versions that:

- Enable track changes mode in Word
- Mark changed paragraphs as revisions
- Show "PR Preview" as the author of changes
- Can be downloaded and opened in Word to review changes

## First PR / No gh-pages Branch

If this is the first PR or the gh-pages branch doesn't exist yet:

- All rendered files are treated as changed
- No comparison highlighting is performed (since there's no baseline)
- A message indicates this is the first PR

## Dependencies

- Python 3 (included in Ubuntu runners)
- `python-docx` package (installed during workflow)
- Git (for fetching gh-pages branch)

## Troubleshooting

### No changes detected

- Check that gh-pages branch exists and is up to date
- Verify that files actually changed in the PR
- Check workflow logs for error messages

### Highlighting not showing

- Verify the `no-preview-highlights` label is not applied
- Check browser console for CSS/JavaScript errors
- Try hard-refreshing the preview page

### DOCX tracked changes not working

- Verify `python-docx` installed successfully
- Check that base DOCX files exist in gh-pages
- Review workflow logs for error messages

## Credits

This implementation is based on the track changes functionality from the [UCD-SERG/lab-manual](https://github.com/UCD-SERG/lab-manual) repository.
