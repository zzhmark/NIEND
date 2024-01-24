#!/public/home/vkzohj/bin/bash

vaa3d=/PBshare/SEU-ALLEN/Users/zuohan/vaa3d_for_neutube/start_vaa3d.sh

in_dirs=(my guo_enh_8 multiscale adathr8 1st_8bit)
out_dirs=(niend_gps guo_gps multi_gps ada_gps raw_gps)

running_jobs=0
for i in `seq 0 4`; do
    mkdir -p ${out_dirs[$i]}
    for in_file in `ls ${in_dirs[$i]}/*`; do
        outfile=${out_dirs[$i]}/`basename ${in_file}_NeuroGPSTree.swc`
        [ -f $outfile ] && continue
        srun --cpus-per-task=4 bash -c "
            echo $in_file
            xvfb-run -a $vaa3d -x HUST -f tracing_func -i $in_file -p \
            0.25 0.25 1 6 0 100 gps_soma.swc 4 > /dev/null
            mv ${in_file}_NeuroGPSTree.swc ${out_dirs[$i]}/
        " &

        ((running_jobs++))

        if ((running_jobs >= 200)); then
            wait -n
            ((running_jobs--))
        fi
    done

done

wait