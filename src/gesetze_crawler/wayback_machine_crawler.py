import requests

def get_wayback_web_addresses(web_address: str, timestamp: str) -> list[str]:
    wayback_address = "https://web.archive.org/cdx/search/cdx?url=" + web_address + "&output=json&collapse=digest&from=" + timestamp
    response = requests.get(wayback_address)
    data = response.json()
    if len(data) <= 1:
        return []
    return ["https://web.archive.org/web/" + row[1] + "/" + web_address for row in data[1:]]

def get_wayback_web_address(web_address: str, timestamp: str) -> str:
    wayback_address = "https://web.archive.org/cdx/search/cdx?url=" + web_address + "&output=json&limit=1&from=" + timestamp
    response = requests.get(wayback_address)
    data = response.json()
    return "https://web.archive.org/web/" + data[1][1] + "/" + web_address if len(data) > 1 else None