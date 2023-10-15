import logging

import azure.functions as func
import logging
import os
from vondel import run

def main(req: func.HttpRequest) -> func.HttpResponse:
  logging.basicConfig(level=logging.INFO)

  logging.info('Python HTTP trigger function processed a request.')

  email = os.environ["VONDELGYM_EMAIL"]
  password = os.environ["VONDELGYM_PASSWORD"]

  try:
    run(email, password)
    return func.HttpResponse("Successfully ran Vondelgym bookers.")
  except Exception as e:
    logging.error(e)
    return func.HttpResponse(
          "This HTTP triggered function executed unsuccessfully.",
          status_code=500
    )
