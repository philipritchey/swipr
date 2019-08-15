# swipr-attendence
id scanner for taking attendance

## Basic Usage
./id_scanner.py to start the program
scan a student ID to log attendance.  new IDs prompt for UIN.
new UINs prompt for name.
scan an admin ID (admin IDs are hardcoded right now) to enter admin mode.
close terminal or enter admin mode (and type exit or quit) to end the program.

## Admin Mode
can exit/quit to end program
can test to see what data is on a mag stripe.
any unrecognized command (including empty) returns to main loop.

## TAMU IDs
TAMU ID has an arbitraily chosen number written 3 times on the stripe.
ID number and UIN must be manually linked, e.g. at first scan.
