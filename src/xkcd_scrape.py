import requests

def get_xkcd_data():
    response = requests.get("https://xkcd.com/info.0.json")

    if response.status_code == 200:
        return response.json()
    # TODO log wrong responses
    return ""

def format_xkcd_data(json_data):
    title = json_data["safe_title"]
    html_data = f'<img src="{json_data["img"]}" alt="{json_data["alt"]}" title="{title}">'
    return html_data, title

if __name__ == "__main__":
    response = get_xkcd_data()
    print(format_xkcd_data(response))
