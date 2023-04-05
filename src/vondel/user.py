import re
import requests
import urllib3
from vondel.utils import VONDELGYM_URL
from vondel.parse_page import get_classes_from_vondelgym_oost

class User:
  session_id_regex = re.compile(r"_mysportpages_session_id_=([\w\d]+);")

  @staticmethod
  def read_session_id(text: str):
    """Return the session id from HTML text"""
    return User.session_id_regex.search(text).group(1)

  def __init__(self, session_id: str = None, email: str = None, password: str = None):
    self.email = email
    self.password = password
    self.session_id = session_id

  def login(self, email, password, force=False):
    if not self.session_id or force:

      url = f'{VONDELGYM_URL}/#login'
      files = {}
      files['f[email]'] =  email
      files['f[password]'] = password
      files['f[remember_me]'] = '0'
      files['next_step'] = ''
      files['commit'] = 'Log in'
      files['f[form_id]'] = '19206'

      body, content_type = urllib3.encode_multipart_formdata(files)

      headers = {}
      headers['Content-type'] = content_type
      headers['Origin'] = VONDELGYM_URL
      headers['Referer'] = VONDELGYM_URL

      response = requests.post(
        url,
        headers=headers,
        data=body
      )

      self.session_id = User.read_session_id(response.headers["Set-Cookie"])
  
    return self

  def book_class(self, session_id: str, registration_id: str):
    conf_id_crossfit = '1138'
    resource_type_id= '1495'
    url = f'{VONDELGYM_URL}/cs_reservations/reserve/{registration_id}?conf_id={conf_id_crossfit}'
    session_id_cookie = f'_mysportpages_session_id_={session_id}'
    headers = {}
    headers['Cookie'] = session_id_cookie
    headers['Origin'] = VONDELGYM_URL
    headers['Referer'] = f'https://vondelgym.nl/lesrooster-vondelgym-oost?resource_type_id={resource_type_id}'
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['Content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'

    return requests.post(
      url,
      headers=headers
    )

  def book_class_at(self, start_time: int, day: int, month: int):
    """Expects to be called with a logged in user."""
    # Do this when not logged in to prevent personal identifiable DDoS
    classes = [clazz for clazz in get_classes_from_vondelgym_oost() \
      if clazz.day == day and clazz.month == month and clazz.start_time == start_time and not clazz.is_full() and not clazz.is_booked]

    if len(classes) > 0:
      clazz =   classes = [clazz for clazz in get_classes_from_vondelgym_oost(self.session_id) \
                  if clazz.day == day and clazz.month == month and clazz.start_time == start_time and not clazz.is_full()][0]
      self.book_class(self.session_id, clazz.registration_id)
      print(f"Booked class: {clazz}")
    else:
      print(f"No spot found in for start time: {start_time}:00 at {day}/{month}.")
