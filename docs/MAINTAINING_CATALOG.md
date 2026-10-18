# Maintaining the repository catalog

The repository catalog is an index of upstream GitHub projects. It does not copy source code, notebooks, slides, or datasets from those projects.

## Regenerate catalog files

Use Python 3 from the repository root:

```bash
python3 scripts/build_catalog.py
```

The script refreshes `data/repos.json`, `data/repos.csv`, `CATALOG.md`, and the ten grouped lists in `resources/00-*.md` through `resources/09-*.md`. It leaves the project README, site, and curriculum guides unchanged.

To add or update an entry, edit the `REPOS` list in `scripts/build_catalog.py`, then regenerate the catalog. Preserve the source URL and repository owner; use repository metadata for the description, language, star count, last update, and archived flag. Star counts and other metadata should include an as-of date.

## Review before publishing

- Confirm the repository URL resolves and the project is relevant to AI learning or bootcamp practice.
- Check category fit and whether the repository is archived.
- Keep descriptions factual and concise; do not imply review or endorsement.
- Do not copy third-party files. If a later change imports any material, check its current license, preserve required notices, and document the source.
- Run the generator and confirm its printed repository/category totals match the expected snapshot.
- Open a pull request with a short explanation of the changes.
