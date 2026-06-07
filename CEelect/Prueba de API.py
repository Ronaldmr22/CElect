#Fuente : https://www.exchangerate-api.com/docs/python-currency-api
import requests

# Where USD is the base currency you want to use
url = 'https://api.hacienda.go.cr/indicadores/tc/dolar'

# Making our request
response = requests.get(url)
data = response.json()
# Your JSON object
print (data)