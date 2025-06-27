#!/usr/bin/env bash
set -e
mkdir -p bin
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar -xJ
mv ffmpeg-*-static/ffmpeg ./bin/ffmpeg
mv ffmpeg-*-static/ffprobe ./bin/ffprobe
chmod +x ./bin/ffmpeg ./bin/ffprobe
export PATH="$(pwd)/bin:$PATH"
