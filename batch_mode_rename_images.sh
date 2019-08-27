#!/bin/bash

# absolute path to image rosters
pathToImageRosters="/home/instructor/Downloads/image_rosters"

# prefix of image files, e.g. "BWXK_GET_PHOTO(1).display"
photoPrefix="BWXK_GET_PHOTO"

# put your sections in the list {...}
# you can do this for multiple classes, too
#   e.g. {121_{513..520},431_{500..502}}
for class in 121_{513..520}
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
    {
        cut -d, -s -f1,2,4 $pathToRoster | sed '1d' | sed 's/,/\t/g'
    } >> /home/instructor/Documents/swipr/roster
done
echo "Done!"
