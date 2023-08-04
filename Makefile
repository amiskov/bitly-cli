run:
	poetry run python app.py --token ${BITLY_TOKEN}

shell:
	poetry run ipython app.py
