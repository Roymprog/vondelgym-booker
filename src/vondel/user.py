import logging
import requests


class User:
  gymly_domain = "https://prod-dot-gymly-337710.ew.r.appspot.com"
  vondelgym_id = "077049ba-b02f-4e2d-a74f-089a4bb82fa7"


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

  def book_class(self, clazz: dict):
    registration_id = clazz["id"]
    start_time = clazz["date"]
    self.logger.info(f"Trying to book: {registration_id} at {start_time}")

    headers = {
      'authorization': f'Bearer {self.jwt}',
      'content-type': 'application/json',
    }

    json_data = {
      'date': start_time,
    }

    response = requests.post(
      f'{self.gymly_domain}/api/v1/courses/{registration_id}/subscribe',
      headers=headers,
      json=json_data,
    )

    return response

  def get_wanted_classes_from_vondelgym_oost(self, page: int = 1, classes = []):
    """Returns a list of ids of classes that are in the waiting list of user belonging to jwt"""
    url = f"{self.gymly_domain}/api/v1/businesses/{self.vondelgym_id}/courses/waitlist"
    headers = {
      'content-type': 'application/json',
      'authorization': f'Bearer {self.jwt}',
    }

    params = {
      'size': '10',
      'page': f'{page}',
    }

    json = requests.get(
      url,
      params=params,
      headers=headers,
    ).json()

    # API always only returns 3 results, so we need to loop through the pages
    if json["totalPages"] >= page:
      return self.get_wanted_classes_from_vondelgym_oost(page + 1, json["content"] + classes)
    else:
      return [{"id": clazz["id"], "date": clazz["startAt"]} for clazz in classes]
