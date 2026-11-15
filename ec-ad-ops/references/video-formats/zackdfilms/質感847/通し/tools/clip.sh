#!/bin/zsh
# クリップを1本作る（Higgsfield kling_o3_flf・pro・音なし）。clip.sh <版 847_B|849_D> <名前> <始めの絵> <終わりの絵> <秒 3|4|5> <指示の文> <両方の版で合わせた上限>
# → クリップ/<版>/<名前>.mp4 。値段は higgsfield generate cost で確かめた数（3秒 3.75・4秒 5・5秒 6.25）。上限をこえる時は打たない。
R=${0:a:h:h}/クリップ; D=$R/$1; n=$2; mkdir -p $D
used=$(awk '{s+=$4} END{print s+0}' $R/credits.log 2>/dev/null); c=$(python3 -c "print({3:3.75,4:5.0,5:6.25}[$5])")
python3 -c "import sys; sys.exit(0 if $used+$c<=$7 else 1)" || { echo "上限をこえる $used+$c"; exit 1; }
echo "$1 $n ${5}s $c" >> $R/credits.log
cp $6 $D/$n.prompt.txt
higgsfield generate create kling_o3_flf --prompt "$(cat $6)" --start-image $3 --end-image $4 --aspect_ratio 9:16 --duration $5 --mode pro --sound off --multi_shots false --wait --wait-timeout 15m --wait-interval 10s > $D/$n.log 2>&1
u=$(/usr/bin/grep -oE 'https://[^" ]+\.mp4[^" ]*' $D/$n.log | tail -1); [ -n "$u" ] && curl -sL -o $D/$n.mp4 "$u"
echo "$(date +%H:%M:%S) $1 $n $5s $( [ -f $D/$n.mp4 ] && echo できた || echo 無い )" >> $R/clips.log
