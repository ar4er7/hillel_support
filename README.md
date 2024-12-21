# About
this is the educational project for Hillel IT

The pipenv is used as a main package manager for the project. For more info please follow [documentation](https://pipenv.pypa.io/en/latest/)

# `pipenv` usage

```sh
# Creating new virtual environment
pipenv shell

#Creating a .lock file form Pipenv five
pipenv lock

#Installing dependencies from .lock file
pipenv sync
```

```python
@app.get("/fetch-market")
async def get_current_market_state():
url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=UAH&apikey=MO31CNEF7DLKTRW1"

# response: requests.Response = requests.get(url)
async with httpx.AsyncClient() as client:
response: httpx.Response = await client.get(url)

rate: str = response.json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"]

return {"rate": rate}
```