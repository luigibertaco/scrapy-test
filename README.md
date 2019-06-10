# scrapy-test

## Install requirements

``pip install -r requirements.txt``

## Start REST API

``python main.py``

### Use API

To get articles open `http://127.0.0.1:5000/article`

Use querystrings for:

- *$skip* and *$limit* for paginaltion - (default to 0 and 10 respectively)
- *$keywords* for filters - comma delimited

I.e.: `http://127.0.0.1:5000/article?keywords=Culture,Law&skip=10&limit=10`

## Configure how many article pages to fetch

modify `MAX_PAGE_REQUESTS` on `scrapy_theguardian/settings.py`

## Collect articles from The Guardian

``cd scrapy_theguardian && scrapy crawl articles``
