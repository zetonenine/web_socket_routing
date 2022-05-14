
def index():
    with open('templates/index.html') as t:
        return t.read()


def locations():
    with open('templates/locations.html') as t:
        return t.read()


def location(city):
    try:
        with open(f'templates/{city}.html') as t:
            return t.read()
    except:
        return f"<h1>I don't know this city: {city}</h1>"
