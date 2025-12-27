# Copilot Instructions for win Repository

This document provides essential guidelines for GitHub Copilot when working on the "What If?" lecture notes repository. The project is a Quarto book that renders to both HTML and RevealJS formats.

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

### Key Dependencies

The project uses packages including:
- `knitr`, `rmarkdown` - document rendering (via Quarto)
- Additional packages as needed for causal inference examples

## Build, Test, and Lint Commands

### Building the Book

```bash
# Preview the book locally (with live reload)
quarto preview

# Render the entire book (both HTML and RevealJS formats)
quarto render

# Render a specific chapter
quarto render chapters/01-introduction.qmd

# Render only HTML format
quarto render --to html

# Render only RevealJS slides
quarto render --to revealjs
```

### Output Structure

After rendering, you'll find:
- `_book/index.html` - HTML book homepage
- `_book/chapters/01-introduction.html` - HTML chapter pages
- `_book/chapters/01-introduction-slides.html` - RevealJS slide presentations

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
- Configuration in `_quarto.yml`
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
├── _book/                      # Generated output (gitignored)
├── .quarto/                    # Quarto cache (gitignored)
├── index.qmd                   # Book homepage
├── _quarto.yml                 # Quarto book configuration (dual-format)
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

Each `.qmd` file should have YAML front matter:

```yaml
---
title: "Chapter Title"
---
```

### Format-Specific Content

Use conditional visibility to create different content for HTML and RevealJS:

```markdown
## Section Title

::: {.content-visible when-format="html"}
Detailed explanations and comprehensive content for book format.
Multiple paragraphs, in-depth examples, full mathematical derivations.
:::

::: {.content-visible when-format="revealjs"}
### Concise Points

- Bullet point summaries
- Key concepts only
- Slide-optimized presentation

::: {.fragment}
Progressive reveal elements
:::
:::
```

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

1. **publish.yml**: Builds and publishes the Quarto book to GitHub Pages
   - Runs on push to main branch
   - Uses Quarto actions to render and deploy
   - Outputs to `_book/` directory
2. **preview.yml**: Generates preview of the book for pull requests
   - Uses PR preview action to deploy to separate preview URL
   - Allows reviewers to see rendered changes
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

### Dual-Format Rendering

**IMPORTANT**: This project uses a dual-format structure where each chapter renders to both HTML and RevealJS.

Key considerations:
- **HTML format**: Detailed, comprehensive book content for reading and study
- **RevealJS format**: Concise, presentation-oriented slides for teaching
- **Content visibility**: Use `.content-visible when-format=` divs to show/hide content based on output format
- **Slide structure**: In RevealJS sections, use `##` for slide titles and `###` for content within slides
- **Progressive reveal**: Use `.fragment` classes for incremental display in slides
- **Output files**: RevealJS uses `{stem}-slides.html` naming pattern (e.g., `01-introduction-slides.html`)

See `DUAL_FORMAT_GUIDE.md` for comprehensive patterns and best practices.

### Data Visualization

- Use ggplot2 for consistency
- Follow tidyverse aesthetic principles
- Include axis labels and titles
- Use appropriate color schemes for accessibility
- Consider how visualizations will appear in both formats (slides may need larger fonts/simpler layouts)

### Making Changes

- When modifying `.qmd` files, ensure code chunks execute successfully
- Run `quarto preview` to verify changes render correctly in both formats
- Check mathematical notation renders properly
- Ensure figures display as intended in both HTML and RevealJS
- Verify cross-references and links work
- Update `_quarto.yml` if adding/removing chapters

### Pull Request Development

**IMPORTANT**: When developing new pull requests, always run `quarto render` to ensure the book can be rendered successfully before finalizing your changes.

- **Always run `quarto render`** during PR development to verify that all changes render correctly
- **CRITICAL**: Test `quarto render` yourself and verify it actually succeeds before claiming success
  - Run the command and wait for it to complete
  - Check the exit code to confirm success (exit code 0)
  - Do not claim success based on partial output or assumptions
  - If the render fails, investigate and fix the issue before proceeding
  - **"Software not installed" is NOT a valid excuse** - install required software (R, Quarto, etc.) first if needed (see Installation section above)
  - **CRITICAL**: When installing R, you MUST use the latest R release from CRAN (see Installation section)
    - **NEVER** use the default R from Ubuntu repositories (e.g., `apt-get install r-base` without adding CRAN repo)
    - The default Ubuntu R is outdated (e.g., R 4.3.3) and will cause issues
    - Always add the CRAN repository first, then install R to get the latest version (R 4.5.2+)
    - Verify the R version with `R --version` before proceeding
- Check that the rendering completes without errors or warnings for both formats
- Review the generated output in the `_book/` directory to ensure quality in both HTML and RevealJS
- Verify that format-specific content appears correctly in each format
- Fix any rendering issues before requesting review
- This practice helps maintain the quality of rendered outputs and streamlines the contribution process
- Note: The CI/CD workflows (preview.yml and publish.yml) will also render the book, but catching issues locally saves time

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
