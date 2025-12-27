# What If: Causal Inference Lecture Notes

Lecture notes and slides based on ["What If" by Miguel Hernán and James Robins](https://miguelhernan.org/whatifbook)

## Overview

This repository contains a Quarto website with:

- **HTML Lecture Notes**: Detailed written materials covering causal inference concepts
- **RevealJS Slides**: Presentation slides for each lecture topic

## Topics Covered

1. **Introduction to Causal Inference**
   - Causal effects and counterfactuals
   - The fundamental problem of causal inference
   - Association vs. causation
   - Exchangeability and randomization

2. **Randomized Experiments**
   - Randomization schemes (simple, stratified, block)
   - Intention-to-treat analysis
   - Non-compliance and instrumental variables
   - Limitations of randomization

3. **Observational Studies**
   - Confounding and identification assumptions
   - Adjustment methods (stratification, matching, regression)
   - Propensity scores and inverse probability weighting
   - Selection bias and directed acyclic graphs

## Building the Website

### Prerequisites

Install [Quarto](https://quarto.org/docs/get-started/):

- **macOS/Linux**: Download from [quarto.org/download](https://quarto.org/docs/download/)
- **Windows**: Download installer from [quarto.org/download](https://quarto.org/docs/download/)

Or via package managers:

```bash
# macOS
brew install quarto

# Ubuntu/Debian
sudo apt-get install quarto

# Windows (with Chocolatey)
choco install quarto
```

### Build Commands

```bash
# Preview the website locally (with live reload)
quarto preview

# Render the website to _site directory
quarto render

# Render only HTML pages
quarto render --to html

# Render only RevealJS slides
quarto render --to revealjs
```

### Project Structure

```
.
├── _quarto.yml              # Main configuration file
├── index.qmd                # Home page
├── styles.css               # Custom CSS styles
├── lectures/                # HTML lecture notes
│   ├── 01-introduction.qmd
│   ├── 02-randomized-experiments.qmd
│   └── 03-observational-studies.qmd
└── slides/                  # RevealJS presentation slides
    ├── 01-introduction.qmd
    ├── 02-randomized-experiments.qmd
    └── 03-observational-studies.qmd
```

## Viewing the Website

After running `quarto render`, the website will be in the `_site` directory. You can:

1. **Open locally**: Open `_site/index.html` in your browser
2. **Serve locally**: Run `quarto preview` for a local server
3. **Deploy**: Deploy the `_site` directory to any static hosting service (GitHub Pages, Netlify, etc.)

## Navigation

- Use the navbar at the top to navigate between sections
- **Lectures** menu: Access detailed HTML notes
- **Slides** menu: Access RevealJS presentations
- **Home**: Return to the main page

## Resources

- [Book Website](https://miguelhernan.org/whatifbook)
- [Quarto Documentation](https://quarto.org/docs/guide/)
- [RevealJS Documentation](https://quarto.org/docs/presentations/revealjs/)

## License

Based on the freely available textbook "Causal Inference: What If" by Miguel Hernán and James Robins.
