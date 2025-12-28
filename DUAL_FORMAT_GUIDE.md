# Dual-Format Rendering Guide

This document explains how this Quarto project is configured to render both HTML and RevealJS formats from the same source files.

## Configuration Structure

The project follows the pattern described in:
- [Quarto Discussions #1751](https://github.com/orgs/quarto-dev/discussions/1751) - Multi-format book rendering
- [quarto_html_revealjs_test](https://github.com/perellonieto/quarto_html_revealjs_test) - Example implementation

## How It Works

### 1. Project Configuration (`_quarto.yml`)

The `_quarto.yml` file defines both output formats:

```yaml
project:
  type: book
  output-dir: _book

format:
  html:
    theme: cosmo
    css: styles.css
    # ... HTML-specific options
    
  revealjs:
    theme: simple
    slide-number: true
    # ... RevealJS-specific options
    output-file: "{stem}-slides.html"
```

Key points:
- The `format` section lists both `html` and `revealjs`
- The `output-file: "{stem}-slides.html"` ensures slides get a distinct filename
- When you run `quarto render`, both formats are generated

### 2. Chapter-Level Format Options

Each chapter can override format options in its YAML frontmatter:

```yaml
---
title: "Chapter Title"
format:
  html:
    toc: true
  revealjs:
    slide-number: true
---
```

### 3. Format-Specific Content

Use conditional blocks to show different content for each format:

```markdown
::: {.content-visible when-format="html"}
This content appears only in the HTML book version.
It can be detailed explanations, longer paragraphs, etc.
:::

::: {.content-visible when-format="revealjs"}
This content appears only in RevealJS slides.
Keep it concise and slide-friendly.
:::
```

You can also have shared content that appears in both formats - just write it normally without conditional blocks.

### 4. Output Structure

After running `quarto render`, you'll get:

```
_book/
├── index.html              # Book homepage
├── chapters/
│   ├── 01-introduction.html           # Chapter 1 HTML
│   ├── 01-introduction-slides.html    # Chapter 1 slides
│   ├── 02-randomized-experiments.html # Chapter 2 HTML
│   ├── 02-randomized-experiments-slides.html # Chapter 2 slides
│   └── ...
└── ...
```

## Best Practices

### Content Strategy

**HTML Format (Book)**:
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
2. **Consistency**: Content stays synchronized between formats
3. **Efficiency**: Update once, renders to both formats
4. **Flexibility**: Customize presentation for each format's strengths
5. **Version Control**: Track changes to both formats together

## Rendering

### Render Everything
```bash
quarto render
```

### Render Specific Format
```bash
quarto render --to html
quarto render --to revealjs
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
