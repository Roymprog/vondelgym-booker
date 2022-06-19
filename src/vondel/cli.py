from vondel.user import User
from vondel.parse_page import get_wanted_classes_from_vondelgym_oost
import click

@click.command()
@click.argument('email', envvar='VONDELGYM_EMAIL')
@click.argument('password', envvar='VONDELGYM_PASSWORD')
def main(email, password):
  user = User()

  user.login(email=email, password=password)

  wanted = get_wanted_classes_from_vondelgym_oost(user.session_id)
  
  print("Found following classes:")
  for clazz in wanted:
    print(f"Trying to book: {clazz}")
    user.book_class_at(clazz.start_time, clazz.day, clazz.month)

if __name__ == "__main__":
  main()
