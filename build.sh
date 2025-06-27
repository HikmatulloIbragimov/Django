#!/usr/bin/env bash
set -eo pipefail

# ⚠️ Fix Render's tput bug
if [ -f /home/render/colors.sh ]; then
  sed -i 's/tput.*/true/' /home/render/colors.sh
fi

# Установка ffmpeg
mkdir -p bin
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJ
mv ffmpeg-*-static/ffmpeg ./bin/ffmpeg
mv ffmpeg-*-static/ffprobe ./bin/ffprobe
chmod +x ./bin/ffmpeg ./bin/ffprobe

# Добавление ffmpeg в PATH
echo 'export PATH="$(pwd)/bin:$PATH"' >> ~/.profile
export PATH="$(pwd)/bin:$PATH"
