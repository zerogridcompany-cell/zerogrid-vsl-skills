#!/bin/zsh
# 絵を1枚作る（Codex だけ・最大900秒で強制終了）。gen.sh <出す先> <名前> <指示の文のファイル> [見本...]
D=$1; n=$2; p=$3; shift 3; mkdir -p $D
cp $p $D/$n.prompt.txt; printf '%s\n' "$@" > $D/$n.refs.txt; I=()
for f in "$@"; do I+=(-i "$f"); done
st=$(date +%s)
perl -e 'alarm shift; exec @ARGV' ${TMO:-900} ${CODEX_BIN:-codex} exec --skip-git-repo-check -s workspace-write -C $D "Use your image_gen tool to generate exactly ONE image, passing the attached reference images to the image tool in the given order (Image 1 = first attachment, Image 2 = second, ...). $(cat $p) Output: a single vertical 2:3 portrait image. Save it in the current directory with exactly this file name: $n.png. Do not resize, crop or post-process it. Report the absolute path as the last line." "${I[@]}" < /dev/null > $D/run-$n.log 2>&1
rc=$?
echo "$(date +%H:%M:%S) $n $( [ -f $D/$n.png ] && echo OK || echo MISSING ) rc=$rc $(( $(date +%s)-st ))s" >> $D/gen.log
