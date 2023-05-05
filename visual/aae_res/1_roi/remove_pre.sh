#!/bin/bash

for file in 000*.png; do
    newfile=$(echo $file | sed 's/^0*//')
    mv $file $newfile
done

