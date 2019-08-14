grep -i -l "error" logs/Z_boson_pt_* | sed s#logs#../../useful_scripts/scripts#g | sed 's/sh.*/sh/'
grep -i -l "error" logs/Z_boson_pt_* | sed s#logs#../../useful_scripts/scripts#g | sed 's/sh.*/sh/' | tr '\n' ' '
grep -i -l "error" logs/Z_boson_pt_*.err | sed s#logs#../../useful_scripts/scripts#g | sed 's/_26.*err/.sh/g' | tr '\n' ' '
for i in {0..1637};
    if [ ! -f Z_boson_pt_$i.root ]; then
        echo $i
    fi
done;
