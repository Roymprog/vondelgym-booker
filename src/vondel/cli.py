import logging

from vondel import run
import click

@click.command()
@click.argument('email', envvar='VONDELGYM_EMAIL')
@click.argument('password', envvar='VONDELGYM_PASSWORD')
def main(email: str, password: str):
  logging.basicConfig(level=logging.INFO)
  run(email, password)

if __name__ == "__main__":
  main()
