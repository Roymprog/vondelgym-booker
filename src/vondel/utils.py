VONDELGYM_URL = 'https://vondelgym.nl'

def start_and_end_time(s):
  """
  Converts time range into start and end integer
  Example:
  '07:00 - 08:00' -> 7, 8
  """
  [start, end] = list(map(lambda x: x.split(':')[0], s.split('-')))
  return (int(start), int(end))
  
def month_to_int(month):
  if month == 'januari':
    return 1
  if month == 'februari':
    return 2
  if month == 'maart':
    return 3
  if month == 'april':
    return 4
  if month == 'mei':
    return 5
  if month == 'juni':
    return 6
  if month == 'juli':
    return 7
  if month == 'augustus':
    return 8
  if month == 'september':
    return 9
  if month == 'oktober':
    return 10
  if month == 'november':
    return 11
  if month == 'december':
    return 12