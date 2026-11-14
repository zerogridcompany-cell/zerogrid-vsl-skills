#!/bin/zsh
# クリップを1秒6コマで並べる。clipsheet.sh <場面> → work/check/<場面>.jpg
W=${ZG_WORK:-$PWD}; s=$1; mkdir -p $W/work/check   # アプリ：作業フォルダ（ZG_WORK）
src=$W/クリップ/847/$s.mp4; for d in "$W/クリップ/847" "$W/クリップ" "$EC_ROOT/$ZG_PRODUCT/07_納品/動画/クリップ"; do [ -f "$d/$s.mp4" ] && { src="$d/$s.mp4"; break; }; done
ffmpeg -v error -y -i "$src" -vf "fps=6,scale=196:294,tile=8x4:padding=2" -frames:v 1 $W/work/check/$s.jpg
echo $W/work/check/$s.jpg
