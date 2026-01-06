import requests

def get_cordinates_from_address(query: str, limit: int = 1) -> dict | None:
    url = "https://api-adresse.data.gouv.fr/search/"
    params = {
        "q": query,
        "limit": limit,
    }

    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()

    data = response.json()
    print(data)

    return (data["features"][0]["geometry"]["coordinates"]) if data["features"] else None