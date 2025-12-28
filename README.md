# What If? - Lecture Notes

Lecture notes based on https://miguelhernan.org/whatifbook

## Dual-Format Rendering

This Quarto book project is configured to render each chapter in two formats:

1. **HTML Book Format**: Traditional book layout with navigation sidebar
2. **RevealJS Slides Format**: Presentation slides for each chapter

### Structure

The project uses Quarto's multi-format rendering capability as described in:
- [Quarto Discussions #1751](https://github.com/orgs/quarto-dev/discussions/1751)
- [quarto_html_revealjs_test example](https://github.com/perellonieto/quarto_html_revealjs_test)

### Files

- `_quarto.yml`: Main configuration file with both HTML and RevealJS formats
- `index.qmd`: Book homepage
- `chapters/`: Directory containing chapter files
- `styles.css`: Custom CSS for the HTML format

### Rendering

To render both formats:

```bash
quarto render
```

This will generate:
- HTML book in `_book/` directory
- RevealJS slides with `-slides.html` suffix for each chapter

### Chapter Structure

Each chapter uses conditional content blocks to provide format-specific content:

```markdown
::: {.content-visible when-format="html"}
Detailed content for book format
:::

::: {.content-visible when-format="revealjs"}
Concise content for slides
:::
```

This allows the same source file to generate both a comprehensive HTML page and focused presentation slides.
