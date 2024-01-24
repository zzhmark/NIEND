#!/public/home/vkzohj/bin/bash

vaa3d=/PBshare/SEU-ALLEN/Users/zuohan/vaa3d_for_neutube/start_vaa3d.sh

in_dir=psf_post
out_dir=psf_app2

running_jobs=0

mkdir -p $out_dir
for in_file in `ls $in_dir/*.v3dpbd`; do
    outfile=$out_dir/`basename $in_file .v3dpbd`.swc
    [ -f $outfile ] && continue
    marker=manual_marker/`basename $in_file`.marker
    [ -f $marker ] || marker=1024.marker
    
    srun --mem=1000 bash -c "
        echo $in_file
        xvfb-run -a $vaa3d -x vn2 -f app2 -i $in_file -o $outfile -p \
        $marker 0 AUTO 0 1 0 0 5 > /dev/null
    " &

    ((running_jobs++))

    if ((running_jobs >= 600)); then
        wait -n
        ((running_jobs--))
    fi
done

wait