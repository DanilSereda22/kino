import requests
url = 'http://localhost:8000/api/capitals/'
response = requests.get(url)
response_on_python = response.json()
with open('capitals.txt', 'w') as file:
    for capital in response_on_python:
        file.write(
            f"The population of {capital['capital_city']} is "
            f"{capital['capital_population']}, "
            f"author - {capital['author']}\n"
        )