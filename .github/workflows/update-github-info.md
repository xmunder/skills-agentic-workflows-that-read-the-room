---
name: update-github-info
engine: copilot
model: gpt-5-mini
on:
  schedule: daily
  workflow_dispatch:

permissions:
  contents: read
  pull-requests: read

tools:
  edit:
  web-fetch:

network:
  allowed:
    - github.blog
    - github.com
    - awesome-copilot.github.com

safe-outputs:
  create-pull-request:
    title-prefix: "[github-info] "
    reviewers: [mona]
    draft: true
    fallback-as-issue: false
    allowed-files:
      - site/content/github-info.md
---

# Update GitHub Info

Keep `site/content/github-info.md` current with concise, practical guidance that helps developers learn GitHub faster.

## Instructions

1. Read `notes/mona-notes.md` and the current `site/content/github-info.md` before making changes.
2. Use `web-fetch` to read https://github.blog/latest/, https://github.blog/changelog/, and https://awesome-copilot.github.com/workflows/.
3. Identify recent items that are useful for the site's existing themes. Verify dates, titles, and details from the fetched pages; do not infer facts that the sources do not state.
4. Update only `site/content/github-info.md`. Keep summaries short and practical, preserve the site's existing structure, and link each new item to its GitHub Blog, Changelog, or Awesome Copilot workflows source.
5. Review the diff for accuracy, clarity, duplicate items, and unintended file changes.
6. When there is a meaningful update, use the `create-pull-request` safe output to open a draft pull request requesting review from Mona. Explain the changes and cite the source links in the pull request description. Do not write directly to the default branch.
7. If the sources contain no meaningful new information, leave the content unchanged and do not create an empty pull request.
