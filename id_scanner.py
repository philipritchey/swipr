#! /usr/bin/env python3

"""
scan TAMU student ID cards and TX driver's licences
for attendance taking
"""

import time
import getpass
import signal
import re
import tkinter as tk
import os
from typing import Dict
from PIL import ImageTk, Image
from compute_attendance import main as compute_attendance_main

PHILIP_RITCHEY  = '6016426594150381'
DILMA_DA_SILVA  = '6016426594344166'
MICHAEL_MOORE   = '6016426594018281'
MICHAEL_NOWAK   = '6016426591940362'
CARLOS_FERREIRA = '6016426594344174'

ADMIN_ID = [
    PHILIP_RITCHEY,
    DILMA_DA_SILVA,
    MICHAEL_MOORE,
    MICHAEL_NOWAK,
    CARLOS_FERREIRA,
    ]
TAMU_ID = '60'
TX_DL = 'TX'

SWIPE_LOG = 'swipe_log'
UIN_DICT = 'uin_dict'
ROSTER = 'roster'

UIN_PATTERN = r'^\d{3}00\d{4}$'
TAMU_ID_PATTERN = r'[%;+](\d{16})\?'

# TODO: eliminate globals.  make a class?
w = tk.Tk()
img_not_available = ImageTk.PhotoImage(Image.open(os.path.join('image','no_image_available.jpeg')))
img_ready = ImageTk.PhotoImage(Image.open(os.path.join('image','ready.png')))

def signal_handler(sig, frame) -> None:
    # ignore
    pass

def admin(roster) -> None:
    """
    access admin functions
    """

    print('Admin Commands')
    print('--------------')
    print('exit, quit    exit the program.')
    print('test          echo ID scan data.  press enter to end.')
    print('rename        change a name on the roster.')
    print('\nany unrecognized command returns to main loop\n')

    while True:
        action = input('admin> ').lower()
        if action in ['exit', 'quit']:
            print('(admin) exiting...')
            exit(1)
        elif action in ['test']:
            print('(admin) entering test mode')
            while True:
                try:
                    id_data = getpass.getpass('(admin/test) swipe ID (mag stripe AWAY from LED)...')
                    if len(id_data) == 0:
                        print('<empty>')
                        break
                    else:
                        print(id_data)
                except EOFError:
                    print()
                    continue
            print('(admin/test) exiting test mode')
        elif action in ['rename']:
            uin = get_uin()
            if uin in roster:
                last_name, preferred_name = roster[uin]
                print('(admin/rename) current roster entry: ')
                print('uin           : {}'.format(uin))
                print('last name     : {}'.format(last_name))
                print('preferred name: {}'.format(preferred_name))
                print('"Howdy, {} {}!"'.format(preferred_name, last_name))
            else:
                print('(admin/rename) no roster entry found, will be created')

            preferred_name = input('(admin/rename) preferred first name: ')
            last_name = input('(admin/rename) last name: ')
            roster[uin] = (last_name, preferred_name)
            with open('roster', 'at') as f:
                f.write('{:s}\t{:s}\t{:s}\n'.format(last_name, preferred_name, uin))
            print('"Howdy, {} {}!"'.format(preferred_name, last_name)) 
        else:
            break
    print('(admin) returning to main loop...')

def get_uin() -> int:
    uin = input('Please enter your UIN: ').strip()
    result = re.match(UIN_PATTERN, uin)
    while not result:
        print('Invalid UIN.')
        uin = input('Please enter your UIN: ').strip()
        result = re.match(UIN_PATTERN, uin)
    return result.group(0)

def init_uin_dict() -> Dict:
    uin_dict = dict()
    try:
        with open(UIN_DICT) as uin_dict_file:
            for line in uin_dict_file:
                key, value = line.strip().split(':')
                if key in uin_dict:
                    print('[WARNING] key ({:s}) already exists, replacing old value.'.format(key))
                uin_dict[key] = value
    except FileNotFoundError:
        pass
    return uin_dict

def init_roster() -> Dict:
    roster = dict()
    try:
        with open(ROSTER) as roster_file:
            for line in roster_file:
                last, preferred_name, uin = line.strip().split('\t')
                if uin in roster:
                    print('[WARNING] UIN ({:s}) already exists, replacing old value'.format(uin))
                roster[uin] = (last, preferred_name)
    except FileNotFoundError:
        pass
    return roster

def update_image(img = None):
    global w
    global panel

    panel.image = img
    width = img.width()
    height = img.height()
    x,y=0,0
    w.geometry('{}x{}+{}+{}'.format(width,height,x,y))
    panel.configure(image = img)
    w.update_idletasks()
    w.update()

# TODO: eliminate globals?
def show_img(uin = '000000000', preferred_name = 'PREFERRED NAME', last = 'LAST'):
    global w
    global panel

    w.title(preferred_name + " " + last)
    try:
        update_image(ImageTk.PhotoImage(Image.open(os.path.join('image',uin+'.jpeg'))))
    except FileNotFoundError:
        update_image(img_not_available)
    time.sleep(1)

# TODO: eliminate globals?
def ready():
    global w
    global panel

    w.title('Ready')
    update_image(img_ready)
    
def init_attendance() -> Dict:
    # create attendance.csv
    compute_attendance_main()
    
    attendance = dict()
    max_total = 0
    with open('attendance.csv') as f:
        # eat the header
        f.readline()
        for line in f:
            values = line.split(',')
            uin = values[2]
            total = int(values[-1])
            attendance[uin] = total
    return attendance

def main() -> None:
    """
    main loop for ID scanning
    """

    # read in previous attendance
    attendance = init_attendance()
    max_attendance = max(attendance[uin] for uin in attendance)

    # read in UIN dictionary
    uin_dict = init_uin_dict()

    # read in roster
    roster = init_roster()

    while True:
        # scan ID
        print()
        ready()
        try:
            id_data = getpass.getpass('swipe ID (mag stripe AWAY from LED)...')
            if len(id_data) == 0:
                continue
        except EOFError:
            print()
            continue

        # is it a UIN directly?
        result = re.match(UIN_PATTERN, id_data)
        if result:
            uin = result.group(0)
            id_key = uin
        else:
            id_type = id_data[1:3]
            if id_type == TX_DL:
                # Texas driver's license
                id_key = ' '.join(id_data[16:].split('^')[0].split('$')[::-1])
            else:
                # student/other ID
                result = re.match(TAMU_ID_PATTERN, id_data)
                if not result:
                    print('[ERROR] swipe error, please swipe again.')
                    continue
                id_key = result.group(1)
            if id_key not in uin_dict:
                print('This seems to be the first time this ID has been swiped.')
                uin = get_uin()
                uin_dict[id_key] = uin
                with open(UIN_DICT,'at') as f:
                    f.write('{}:{}\n'.format(id_key, uin))
            else:
                uin = uin_dict[id_key]
        if uin not in roster:
            print('The UIN associated with this ID is not in the roster.')
            print('Please verify your UIN.')
            uin = get_uin()
            uin_dict[id_key] = uin
            with open(UIN_DICT,'at') as f:
                f.write('{:s}:{:s}\n'.format(id_key, uin))
            if uin not in roster:
                preferred_name = input('preferred first name: ')
                last = input('last name: ')
                with open('roster', 'at') as f:
                    f.write('{:s}\t{:s}\t{:s}\n'.format(last, preferred_name, uin))
                roster[uin] = (last, preferred_name)
                # not in roster, so also not in attendance, so need to add
                attendance[uin] = 0
        last, preferred_name = roster[uin]
        event = '{:.4f},{:s},{:s},{:s},{:s}'.format(time.time(), id_key, preferred_name, last, uin)
        with open(SWIPE_LOG, 'at') as swipe_log:
            swipe_log.write(event + '\n')
        print('Howdy, {:s} {:s}! You have {:d} days of swipes ({:.0f}%)'.format(preferred_name, last, attendance[uin]+1, (attendance[uin]+1)/(max_attendance+1)*100))
        show_img(uin, preferred_name, last)
        if id_key in ADMIN_ID:
            admin(roster)

if __name__ == '__main__':
    # ignore SIGINT, SIGTSTP
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTSTP, signal_handler)

    # setup tkinter window
    panel = tk.Label(w)
    panel.pack(side = tk.TOP, fill = tk.BOTH, expand = tk.YES)

    main()
