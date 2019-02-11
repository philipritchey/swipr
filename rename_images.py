import os
import sys

if len(sys.argv) < 4:
    path_to_photos = input('path to photos: ')
    photo_prefix = input('photo prefix: ')
    path_to_roster = input('path to roster: ')
else:
    path_to_photos = sys.argv[1]
    photo_prefix = sys.argv[2]
    path_to_roster = sys.argv[3]


#LAST NAME,FIRST NAME,MID NAME,UIN,TNUMBER,EMAIL,CLASSIFICATION,CLASSCODE,CREDITS,MAJOR,MIDTERM REQUIRED,DEGREE CANDIDATE,ABSENCES,MIDTERM,FINALGRADE,UPDATEDFINALGRADE
uin = list()
with open(path_to_roster) as f:
    for line in f:
        student = line.strip().split(',')
        uin.append(student[3])
# delete headers
uin = uin[1:]

photo_path = path_to_photos+"/"+photo_prefix
for i in range(len(uin)):
    if i > 0:
        old = photo_path+"("+str(i)+").display"
    else:
        old = photo_path+".display"
    new = path_to_photos+"/"+uin[i]+".jpeg"
    print('renaming',old,'->',new)
    os.rename(old, new)
