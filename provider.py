name: Update Playlist

on:
  workflow_dispatch:
  schedule:
    - cron: "0 */6 * * *"

permissions:
  contents: write

concurrency:
  group: update-playlist
  cancel-in-progress: false

jobs:
  update:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
          cache-dependency-path: requirements.txt

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Generate playlist
        run: python provider.py

      - name: Check for changes
        id: changes
        run: |
          git add rutv2.m3u

          if git diff --cached --quiet; then
            echo "changed=false" >> $GITHUB_OUTPUT
          else
            echo "changed=true" >> $GITHUB_OUTPUT
          fi

      - name: Commit changes
        if: steps.changes.outputs.changed == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

          git commit -m "Update playlist $(date -u '+%Y-%m-%d %H:%M UTC')"
          git push

      - name: No changes
        if: steps.changes.outputs.changed == 'false'
        run: echo "Playlist already up to date"
