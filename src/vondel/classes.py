class Class(object):
  def __init__(self, registration_id: str, start_time: int, end_time: int, capacity: int, signed_up: int, class_type: str, is_booked: bool = False):
    self.registration_id = registration_id
    self.start_time = start_time
    self.end_time = end_time
    self.capacity = capacity
    self.signed_up = signed_up
    self.class_type = class_type
    self.is_booked = is_booked

  def is_full(self):
    return self.capacity > 0  and self.signed_up >= self.capacity
    
  def __repr__(self):
    return f"""
    'registration_id': {self.registration_id}
    'start_time': {self.start_time}
    'end_time': {self.end_time}
    'capacity': {self.capacity}
    'signed_up': {self.signed_up}
    'class_type': {self.class_type}
    'is_booked': {self.is_booked}
    'day': {self.day if self.day else None}
    'month': {self.month if self.month else None}
    """

class Desired_class:
  def __init__(self, start_time: int, day: int, month: int):
    self.start_time = start_time
    self.day = day
    self.month = month

  def __repr__(self):
    return f"""
    'start_time': {self.start_time}
    'day': {self.day if self.day else None}
    'month': {self.month if self.month else None}
    """