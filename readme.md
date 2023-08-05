# CLI for Bitly
A CLI client for Bitly. For now it can shorten a given URL and count clicks for a given bitlink (a short URL, provided by Bitly).

Usage:

```sh
# Install
$ poetry install

# Run: create short URL from a long one
$ poetry run python app.py
Enter a URL: https://some.long.url/
Битлинк: https://bit.ly/blah123

# Run: count links for a bitlink
$ poetry run python app.py
Enter a URL: https://bit.ly/blah123
7
```

You can grab your token [here](https://app.bitly.com/settings/api/).
