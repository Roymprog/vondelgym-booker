__version__="0.0.1"

from vondel.user import User
from vondel.parse_page import get_wanted_classes_from_vondelgym_oost
import logging
import asyncio

def run(email: str, password: str) -> None:
  logger = logging.getLogger()
  user = User()

  user.login(email=email, password=password)

  wanted = get_wanted_classes_from_vondelgym_oost(user.session_id)
  
  logger.info("Found following classes:")

  tasks = []
  for clazz in wanted:
    logger.info(f"Trying to book: {clazz}")
    tasks.append(user.book_class_at(clazz.start_time, clazz.day, clazz.month))

  asyncio.gather(*tasks)
