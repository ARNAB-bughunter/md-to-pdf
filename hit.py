import requests

with open("input.md") as f:
    text = f.read()
    url = "http://0.0.0.0:5000/api/convert"
    response = requests.post(url=url, json={"markdown": text, "filename": "test.pdf"})

    with open('test.pdf', 'wb') as f:
        f.write(response.content)