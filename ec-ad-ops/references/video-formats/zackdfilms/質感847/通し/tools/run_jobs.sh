#!/bin/zsh
# jobs.tsv を最大3本ずつ並行で回す。run_jobs.sh <回のフォルダ> [名前...]
R=$1; shift; T=${0:a:h}
while IFS=$'\t' read -r n rest; do
  [[ $# -gt 0 && ${@[(Ie)$n]} -eq 0 ]] && continue
  refs=(${(s:	:)rest})
  while (( ${(M)#jobstates:#running:*} >= 3 )); do sleep 5; done
  zsh $T/gen.sh $R $n $R/prompts/$n.txt $refs &
done < $R/jobs.tsv
wait
echo ALLDONE >> $R/gen.log
