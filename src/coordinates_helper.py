import requests
import structlog

logger = structlog.get_logger()


def get_cordinates_from_address(query: str, limit: int = 1) -> dict | None:

    try:
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
    
    except requests.HTTPError as e:
        logger.error("Error HTTP", error=str(e))
        return None
    except requests.RequestException as e:
        logger.error("Error network", error=str(e))
        return None