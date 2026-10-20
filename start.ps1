# Windows 默认经已有 Ubuntu WSL 启动；原生 Ruby 也可直接使用 bundle 命令。
param([int]$Port = 4000, [string]$Distribution = 'Ubuntu')
$ErrorActionPreference = 'Stop'
$linuxProject = (& wsl.exe -d $Distribution --exec wslpath -a $PSScriptRoot).Trim()
if ($LASTEXITCODE -ne 0) { throw '无法解析 WSL 项目路径，请确认 Ubuntu 已安装。' }
& wsl.exe -d $Distribution --exec env "PORT=$Port" bash "$linuxProject/start.sh"
exit $LASTEXITCODE
