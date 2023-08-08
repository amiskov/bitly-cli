# CLI for Bitly
A CLI client for [Bitly](https://bitly.com). It can shorten a given URL or count clicks for a given bitlink (a short URL, provided by Bitly).

## Requirements
Add dependencies via [Poetry](https://python-poetry.org):

```sh
$ poetry install
```

## Secrets
Grab your Bitly API token [here](https://app.bitly.com/settings/api/) and paste it into `.env` using `.env.example` as a template:

```sh
$ cp .env.example .env
# paste your token into `.env`
```

## Run
Now you can create a bitlink (short URL) from a long one:

```sh
$ poetry run python app.py https://some.long.url/
Битлинк: https://bit.ly/blah123
```

or count links for a bitlink:

```sh
$ poetry run python app.py https://bit.ly/blah123
7
```
