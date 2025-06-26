#!/usr/bin/env bash

set -e  # Остановить при ошибке

curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar xJ
mv ffmpeg-*-static/ffmpeg /usr/local/bin/ffmpeg
mv ffmpeg-*-static/ffprobe /usr/local/bin/ffprobe
