from datetime import datetime

def load_roster(filename):
  name = dict()
  line_no = 0
  with open(filename) as f:
    for line in f:
      line_no += 1
      try:
        values = line.split()
        uin = values[-1]
        last = values[0]
        first = ' '.join(values[1:-1])
      except (ValueError, IndexError) as err:
        print(err)
        print('at line {}'.format(line_no))
        break
      if uin in name and not (first == name[uin]['first'] and last == name[uin]['last']):
        print('[WARNING] {} already exists, replacing with new value'.format(uin))
        print('  old: {} {}'.format(name[uin]['first'], name[uin]['last']))
        print('  new: {} {}'.format(first, last))
        #c = input('replace? (y/n) ')
        #if c == 'n':
        #    continue
      else:
        name[uin] = dict()
      name[uin]['first'] = first;
      name[uin]['last'] = last
  return name

def split_on_comma_or_whitespace(line):
  if ',' in line:
    values = line.strip().split(',')
  else:
    values = line.strip().split()
  return values

def load_swipe_log(filename):
  attendance = dict()
  for line in open(filename):
    values = split_on_comma_or_whitespace(line)
    time = float(values[0])
    uin = values[-1].strip()
    date = str(datetime.fromtimestamp(time)).split()[0]
    if date not in attendance:
      print('processing attendance on {}'.format(date))
      attendance[date] = set()
    #if uin not in attendance[date]:
    #    print('marked {} present on {}'.format(uin, date))
    attendance[date].add(uin)
  return attendance

def compute_attendance(name, attendance, filename='attendance.csv'):
  print('writing attendance data to "{}"...'.format(filename))
  with open(filename,'wt') as f:
    f.write('last,first,uin,{},total\n'.format(','.join(date for date in sorted(attendance))))
    f.write('\n'.join('{},{},{},{},{}'.format(name[uin]['last'], name[uin]['first'], uin, ','.join(str(uin in attendance[date]) for date in sorted(attendance)), sum(int(uin in attendance[date]) for date in sorted(attendance))) for uin in sorted(name)))
    f.write('\n')
  print('done.')

def main():
  name = load_roster('roster')
  attendance = load_swipe_log('swipe_log')
  compute_attendance(name, attendance)

if __name__ == '__main__':
  main()
