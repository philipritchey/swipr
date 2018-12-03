"""
scan TAMU student ID cards and TX driver's licences
for attendance taking
"""

import time
import getpass

ADMIN_ID = '6016426592443531'
STUDENT_ID = '60'
TX_DL = 'TX'

def admin() -> None:
    """
    access admin functions
    """

    action = input('> ')
    if action.lower() in ['exit', 'quit']:
        print('exiting...')
        exit(1)
    print('nothing happened...')

def main() -> None:
    """
    main loop for ID scanning
    """

    with open('swipe_log', 'at') as swipe_log:
        while True:
            # scan ID
            id_data = getpass.getpass('swipe ID...')
            id_type = id_data[1:3]
            if id_type == STUDENT_ID:
                # student ID
                id_num = id_data[1:17]
                event = '{:.4f}\t{:s}'.format(time.time(), id_num)
                print(event)
                swipe_log.write(event + '\n')
                if id_num == ADMIN_ID:
                    admin()
            elif id_type == TX_DL:
                # Texas driver's license
                id_name = ' '.join(id_data[16:].split('^')[0].split('$')[::-1])
                event = '{:.4f}\t{:s}'.format(time.time(), id_name)
                print(event)
                swipe_log.write(event + '\n')
                if id_name == 'PHILIP RITCHEY':
                    admin()

if __name__ == '__main__':
    main()
