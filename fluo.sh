#!/bin/bash

func=""

S0=
S1=

template="template_fluo.inp"
op=_HT_fluo
sed -e "s/FUNC/$func/g"   $template > $op.inp
sed -i "s/groundstate.hess/$S0.hess/g" $op.inp
sed -i "s/singletstate.hess/$S1.hess/g" $op.inp
sed -i "s/* XYZFILE 0 1/* XYZFILE 0 1 $S0.xyz/g" $op.inp
ORCA-submission -n $op -m 360 -esd -c 12
# qsub $op.sh



