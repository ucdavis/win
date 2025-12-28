# Multi-Format Rendering Guide

This document explains how this Quarto project is configured to render HTML, RevealJS, PDF, and DOCX formats from the same source files.

## Configuration Structure

The project follows the pattern described in:
- [Quarto Discussions #1751](https://github.com/orgs/quarto-dev/discussions/1751) - Multi-format book rendering
- [quarto_html_revealjs_test](https://github.com/perellonieto/quarto_html_revealjs_test) - Example implementation

## How It Works

### 1. Project Configuration (`_quarto-website.yml`)

The `_quarto-website.yml` file defines all output formats:

```yaml
format:
  html:
    theme: cosmo
    css: styles.css
    # ... HTML-specific options
    
  revealjs:
    theme: simple
    slide-number: true
    # ... RevealJS-specific options
    
  pdf:
    geometry:
      - top=15mm
      - bottom=20mm
    # ... PDF-specific options
    
  docx:
    toc: true
    number-sections: true
    # ... DOCX-specific options
```

Key points:
- The `format` section lists all four formats: `html`, `revealjs`, `pdf`, and `docx`
- Each format has specific configuration options
- When you run `quarto render`, all formats are generated

### 2. Chapter-Level Format Options

Each chapter can override format options in its YAML frontmatter:

```yaml
---
title: "Chapter Title"
format:
  html: default
  revealjs:
    output-file: chapter-slides.html
  pdf:
    output-file: chapter-handout.pdf
  docx:
    output-file: chapter.docx
---
```

### 3. Format-Specific Content

Use conditional blocks to show different content for each format:

```markdown
::: {.content-visible when-format="html"}
This content appears only in the HTML website version.
It can be detailed explanations, longer paragraphs, etc.
:::

::: {.content-visible when-format="revealjs"}
This content appears only in RevealJS slides.
Keep it concise and slide-friendly.
:::

::: {.content-visible when-format="pdf"}
This content appears only in PDF handouts.
Good for print-optimized content and references.
:::

::: {.content-visible when-format="docx"}
This content appears only in DOCX documents.
Useful for Word-specific formatting needs.
:::
```

You can also have shared content that appears in all formats - just write it normally without conditional blocks.

### 4. Output Structure

After running `quarto render`, you'll get:

```
_site/
├── index.html                                     # Homepage HTML
├── index-slides.html                              # Homepage slides
├── index-handout.pdf                              # Homepage PDF
├── index.docx                                     # Homepage DOCX
├── chapters/
│   ├── 01-introduction.html                       # Chapter 1 HTML
│   ├── 01-introduction-slides.html                # Chapter 1 slides
│   ├── 01-introduction-handout.pdf                # Chapter 1 PDF
│   ├── 01-introduction.docx                       # Chapter 1 DOCX
│   ├── 02-randomized-experiments.html             # Chapter 2 HTML
│   ├── 02-randomized-experiments-slides.html      # Chapter 2 slides
│   ├── 02-randomized-experiments-handout.pdf      # Chapter 2 PDF
│   ├── 02-randomized-experiments.docx             # Chapter 2 DOCX
│   └── ...
└── ...
```

## Best Practices

### Content Strategy

**HTML Format (Website)**:
- Detailed explanations
- Comprehensive examples
- Long-form text
- Detailed mathematical derivations
- Extended discussions

**RevealJS Format (Slides)**:
- Concise bullet points
- Key concepts highlighted
- Visual presentations
- Summary equations
- Progressive disclosure with fragments

**PDF Format (Handouts)**:
- Print-optimized layout
- References and citations
- Comprehensive content for offline reading
- Suitable for printing and annotation

**DOCX Format (Word Documents)**:
- Editable format for further customization
- Useful for collaboration and comments
- Compatible with Microsoft Word and similar applications
- Easy to share and edit

### Structuring Chapters

1. **Use semantic headings**: `##` for sections that become slides
2. **Share common content**: Core definitions and equations
3. **Differentiate details**: Use conditional blocks for format-specific elaboration
4. **Maintain consistency**: Each chapter should follow similar patterns

### Example Pattern

```markdown
## Section Title

Shared introductory sentence or definition.

::: {.content-visible when-format="html"}
Extended explanation with multiple paragraphs,
detailed examples, and comprehensive coverage
suitable for a textbook.
:::

::: {.content-visible when-format="revealjs"}
### Key Points

- Concise bullet point 1
- Concise bullet point 2
- Concise bullet point 3

::: {.fragment}
Progressive reveal for emphasis
:::
:::
```

## Advantages

1. **Single Source**: Maintain one file per chapter
2. **Consistency**: Content stays synchronized across all formats
3. **Efficiency**: Update once, renders to all formats
4. **Flexibility**: Customize presentation for each format's strengths
5. **Version Control**: Track changes to all formats together
6. **Multiple Use Cases**: HTML for web, RevealJS for presentations, PDF for print, DOCX for editing

## Rendering

### Render Everything
```bash
quarto render
```

### Render Specific Format
```bash
quarto render --to html
quarto render --to revealjs
quarto render --to pdf
quarto render --to docx
```

### Render Multiple Formats
```bash
quarto render --to html,revealjs,docx
```

### Render Specific File
```bash
quarto render chapters/01-introduction.qmd
```

### Preview During Development
```bash
quarto preview
```

## Customization

### HTML Styling
Edit `styles.css` to customize the book appearance.

### RevealJS Theme
Modify the `revealjs.theme` option in `_quarto.yml` or create a custom theme.

### Format-Specific CSS
You can add format-specific CSS classes:

```markdown
::: {.html-only}
HTML-specific styled content
:::

::: {.slides-only}
Slides-specific styled content
:::
```

Then in `styles.css`:
```css
.html-only { /* HTML-specific styles */ }
```

And in a custom RevealJS CSS file:
```css
.slides-only { /* Slides-specific styles */ }
```
