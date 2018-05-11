for i in {1..75}
do
  for ((i=1;i<=5;i+=1));
  do
  temp=$[(100 + (RANDOM % 100))]$[1000 + (RANDOM % 1000)]
  v[i-1]=0.${temp:1:2}${temp:4:3}
  done
echo -n ${v[@]} >> results.txt
python referee_changed.py player player
echo "" >> results.txt
sleep 5
done
