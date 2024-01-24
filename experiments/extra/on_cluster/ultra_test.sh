vaa3d=/PBshare/SEU-ALLEN/Users/zuohan/vaa3d/start_vaa3d.sh

wkdir=/PBshare/SEU-ALLEN/Users/zuohan/trans/rectify_1891

cp niend_ut.marker 17302_15030_27059_4032_ut.marker
xvfb-run -a $vaa3d -x ultra -f trace_APP2_GD -i \
    $wkdir/17302_15030_27059_4032_niend/'RES(2048x2048x256)' -p \
    17302_15030_27059_4032_ut.marker 512 0 1 0 0 0 0
rm 17302_15030_27059_4032_ut.marker
