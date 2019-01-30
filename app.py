import os
from urllib.parse import urlsplit, urlunsplit

from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, url_for
import requests


class BadKeyError(Exception):
    pass


app = Flask(__name__)

key = os.getenv("NEWSAPI_KEY")
base_url = "https://newsapi.org/v2/"

if key is None or key == "":
    raise BadKeyError("Please ensure the NEWSAPI_KEY environment variable is set")

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
            if item.name == "p":
                if item.has_attr("class") and item["class"] == [
                    "story-body__introduction"
                ]:
                    article += item.prettify()
                elif not item.has_attr("class"):
                    article += item.prettify()
            elif item.name == "h2":
                article += item.prettify()
            elif item.name == "figure":
                caption = ""
                for figcaption in item.select("figcaption"):
                    for span in figcaption.select("span.media-caption__text"):
                        caption = span.text
                for span in item.select("span"):
                    for div in span.select("div.js-delayed-image-load"):
                        img_url = urlsplit(div['data-src'])
                        img_path = img_url.path.split('/')
                        img_path[2] = str(800)
                        new_path = ("/".join(img_path))
                        new_img_url = urlunsplit((
                            img_url.scheme,
                            img_url.netloc,
                            new_path,
                            img_url.query,
                            img_url.fragment
                        ))
                        article += f"""
                            <figure class="box">
                                <img 
                                    src={new_img_url} 
                                    alt="{div['data-alt']}"
                                />
                                <figcaption>
                                    <strong>{caption}</strong>
                                </figcaption>
                            </figure>
                        """
                for img in item.select("img"):
                    caption = item.select("span.media-caption__text")
                    caption = caption[0] if len(caption) > 0 else ""
                    article += f"""
                        <figure class="box">
                            {img.prettify()}
                            <figcaption>
                                <strong>{caption}</strong>
                            </figcaption>
                        </figure>
                    """
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
