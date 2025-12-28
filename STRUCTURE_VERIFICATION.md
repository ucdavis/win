# Project Structure Verification

This document shows the current project structure and verifies the dual-format rendering setup.

## File Tree

```
.
├── README.md                           # Main project documentation
├── DUAL_FORMAT_GUIDE.md               # Detailed guide for dual-format rendering
├── _quarto.yml                        # Main Quarto configuration
├── .gitignore                         # Git ignore for build artifacts
├── index.qmd                          # Book homepage
├── styles.css                         # Custom CSS for HTML format
└── chapters/
    ├── 01-introduction.qmd            # Chapter 1: Introduction
    └── 02-randomized-experiments.qmd  # Chapter 2: Randomized Experiments
```

## Key Configuration Elements

### _quarto.yml Configuration

The `_quarto.yml` file is configured with:

1. **Project Type**: `book` - for multi-chapter organization
2. **Output Directory**: `_book` - where rendered files go
3. **Dual Formats**:
   - `html`: Full book format with sidebar navigation
   - `revealjs`: Presentation slides for each chapter

### Critical Configuration Options

**HTML Format:**
- Theme: cosmo
- Table of contents enabled
- Number sections
- Custom CSS styling

**RevealJS Format:**
- Theme: simple
- Slide numbers enabled
- Chalkboard plugin enabled
- Output filename pattern: `{stem}-slides.html`

### Chapter Format

Each chapter uses:

```markdown
---
title: "Chapter Title"
format:
  html:
    toc: true
  revealjs:
    slide-number: true
---
```

### Content Conditional Blocks

Format-specific content uses:

```markdown
::: {.content-visible when-format="html"}
Content for HTML book version
:::

::: {.content-visible when-format="revealjs"}
Content for RevealJS slides
:::
```

## Expected Output Structure

After running `quarto render`, the `_book/` directory will contain:

```
_book/
├── index.html                                    # Homepage
├── chapters/
│   ├── 01-introduction.html                      # Chapter 1 HTML
│   ├── 01-introduction-slides.html               # Chapter 1 Slides
│   ├── 02-randomized-experiments.html            # Chapter 2 HTML
│   └── 02-randomized-experiments-slides.html     # Chapter 2 Slides
├── site_libs/                                    # Quarto dependencies
└── search.json                                   # Search index
```

## Rendering Commands

### Render All Formats
```bash
quarto render
```

### Render Specific Format
```bash
quarto render --to html
quarto render --to revealjs
```

### Preview During Development
```bash
quarto preview
```

## Implementation Pattern Summary

This implementation follows the dual-format pattern by:

1. **Single Source Files**: Each chapter is a single `.qmd` file
2. **Format Declarations**: Both formats declared in `_quarto.yml`
3. **Conditional Content**: Using `when-format` for format-specific content
4. **Distinct Filenames**: RevealJS uses `-slides.html` suffix
5. **Shared Navigation**: Book sidebar for HTML, slide navigation for RevealJS

## References

- [Quarto Multi-Format Projects](https://quarto.org/docs/output-formats/html-multi-format.html)
- [Quarto Discussions #1751](https://github.com/orgs/quarto-dev/discussions/1751)
- [quarto_html_revealjs_test](https://github.com/perellonieto/quarto_html_revealjs_test)

## Verification Checklist

- [x] `_quarto.yml` exists with dual formats configured
- [x] Both `html` and `revealjs` formats declared
- [x] Output filename pattern set for RevealJS: `{stem}-slides.html`
- [x] At least two example chapters created
- [x] Chapters use format-specific content blocks
- [x] Documentation created (README and DUAL_FORMAT_GUIDE)
- [x] `.gitignore` configured to exclude build artifacts
- [x] Custom CSS created for HTML format
- [x] Book structure with index page
- [x] Chapters listed in book configuration

All elements are in place for dual-format rendering!
