num_passes=5

models=(
    inceptionv3
    resnext50
    bert
    nasrnn
    nasnet_a
)

for model in "${models[@]}"; do
    for pass in $(seq 0 $(expr $num_passes - 1))
    do
        python "$model".py --result_file "$model"_time.txt
        cat timer.txt >> "$model"_stats.txt
    done
done

models=(
    squeezenet
    vgg19-7
)

for model in "${models[@]}"; do
    for pass in $(seq 0 $(expr $num_passes - 1))
    do
        python test_onnx.py --file "$model".onnx --result_file "$model"_time.txt
        cat timer.txt >> "$model"_stats.txt
    done
done
