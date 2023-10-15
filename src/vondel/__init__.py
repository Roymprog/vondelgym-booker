__version__="0.0.1"

from vondel.user import User
import logging
import asyncio

def run(email: str, password: str) -> None:
  logger = logging.getLogger()
  user = User()

  if not user.jwt:
    user.login(email=email, password=password)

    wanted = user.get_wanted_classes_from_vondelgym_oost()
  
  logger.info("Found following classes:")

  tasks = []
  for clazz in wanted:
    logger.info(f"Trying to book: {clazz}")
    tasks.append(user.book_class(user.jwt, clazz["id"], clazz["date"]))

  asyncio.gather(*tasks)
