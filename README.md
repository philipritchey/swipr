# swipr
id scanner for taking attendance

## Updates
run `git pull` to update.

## Basic Usage
1. `./id_scanner.py` to start the program
1. scan a student ID to log attendance.
   * new IDs prompt for UIN.
   * new UINs prompt for name.
1. scan an admin ID (admin IDs are hardcoded right now) to enter admin mode.
1. end the program.
   * use admin `exit` or `quit`.
   * close terminal (not suggested, but probably OK)

## Admin Mode
admin users can swipe in to access these functions: 
* exit/quit to end program
* test to see what data is on a mag stripe
* rename students on roster

any unrecognized command (including empty) returns to main loop.

## TAMU IDs
TAMU ID has an arbitraily chosen number written 3 times on the stripe.
ID number and UIN must be manually linked, e.g. at first scan.

## Importing Images from Howdy
1. Go to https://howdy.tamu.edu
1. Login
1. "Faculty / Teaching" tab
1. "Class Roster and Syllabus" link
1. Select current term, e.g. "Fall 2019 - College Station"
1. For each section:
   1. "view" roster
   1. at bottom of page, "Import Entire Roster into CSV"
       * rename file to course and section ID
         * e.g. 22889.csv --> 121_513.csv
   1. back at top of page, "Image Roster"
   1. "View Entire Roster"
   1. ctrl+s (save)
      * rename file to course and section ID
        * e.g. BWXKPHOTO.html --> 121_513.html
1. Put the image files and the csv files in the same folder
   * e.g. ~/Downloads/image_rosters/
     * 121_513.csv
     * ...
     * 121\_513\_files/
     * ...
     * the .html files are not needed
1. Just in case this script goes awry, make a backup copy of the folder
   1. select image_rosters folder
   1. 2-finger click
   1. "Create Archive..."
1. Add your details to this script (`batch_mode_rename_images.sh`) and execute it:
```bash
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
```
1. Verify that swipr/image has a bunch of jpeg images with UINs for names
1. Verify that swipr/roster has names and UINs
1. It is now safe to delete the image_rosters folder
   * `rm -r ~/Downloads/image_rosters`
