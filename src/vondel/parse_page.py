from typing import Union
from bs4 import BeautifulSoup
import requests
from itertools import chain
from vondel.classes import Class, Desired_class
from vondel.utils import *

def class_has_res_activities_class(tag: BeautifulSoup):
  return tag.has_attr('class') and 'res_activities' in tag.get_attribute_list('class')

def class_has_res_days_class(tag: BeautifulSoup):
  return tag.has_attr('class') and 'res_days' in tag.get_attribute_list('class')

def class_has_status_class(tag: BeautifulSoup):
  """Element having 'status' means it is in notifications"""
  return tag.has_attr('class') and 'status' in tag.get_attribute_list('class')

def span_has_sp_time_class(tag: BeautifulSoup):
  return tag.name == 'span' and 'sp_time' in tag.get_attribute_list('class')

def span_has_available_class(tag: BeautifulSoup):
  return tag.name == 'span' and 'available' in tag.get_attribute_list('class')

def div_has_res_name_class(tag: BeautifulSoup):
  return tag.name == 'div' and 'res_name' in tag.get_attribute_list('class')

def div_has_res_reserve_class(tag: BeautifulSoup):
  return tag.name == 'div' and 'res_reserve' in tag.get_attribute_list('class')

def a_has_cancel_class(tag: BeautifulSoup):
  return tag.name == 'a' and 'cancel' in tag.get_attribute_list('class')

def span_has_date_dd(tag: BeautifulSoup):
  return tag.name == 'span' and 'date_dd' in tag.get_attribute_list('class')

def span_has_date_first(tag: BeautifulSoup):
  return tag.name == 'span' and 'date_first' in tag.get_attribute_list('class')

def span_has_pli_time(tag: BeautifulSoup):
  return tag.name == 'span' and 'pli_time' in tag.get_attribute_list('class')

def get_class_info(div):
  time_div = div.find(span_has_sp_time_class)
  start_time, end_time = start_and_end_time(time_div.text)
  availability_div = div.find(span_has_available_class)
  [signed_up, capacity] = list(map(lambda x: int(x), availability_div.text.split('/')))
  class_type = div.find(div_has_res_name_class).text.split(' ')[0]
  registration_id = div.find(div_has_res_reserve_class).a['id'].split('_')[1] if (div.find(div_has_res_reserve_class).a) else None 
  is_booked = div.find(a_has_cancel_class) != None

  return Class(registration_id, start_time, end_time, capacity, signed_up, class_type, is_booked)

def get_classes_from_days(soup: BeautifulSoup):
  def set_day_and_month(clazz: Class, day: int, month: int):
    clazz.day = day
    clazz.month = month
    return clazz

  day, month = get_day_and_month(soup)

  classes_divs = soup.find_all(class_has_res_activities_class)
  classes = list(map(get_class_info, classes_divs))

  return [set_day_and_month(clazz, day, month) for clazz in classes]

def get_day_and_month(div):
  [day, month] = div.find(span_has_date_dd).text.split(' ')
  return int(day), month_to_int(month)

def get_classes(soup: BeautifulSoup):
  result = [get_classes_from_days(day_div) for day_div in soup.find_all(class_has_res_days_class)]
  return list(chain.from_iterable(result))

def get_classes_from_vondelgym_oost(session_id: Union[str, None] = None):
  headers = {}
  if session_id:
    session_id_cookie = f'_mysportpages_session_id_={session_id}'
    headers['Cookie'] = session_id_cookie

  html =  requests.get(
    'https://vondelgym.nl/lesrooster-vondelgym-oost?resource_type_id=1495',
    headers=headers
  ).text

  return get_classes(BeautifulSoup(html, "html.parser"))

def get_class_from_notification(div: BeautifulSoup):
  date_text_split = div.find(span_has_date_first).text.split('-')
  day = int(date_text_split[0])
  month = int(date_text_split[1])
  start_time_text = div.find(span_has_pli_time).text
  start_time, _ = start_and_end_time(start_time_text)

  return Desired_class(start_time, day, month)

def get_wanted_classes(soup: BeautifulSoup):
  return [get_class_from_notification(desired_class_div) for desired_class_div in soup.find_all(class_has_status_class)]

def get_wanted_classes_from_vondelgym_oost(session_id: Union[str, None] = None):
  headers = {}
  session_id_cookie = f'_mysportpages_session_id_={session_id}'
  headers['Cookie'] = session_id_cookie

  html =  requests.get(
    'https://vondelgym.nl/profiel-lesinschrijvingen',
    headers=headers
  ).text

  return get_wanted_classes(BeautifulSoup(html, "html.parser")) 