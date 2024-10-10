#!/bin/bash

opt=$1
S0=$2
T1=$3
Energy1=`grep "Electronic energy " $S0.out | awk '{print $4}'`
Energy2=`grep "Electronic energy " $T1.out | awk '{print $4}'`
DEnergyT1=$(echo "($Energy2 - $Energy1) * 219474.6" | bc)
DiffEnergyT1=$(echo "($DEnergyT1 + 0.5) / 1" | bc) 

 echo "T1 - S0 = " $DEnergyT1

   for i in 1 2 3; do
   local op="${1%.inp}_T$i"  
     sed -e "s/IROOT/IROOT $i/g" $1 > $op.inp
     sed -i "s/DELE/DELE $DiffEnergyT1/g" $op.inp
     sed -i "s/groundstate.hess/$S0.hess/g" $op.inp
     sed -i "s/tripletstate.hess/$T1.hess/g" $op.inp
     sed -i "s/* XYZFILE 0 1/* XYZFILE 0 1 $S0.xyz/g" $op.inp

   done

