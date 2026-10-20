#!/usr/bin/env bash
# 从任意工作目录启动本项目；依赖安装在 vendor/bundle。
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if ! command -v bundle >/dev/null; then
  printf '请先安装 Ruby 与 Bundler，参见 README.md。\n' >&2
  exit 1
fi
bundle config set --local path vendor/bundle
bundle check || bundle install
exec bundle exec jekyll serve --host 0.0.0.0 --port "${PORT:-4000}" --baseurl "" --force_polling
