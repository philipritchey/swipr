#!/bin/bash

# this is for populating the swipr/roster file AFTER you have already renamed the images
# the updated image renaming script (batch_mode_rename_images.sh) now include this
# put this script in the same place as the .csv roster files
# optionally give it an output filename (default: OUTPUT)
# copy/paste or cat the contents of the output file into the swpr/roster file

if [ $# -gt 0 ]
then
    out=$1
else
    out="OUTPUT"
fi

if [ -f $out ]
then
    echo "ERROR: File \"$out\" exists.  Please remove or rename it."
    exit 1
fi

for csv in *.csv
do
    echo "adding names and UINs from $(basename $csv) to $out"
    {
        cut -d, -s -f1,2,4 $csv | sed '1d' | sed 's/,/\t/g'
    } >> $out
done
