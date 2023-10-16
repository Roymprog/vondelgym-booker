__version__="0.0.2"

from multiprocessing import Pool

from vondel.user import User
import logging


def run(email: str, password: str) -> None:
  logger = logging.getLogger()

  user = User()

  if not user.jwt:
    user.login(email=email, password=password)

    wanted = user.get_wanted_classes_from_vondelgym_oost()

  with Pool(4) as p:
    for response in p.map(user.book_class, wanted):
      logger.info(f"Response: {response.status_code} {response.text}")


