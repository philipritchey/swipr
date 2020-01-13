#!/bin/bash

username="red"
#username="instructor"

# absolute path to image rosters
pathToImageRosters="/home/$username/Downloads/image_rosters"

# prefix of image files, e.g. "BWXK_GET_PHOTO(1).display"
photoPrefix="BWXK_GET_PHOTO"

# absolute path to swipr/roster
rosterFile="/home/$username/Documents/swipr/roster"

# put your sections in the list {...}
# you can do this for multiple classes, too
#   e.g. {121_{513..520},431_{500..502}}
for class in {121_{521..528},489_502,713_600}
do
    # setup paths arguments
    pathToPhotos="$pathToImageRosters/$class""_files"
    pathToRoster="$pathToImageRosters/$class.csv"
    
    # invoke the python script to rename images
    python3 rename_images.py $pathToPhotos $photoPrefix $pathToRoster

    # copy the images into the swipr/image/ folder 
    for img in "$pathToPhotos/*.jpeg"
    do
        cp $img ./image/
    done
    
    # add names and UINs to swipr/roster file
    echo "adding names and UINs for $class to $rosterFile"
    {
        cut -d, -s -f1,2,4 $pathToRoster | sed '1d' | sed 's/,/\t/g'
    } >> $rosterFile
done

# sort and remove duplicates from swipr/roster
echo "sorting $rosterFile and removing duplicates"
sort $rosterFile | uniq > $rosterFile

echo "Done!"
