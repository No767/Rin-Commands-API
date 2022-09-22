# 🛠️ Rin Commands API v0.3.2 🛠️

This update fixes many issues after noticing that there were issues when the frontend was deployed to prod. By removing the rate limiter, this means that the prometheus metrics should start working again, and the frontend won't get spammed w/ 429 errors
## 🛠️ Changes

- List all commands w/ `ASC` order by `name`
## ✨ Additions

## ➖ Removals

- Completely remove the rate limiter like for the 15th time already

## ⬆️ Dependency Updates

