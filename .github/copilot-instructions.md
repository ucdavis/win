# Copilot Instructions for win Repository

This document provides essential guidelines for GitHub Copilot when working on the "What If?" lecture notes repository. The project is a Quarto website that renders to HTML, RevealJS, and PDF formats.

## Installation and Setup

### Installing R

**CRITICAL**: When installing R, you MUST use the latest R release from CRAN.

**On Ubuntu/Debian**:
```bash
# Add CRAN repository first to get the latest R version
sudo apt update -qq
sudo apt install --no-install-recommends software-properties-common dirmngr
wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.gpg | sudo tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
sudo add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"
sudo apt install --no-install-recommends r-base

# Verify R version (should be 4.5.2 or later)
R --version
```

**NEVER** use the default Ubuntu R package (e.g., `apt-get install r-base` without adding CRAN repo) as it will be outdated (e.g., R 4.3.3 instead of R 4.5.2).

**On other systems**: Download the latest R release from https://cloud.r-project.org/

To set up the development environment:

```r
# Install renv if not already installed
install.packages("renv")

# Restore package dependencies from renv.lock
renv::restore()
```

### Installing Quarto

Download and install Quarto from https://quarto.org/docs/get-started/

```bash
# On Ubuntu/Debian
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.4.550/quarto-1.4.550-linux-amd64.deb
sudo dpkg -i quarto-1.4.550-linux-amd64.deb
```

Verify installation:
```bash
quarto --version
```

### Installing TinyTeX (for PDF rendering)

TinyTeX is required for rendering PDF handouts:

```bash
# Install via Quarto (preferred method)
quarto install tinytex --no-prompt

# Verify installation
quarto list tools
```

Alternative via R:
```r
install.packages("tinytex")
tinytex::install_tinytex()
```

### Key Dependencies

The project uses packages including:
- `knitr`, `rmarkdown` - document rendering (via Quarto)
- Additional packages as needed for causal inference examples

## Build, Test, and Lint Commands

### Building the Website

```bash
# Preview the website locally (with live reload)
quarto preview

# Render the entire website (HTML, RevealJS, and PDF formats)
quarto render

# Render without PDF (if TinyTeX is not installed)
quarto render --to html,revealjs

# Render a specific chapter
quarto render chapters/01-introduction.qmd

# Render only HTML format
quarto render --to html

# Render only RevealJS slides
quarto render --to revealjs

# Render using specific profiles
QUARTO_PROFILE=revealjs quarto render  # Standalone slides in _slides/
QUARTO_PROFILE=handout quarto render    # Standalone PDFs in _handouts/
```

### Output Structure

After rendering with the default profile, you'll find in `_site/`:
- `index.html` - Website homepage
- `index-slides.html` - RevealJS slides for homepage
- `index-handout.pdf` - PDF handout for homepage (requires TinyTeX)
- `chapters/01-introduction.html` - HTML chapter pages
- `chapters/01-introduction-slides.html` - RevealJS slide presentations
- `chapters/01-introduction-handout.pdf` - PDF handouts (requires TinyTeX)

### Running Tests

This is a documentation/notes repository, so there are no formal unit tests. However, you can verify code chunks work correctly by:

```r
# In R, render a specific Quarto document
quarto::quarto_render("chapters/01-introduction.qmd")
```

### Linting

```r
# Lint R code files
lintr::lint("script.R")

# Lint R code chunks in Quarto documents (requires extracting code)
# This is typically done via the lint-changed-files workflow
```

### Spell Checking

```r
# Run spell check on the repository
spelling::spell_check_package()

# Check specific files
spelling::spell_check_files("README.md")
```

## Code Style and Conventions

### General Guidelines

1. **Follow tidyverse style guide**: Use the tidyverse style guide for R code
2. **Use clear variable names**: Prefer descriptive names over abbreviations
3. **Comment mathematical formulas**: Explain the causal inference concepts when implementing examples
4. **Reproducibility**: Ensure all code chunks are reproducible with set seeds where necessary
5. **Use pipe operators**: Prefer the native R pipe (`|>`) or magrittr pipe (`%>%`) for data manipulation

### Naming Conventions

- **Functions**: Use snake_case (e.g., `calculate_ate`, `estimate_effect`)
- **Variables**: Use snake_case (e.g., `treatment_group`, `outcome_var`)
- **Chapter files**: Use numbered format with descriptive names (e.g., `01-introduction.qmd`, `02-randomized-experiments.qmd`)

### Documentation Standards

- Use Quarto/R Markdown formatting for mathematical notation (LaTeX)
- Include explanatory text before code chunks
- Add comments within complex code blocks
- Reference the "What If?" textbook (Hernán MA, Robins JM) when applicable
- Use code chunk options appropriately:
  - `echo=FALSE` to hide code in HTML, or use format-specific visibility
  - `message=FALSE` to suppress messages
  - `fig.align='center'` for centered figures

### Code Organization

- Chapter notes in `chapters/*.qmd` files with numbered prefixes
- Main index in `index.qmd`
- Configuration files: `_quarto.yml` (shared settings), `_quarto-website.yml` (website config), `_quarto-revealjs.yml` (slides config), `_quarto-handout.yml` (PDF config)
- Styling in `styles.css`
- Documentation in `README.md`, `DUAL_FORMAT_GUIDE.md`, `STRUCTURE_VERIFICATION.md`

## Repository Structure

```
win/
├── .github/
│   ├── workflows/              # GitHub Actions workflows
│   │   ├── check-spelling.yaml # Spell checking
│   │   ├── lint-changed-files.yaml # R code linting
│   │   ├── preview.yml         # PR preview deployment
│   │   └── publish.yml         # GitHub Pages publishing
│   └── copilot-instructions.md # This file
├── chapters/
│   ├── 01-introduction.qmd     # Chapter 1: Introduction
│   ├── 02-randomized-experiments.qmd # Chapter 2: Randomized Experiments
│   └── ...                     # Additional chapters
├── _site/                      # Generated website output (gitignored)
├── _slides/                    # Generated slides output (gitignored)
├── _handouts/                  # Generated PDF handouts (gitignored)
├── .quarto/                    # Quarto cache (gitignored)
├── index.qmd                   # Website homepage
├── _quarto.yml                 # Shared Quarto configuration with default profile
├── _quarto-website.yml         # Website configuration (multi-format: HTML, RevealJS, PDF)
├── _quarto-revealjs.yml        # Standalone RevealJS slides configuration
├── _quarto-handout.yml         # Standalone PDF handouts configuration
├── styles.css                  # Custom CSS styling
├── renv.lock                   # Package dependency lockfile
├── .Rprofile                   # R session configuration (when renv is used)
├── win.Rproj                   # RStudio project file
├── README.md                   # Project overview
├── DUAL_FORMAT_GUIDE.md        # Guide for dual-format rendering
└── STRUCTURE_VERIFICATION.md   # Implementation checklist
```

## Quarto Document Structure

### Front Matter

Each `.qmd` file should have YAML front matter with format specifications:

```yaml
---
title: "Chapter Title"
format:
  html: default
  revealjs:
    output-file: filename-slides.html
  pdf:
    output-file: filename-handout.pdf
---
```

This allows the same source file to generate three outputs:
- HTML page for the website
- RevealJS slides with `-slides.html` suffix
- PDF handout with `-handout.pdf` suffix

### Format-Specific Content

**IMPORTANT**: Minimize use of `.content-visible` divs. Most content should be shared between formats.

**Preferred approach**: Use speaker notes for additional context:

```markdown
## Section Title

Core content that appears in both HTML and RevealJS formats.
This should be concise enough for slides but informative enough for the website.

::: {.notes}
Additional detailed explanations that would clutter slides.
These appear as speaker notes in RevealJS and as regular text in HTML/PDF.
:::
```

**Only use `.content-visible` when absolutely necessary** (rarely needed):

```markdown
::: {.content-visible when-format="html"}
Content that truly only makes sense in HTML format
:::

::: {.content-visible when-format="pdf"}
Content specific to PDF format (e.g., print-specific formatting)
:::
```

### Speaker Notes for RevealJS

Use `.notes` divs to add detailed explanations that supplement slides without cluttering them:

```markdown
## Key Concept

Brief explanation suitable for slides.

::: {.notes}
Longer explanation with examples, context, and details.
This text appears in speaker view during presentations
and as regular text in HTML/PDF formats.
:::
```

See [Quarto RevealJS Speaker Notes documentation](https://quarto.org/docs/presentations/revealjs/#speaker-notes) for more details.

### Citations and References

Use Quarto's built-in citation system rather than manual citations:

1. Create a `references.bib` file in the project root
2. Add bibliography to `_quarto.yml`:
   ```yaml
   bibliography: references.bib
   csl: https://www.zotero.org/styles/apa  # or other style
   ```
3. Use citation syntax in documents:
   ```markdown
   As shown in @hernan2020causal [Chapter 1]...
   ```
4. Add a references section at the end of documents:
   ```markdown
   ## References
   
   ::: {#refs}
   :::
   ```

See [Quarto Citations documentation](https://quarto.org/docs/authoring/citations.html) for more details.

### Code Chunks

Use R code chunks with appropriate options:

````markdown
```{r echo=FALSE, message=FALSE}
library(ggplot2)
knitr::opts_chunk$set(fig.align = 'center', message = FALSE)
```
````

### Mathematical Notation

Use LaTeX for mathematical expressions:

```markdown
Inline math: $E[Y^a]$

Display math:
$$
E[Y^a] = \sum_c E[Y^a \mid C=c] P(C=c)
$$

Aligned equations:
\begin{align}
ATE &= E[Y^1] - E[Y^0] \\
    &= E[Y \mid A=1] - E[Y \mid A=0] \quad \text{(under randomization)}
\end{align}
```

## CI/CD Workflows

The repository uses GitHub Actions for continuous integration:

1. **publish.yml**: Builds and publishes the Quarto website to GitHub Pages
   - Runs on push to main branch
   - Uses Quarto actions to render and deploy
   - Installs TinyTeX for PDF rendering
   - Outputs to `_site/` directory
2. **preview.yml**: Generates preview of the website for pull requests
   - Uses PR preview action to deploy to separate preview URL
   - Allows reviewers to see rendered changes
   - Watches `_quarto-*.yml` files for configuration changes
   - Outputs to `_site/` directory
3. **lint-changed-files.yaml**: Runs lintr on changed R files in pull requests
4. **check-spelling.yaml**: Checks spelling across the repository

All workflows run on relevant triggers (push to main, pull requests, etc.).

## Important Notes

### Working with Causal Inference Examples

- Set random seeds for reproducibility: `set.seed()` or `withr::local_seed()`
- Document the causal concepts and their sources (refer to Hernán & Robins when applicable)
- Include references to papers and textbooks
- Explain DAGs and causal assumptions clearly
- Use clear notation for potential outcomes and interventions

### Multi-Format Rendering

**IMPORTANT**: This project uses a multi-format structure where each chapter renders to HTML, RevealJS, and PDF.

Key considerations:
- **HTML format**: Detailed, comprehensive website content for reading and study
- **RevealJS format**: Concise, presentation-oriented slides for teaching
- **PDF format**: Print-friendly handouts with references and notes
- **Content visibility**: Use `.content-visible when-format=` divs to show/hide content based on output format
- **Slide structure**: In RevealJS sections, use `##` for slide titles and `###` for content within slides
- **Progressive reveal**: Use `.fragment` classes for incremental display in slides
- **Output files**: 
  - HTML: `{filename}.html` (e.g., `01-introduction.html`)
  - RevealJS: `{filename}-slides.html` (e.g., `01-introduction-slides.html`)
  - PDF: `{filename}-handout.pdf` (e.g., `01-introduction-handout.pdf`)

See `DUAL_FORMAT_GUIDE.md` for comprehensive patterns and best practices.

### Profile-Based Rendering

The project supports multiple rendering profiles:

1. **Default (website)**: Renders all formats (HTML, RevealJS, PDF) to `_site/`
   ```bash
   quarto render
   ```

2. **RevealJS profile**: Renders only slides to `_slides/`
   ```bash
   QUARTO_PROFILE=revealjs quarto render
   ```

3. **Handout profile**: Renders only PDFs to `_handouts/`
   ```bash
   QUARTO_PROFILE=handout quarto render
   ```

### Data Visualization

- Use ggplot2 for consistency
- Follow tidyverse aesthetic principles
- Include axis labels and titles
- Use appropriate color schemes for accessibility
- Consider how visualizations will appear in all formats (slides may need larger fonts/simpler layouts, PDFs need to be printer-friendly)

### Making Changes

- When modifying `.qmd` files, ensure code chunks execute successfully
- Run `quarto preview` to verify changes render correctly in all formats
- Check mathematical notation renders properly
- Ensure figures display as intended in HTML, RevealJS, and PDF
- Verify cross-references and links work
- Update `_quarto-website.yml` if adding/removing chapters (and also update `_quarto-handout.yml` render list)

### Pull Request Development

**IMPORTANT**: When developing new pull requests, always run `quarto render` to ensure the website can be rendered successfully before finalizing your changes.

- **Always run `quarto render`** during PR development to verify that all changes render correctly
- **CRITICAL**: Test `quarto render` yourself and verify it actually succeeds before claiming success
  - Run the command and wait for it to complete
  - Check the exit code to confirm success (exit code 0)
  - Do not claim success based on partial output or assumptions
  - If the render fails, investigate and fix the issue before proceeding
  - **"Software not installed" is NOT a valid excuse** - install required software (R, Quarto, TinyTeX) first if needed (see Installation section above)
  - **CRITICAL**: When installing R, you MUST use the latest R release from CRAN (see Installation section)
    - **NEVER** use the default R from Ubuntu repositories (e.g., `apt-get install r-base` without adding CRAN repo)
    - The default Ubuntu R is outdated (e.g., R 4.3.3) and will cause issues
    - Always add the CRAN repository first, then install R to get the latest version (R 4.5.2+)
    - Verify the R version with `R --version` before proceeding
  - **Note**: If TinyTeX cannot be installed due to network restrictions, you can render without PDF using `quarto render --to html,revealjs`
- Check that the rendering completes without errors or warnings for all formats
- Review the generated output in the `_site/` directory to ensure quality in HTML, RevealJS, and PDF formats
- Verify that format-specific content appears correctly in each format
- Fix any rendering issues before requesting review
- This practice helps maintain the quality of rendered outputs and streamlines the contribution process
- Note: The CI/CD workflows (preview.yml and publish.yml) will also render the website, but catching issues locally saves time

### Dependencies

- Use `renv::snapshot()` after adding new packages
- Ensure all required packages are available
- Test that `renv::restore()` works for reproducibility

### Working with renv in CI/CD

This project uses `renv` for R package dependency management. The workflows are configured to use renv properly:

**Key points:**
1. **renv activation**: If using renv, the `.Rprofile` file activates renv with `source("renv/activate.R")`
2. **GitHub Actions setup**: Use `r-lib/actions/setup-renv@v2` in workflows instead of `setup-r-dependencies`
3. **Package repository**: The `renv.lock` file uses Posit Package Manager (https://packagemanager.posit.co/cran/latest)
4. **Cache management**: The `setup-renv` action automatically caches the renv library for faster builds

**Workflow configuration example:**
```yaml
- uses: r-lib/actions/setup-r@v2
  with:
    use-public-rspm: true

- uses: r-lib/actions/setup-renv@v2
  with:
    cache-version: 1
```

**Local testing with renv:**
- When you activate renv locally (by sourcing `.Rprofile` or running R in the project), renv creates its own package library
- The first time, run `renv::restore()` to install all packages from `renv.lock`
- Packages are cached in `~/.cache/R/renv/` (or similar) for reuse across projects
- `quarto render` will automatically use the renv environment when `.Rprofile` sources `renv/activate.R`

**Troubleshooting:**
- If `quarto render` fails with "package not found" errors, ensure you've run `renv::restore()` first
- Check that `.Rprofile` is activating renv (it should have `source("renv/activate.R")` uncommented)
- In CI/CD, the `setup-renv` action handles restoration automatically

## Getting Help

- Project GitHub: https://github.com/ucdavis/win
- Original Textbook: Hernán MA, Robins JM. "Causal Inference: What If." Boca Raton: Chapman & Hall/CRC, 2020. (https://www.hsph.harvard.edu/miguel-hernan/causal-inference-book/)
- Quarto Documentation: https://quarto.org/docs/guide/
- Quarto Multi-format Discussion: https://github.com/orgs/quarto-dev/discussions/1751
