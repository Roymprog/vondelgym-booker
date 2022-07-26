from bs4 import BeautifulSoup
from vondel.user import User 


def test_get_classes(login_html_soup: BeautifulSoup):
  session_id = User.read_session_id(login_html_soup.prettify())
  
  assert session_id == 'some_session_id'
