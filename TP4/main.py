from app import app
import requests


if __name__ == "__main__":
    print(requests.get(f"http://127.0.0.1:8000/power_function?x=9&a=2").json())


