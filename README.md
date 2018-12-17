# Simple BBC

## Overview

A simple Flask application that requests the top news articles from BBC News using the free plan of [newsapi.org](newsapi.org) and displays the contents in a clean and easy to read way.

## Reasoning

I have created this project in an effort to focus more on the content I am consuming. BBC News is my preferred source for news, and although I enjoy the layout of their website, there is still clickbaity articles and videos that threaten to drag me down a rabbit hole. Simple BBC allows me to focus on staying informed without browsing endless content. By forcing my news content to have a conclusion I will be removing the danger of mindlessly scrolling through content until the end of time.

## Tech

Simple BBC runs on Python using Flask as the web server, requests to talk to [newsapi.org](newsapi.org), Beautiful Soup to scrape the articles and the Bulma CSS Framework.

## Setup and Operation

To run the project for yourself you will require an API key from [newsapi.org](newsapi.org). This should be added to the `NEWSAPI_KEY` environment variable.