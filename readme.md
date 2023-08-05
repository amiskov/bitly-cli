# CLI for Bitly
A CLI client for Bitly. For now it can shorten a given URL and count clicks for a given bitlink (a short URL, provided by Bitly).

## Usage
First, grab your Bitly API token [here](https://app.bitly.com/settings/api/) and paste it into `.env`:

```sh
cp .env.example .env
# paste your token into `.env`
```

Add dependencies via [Poetry](https://python-poetry.org):

```sh
$ poetry install
```

Now you can create a bitlink (short URL) from a long one:

```sh
$ poetry run python app.py
Enter a URL: https://some.long.url/
Битлинк: https://bit.ly/blah123
```

or count links for a bitlink:

```sh
$ poetry run python app.py
Enter a URL: https://bit.ly/blah123
7
```
