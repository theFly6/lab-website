#!/usr/bin/env bash
# 上游入口会自动调用旧引文同步器并覆盖数据，本定制站点明确禁用。
printf '%s\n' '该 Docker 入口已弃用：当前站点的 sources.json 是来源注册表，不能交给上游 _cite/cite.py。' >&2
printf '%s\n' '请按 README.md 使用 WSL/Ruby 环境运行 start.sh；本项目未验收 Docker 运行方式。' >&2
exit 2
