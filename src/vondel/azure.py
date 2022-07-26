import logging

import azure.functions as func
import cli

def main() -> func.HttpResponse:
  logging.info('Python HTTP trigger function processed a request.')

  try:
    cli.main()
    return func.HttpResponse("Successfully ran Vondelgym bookers.")
  except Exception as e:
    logging.error(e.message)
    return func.HttpResponse(
          "This HTTP triggered function executed unsuccessfully.",
          status_code=500
    )
