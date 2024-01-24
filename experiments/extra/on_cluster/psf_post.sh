#!/public/home/vkzohj/bin/bash

in_dir=psf
python=~/.conda/envs/230k/bin/python

running_jobs=0
out_dir=psf_post
mkdir -p $out_dir

for in_file in `ls $in_dir/*`; do
    srun --mem=1000 bash -c "
        echo $in_file
        $python psf_post.py $in_file $out_dir
    " &

    ((running_jobs++))
    
    if ((running_jobs >= 400)); then
        wait -n
        ((running_jobs--))
    fi
done

wait