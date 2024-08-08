import requests


def generate_summary(content):
    response = requests.post("http://localhost:5000/generate-summary", json={"content": content})
    return response.json().get('summary', '')


def generate_review_summary(reviews):
    review_content = " ".join(reviews)
    response = requests.post("http://localhost:5000/generate-summary", json={"content": review_content})
    return response.json().get('summary', '')
