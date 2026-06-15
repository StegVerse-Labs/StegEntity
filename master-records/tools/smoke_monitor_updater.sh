#!/usr/bin/env bash
set -eu

python master-records/tools/monitor_updater_min.py \
  --task-id 2026-06-14-site-exchange-pages \
  --state waiting \
  --target-repo StegVerse-Labs/Site \
  --org-percent 30 \
  --repo-percent 64
