import pytest
from pathlib import Path
from bs4 import BeautifulSoup

@pytest.fixture
def login_html_soup():
  with open(Path(__file__).parent / 'data/login.html', 'r') as fp:
    yield BeautifulSoup(fp, "html.parser")
