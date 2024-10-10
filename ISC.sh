#!/bin/bash

T1=$2
S1=$3

init=$S1
final=$T1
echo "Initial state: " $init
echo "Final state: " $final
Energy1=`grep "Electronic energy " $init.out | awk '{print $4}'`
Energy2=`grep "Electronic energy " $final.out | awk '{print $4}'`
DEnergyT1=$(echo "($Energy1 - $Energy2) * 219474.6" | bc)
DiffEnergyT1=$(echo "($DEnergyT1 + 0.5) / 1" | bc) 

 echo "Energy gap between S1 and T1 = $DiffEnergyT1 cm-1"
 echo "Creating input files for ISC calculation"

  template="template_ISC.inp"
   for i in 1 2 3; do
     op="${1%.inp}_T$i"
     s=$(( $i - 2 ))
     sed -e "s/TROOTSSL/TROOTSSL $s/g" $1 > $op.inp
     sed -i "s/DELE/DELE $DiffEnergyT1/g" $op.inp
     sed -i "s/initial.hess/$init.hess/g" $op.inp
     sed -i "s/tripletstate.hess/$final.hess/g" $op.inp
     sed -i "s/* XYZFILE 0 1/* XYZFILE 0 1 $final.xyz/g" $op.inp
     echo "ISC input file: $op.inp created"
   done

