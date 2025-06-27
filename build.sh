echo '#!/bin/sh' > /home/render/colors.sh || true
echo 'exit 0' >> /home/render/colors.sh || true
#!/usr/bin/env bash
set -eo pipefail

# ✅ Ставим ffmpeg в свою папку
mkdir -p bin
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJ
mv ffmpeg-*-static/ffmpeg ./bin/ffmpeg
mv ffmpeg-*-static/ffprobe ./bin/ffprobe
chmod +x ./bin/ffmpeg ./bin/ffprobe

# ✅ Добавляем ffmpeg в PATH
echo 'export PATH="$(pwd)/bin:$PATH"' >> ~/.profile
export PATH="$(pwd)/bin:$PATH"
