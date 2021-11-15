.PHONY: index.html
index.html: index.html.in index.cfg index.py
	python index.py > index.html

.PHONY: clean
clean:
	rm -f index.html
