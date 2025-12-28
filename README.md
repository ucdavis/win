# What If? - Lecture Notes

Lecture notes based on https://miguelhernan.org/whatifbook

## Multi-Format Rendering

This Quarto website project is configured to render each chapter in multiple formats:

1. **HTML Website**: Traditional website layout with navigation navbar
2. **RevealJS Slides Format**: Presentation slides for each chapter
3. **PDF Handouts**: PDF documents for each chapter

### Structure

The project uses Quarto's multi-format rendering capability with profile-based configuration:
- Default profile: website (generates HTML, RevealJS, and PDF in `_site/`)
- RevealJS profile: standalone slides rendering (generates slides in `_slides/`)
- Handout profile: standalone PDF rendering (generates PDFs in `_handouts/`)

### Files

- `_quarto.yml`: Main configuration file with shared settings and default profile
- `_quarto-website.yml`: Website configuration with HTML, RevealJS, and PDF formats
- `_quarto-revealjs.yml`: Standalone RevealJS slides configuration
- `_quarto-handout.yml`: Standalone PDF handouts configuration
- `index.qmd`: Website homepage
- `chapters/`: Directory containing chapter files
- `styles.css`: Custom CSS for the HTML format

### Rendering

To render the default website with all formats:

```bash
quarto render
```

This will generate in `_site/` directory:
- HTML pages: `index.html`, `chapters/01-introduction.html`, etc.
- RevealJS slides: `index-slides.html`, `chapters/01-introduction-slides.html`, etc.
- PDF handouts: `index-handout.pdf`, `chapters/01-introduction-handout.pdf`, etc.

To render only slides:

```bash
QUARTO_PROFILE=revealjs quarto render
```

To render only PDF handouts:

```bash
QUARTO_PROFILE=handout quarto render
```

### Chapter Structure

Each chapter uses conditional content blocks to provide format-specific content:

```markdown
::: {.content-visible when-format="html"}
Detailed content for website format
:::

::: {.content-visible when-format="revealjs"}
Concise content for slides
:::
```

This allows the same source file to generate comprehensive HTML pages, focused presentation slides, and PDF handouts.
