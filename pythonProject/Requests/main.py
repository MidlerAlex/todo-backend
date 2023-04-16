import requests
from pprint import pprint


result = requests.get('https://swapi.dev/api/people/1')

pprint(result.json())