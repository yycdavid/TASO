num_passes=2
for pass in $(seq 0 $(expr $num_passes - 1))
do
    python bert.py --result_file bert_time.txt
done