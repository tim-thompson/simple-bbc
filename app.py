import os
import urllib.parse

from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, url_for
import requests

app = Flask(__name__)

key = os.getenv("NEWSAPI_KEY")
base_url = "https://newsapi.org/v2/"

headlines = []


@app.route("/")
def index():
    global headlines
    response = requests.get(base_url + f"top-headlines?sources=bbc-news&apiKey={key}")
    if response.json()["status"] != "ok":
        return "An error occurred requesting latest headlines", 503
    headlines = [
        article
        for article in response.json()["articles"]
        if article["content"] is not None
    ]
    return render_template("index.html", headlines=headlines)


@app.route("/<int:index>")
def article(index):
    global headlines

    if len(headlines) == 0:
        return redirect(url_for("index"))

    response = requests.get(headlines[index]["url"])
    html = BeautifulSoup(response.content, "html.parser")
    article = ""
    content = html.select("div.story-body__inner")
    for div in content:
        for item in div.children:
            print(item.name)
            if item.name == "p":
                if item.has_attr("class") and item["class"] == [
                    "story-body__introduction"
                ]:
                    article += item.prettify()
                elif not item.has_attr("class"):
                    article += item.prettify()
            elif item.name == "figure":
                for img in item.select("img"):
                    caption = item.select("span.media-caption__text")
                    caption = caption[0] if len(caption) > 0 else ""
                    article += f"""
                        <figure>
                            {img.prettify()}
                            <figcaption>
                                {caption}
                            </figcaption>
                        </figure>
                    """
                print(item)

    title = ""
    for h1 in html.select("h1"):
        title = h1.text
    return render_template(
        "article.html",
        html=html,
        article=article,
        headline=headlines[index],
        title=title,
    )


if __name__ == "__main__":
    app.run()
