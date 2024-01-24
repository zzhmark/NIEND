#!/public/home/vkzohj/bin/bash

in_dir=/PBshare/SEU-ALLEN/Users/zuohan/trans/crop1891/1st
python=~/.conda/envs/230k/bin/python

running_jobs=0
out_dir=psf
mkdir -p $out_dir
for in_file in `ls $in_dir/*`; do
    srun --mem=10000 bash -c "
        echo $in_file
        $python psf.py $in_file $out_dir
    " &

    ((running_jobs++))
    
    if ((running_jobs >= 400)); then
        wait -n
        ((running_jobs--))
    fi
done

wait