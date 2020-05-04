#!/bin/bash
path1='/Users/jia/Desktop/covert_attack/WebGLSamples.github.io/aquariumFPSdata/'
files=`ls -t $path1`
for file1 in $files
do
    break;
done

path2='data/'
files=`ls -t $path2`
for file2 in $files
do
    break;
done

echo $file1
echo $file2

python set.py  $path1$file1 $path2$file2