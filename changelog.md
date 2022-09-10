# ✨ Rin Commands API v0.2.0 ✨

Adds a new release workflow, and patches issues with CORS and dependency bumps.

## 🛠️ Changes

- Fix CORS issues
- Condense and merge Docker build workflows back into 2 workflows instead of 4
- Bump Python to 3.10.7 within both Alpine and Debian Docker images

## ✨ Additions

- Add new release workflow (to automatically tag a new release, and build the docker images as needed)
- Use Renovate for dependency management and upgrades

## ➖ Removals

## ⬆️ Dependency Updates

- Update python Docker tag to v3.10.7 (@renovate)
- Update dependency fastapi to ^0.82.0 (@renovate)
- Update actions/checkout action to v3 (@renovate)