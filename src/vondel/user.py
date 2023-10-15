import logging
import requests


class User:
  gymly_domain = "https://prod-dot-gymly-337710.ew.r.appspot.com"
  vondelgym_id = "077049ba-b02f-4e2d-a74f-089a4bb82fa7"

  @staticmethod
  def read_session_id(text: str):
    """Return the session id from HTML text"""
    return User.session_id_regex.search(text).group(1)

  def __init__(self, jwt: str = None, email: str = None, password: str = None):
    self.email = email
    self.password = password
    self.jwt = jwt
    self.logger = logging.getLogger()

  def login(self, email, password, force=False):
    if not self.jwt or force:

      """Login to Gymly and return the JWT token."""
      gymly_url = f"{self.gymly_domain}/api/v1/user/auth/login"
      self.logger.info("Logging in...")
      response = requests.post(gymly_url, json={"email": email, "password": password})
      if response.status_code != 200:
        raise Exception(f"Could not login: {response.status_code} {response.text}")
      jwt = response.json()["jwt"]
      self.logger.info("Logged in!")
      self.jwt = jwt
  
    return self

  async def book_class(self, jwt: str, registration_id: str, start_time: str):
    headers = {
      'authorization': f'Bearer {jwt}',
      'content-type': 'application/json',
    }

    json_data = {
      'date': start_time,
    }

    return requests.post(
      f'{self.gymly_domain}/api/v1/courses/{registration_id}/subscribe',
      headers=headers,
      json=json_data,
    )

  def get_wanted_classes_from_vondelgym_oost(self):
    """Returns a list of ids of classes that are in the waiting list of user belonging to jwt"""
    url = f"{self.gymly_domain}/api/v1/businesses/{self.vondelgym_id}/courses/waitlist"
    headers = {
      'content-type': 'application/json',
      'authorization': f'Bearer {self.jwt}',
    }

    params = {
      'size': '10',
      'page': '1',
    }

    classes = requests.get(
      url,
      params=params,
      headers=headers,
    ).json()["content"]

    return [{"id": clazz["id"], "date": clazz["startAt"]} for clazz in classes]
