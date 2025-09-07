#!/bin/bash
uv run jupyter nbconvert --to html notebooks/analysis.ipynb --output ../index.html
git add index.html