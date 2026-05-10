import requests


API_URL = "http://127.0.0.1:8000"


def test_health():
    response = requests.get(f"{API_URL}/health", timeout=10)
    print("Health:", response.status_code, response.json())


def test_ask():
    payload = {
        "question": "Quels événements culturels puis-je faire prochainement dans le Val-de-Marne ?"
    }

    response = requests.post(f"{API_URL}/ask", json=payload, timeout=60)

    print("Ask:", response.status_code)
    print(response.json())


if __name__ == "__main__":
    test_health()
    test_ask()