#!/public/home/vkzohj/bin/bash

vaa3d=/PBshare/SEU-ALLEN/Users/zuohan/vaa3d_for_neutube/start_vaa3d.sh

in_dirs=(my guo_enh_8 multiscale adathr8 1st_8bit)
out_dirs=(niend_app1 guo_app1 multi_app1 ada_app1 raw_app1)

running_jobs=0
for i in `seq 2 4`; do
    mkdir -p ${out_dirs[$i]}
    for in_file in `ls ${in_dirs[$i]}/*`; do
        outfile=${out_dirs[$i]}/`basename ${in_file}_app1.swc`
        [ -f $outfile ] && continue
        marker=manual_marker/`basename $in_file`.marker
        [ -f $marker ] || marker=1024.marker
        srun --mem=15000 -p normal bash -c "
            echo $in_file
            xvfb-run -a $vaa3d -x vn2 -f app1 -i $in_file -o $outfile -p \
            $marker 0 AUTO 0 > /dev/null
        " &

        ((running_jobs++))

        if ((running_jobs >= 600)); then
            wait -n
            ((running_jobs--))
        fi
    done

done

wait