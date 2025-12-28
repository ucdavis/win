# PR Superseded

This PR has been superseded by PR #2 which was merged to main.

The main branch now contains a Quarto book structure with dual HTML/RevealJS rendering, which is the preferred approach.

This PR originally proposed a Quarto website structure with separate lectures and slides directories, but that approach has been replaced.

## Main Branch Structure (Preferred)

The current main branch (as of commit d15105d) contains:
- Quarto book format with `chapters/` directory
- Dual HTML/RevealJS rendering per chapter
- GitHub Actions workflows for publish, preview, spell-check, and lint
- RStudio project file
- Comprehensive documentation in `DUAL_FORMAT_GUIDE.md` and `STRUCTURE_VERIFICATION.md`

## This PR's Original Structure (Deprecated)

This PR proposed:
- Quarto website format
- Separate `lectures/` (HTML) and `slides/` (RevealJS) directories
- Simpler navigation structure

The main branch structure is more flexible and maintainable for the project's needs.
