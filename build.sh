#!/usr/bin/env bash


echo "Disabling tput error..."
touch /home/render/colors.sh
echo '#!/bin/sh' > /home/render/colors.sh
echo 'exit 0' >> /home/render/colors.sh

set -eo pipefail
tput setaf 2 || true
apt update && apt install -y ncurses-bin

# Установка ffmpeg для moviepy
mkdir -p bin
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJ
mv ffmpeg-*-static/ffmpeg ./bin/ffmpeg
mv ffmpeg-*-static/ffprobe ./bin/ffprobe
chmod +x ./bin/ffmpeg ./bin/ffprobe

# Обновление PATH
export PATH="$(pwd)/bin:$PATH"
