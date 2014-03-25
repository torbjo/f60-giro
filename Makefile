
all: example.pdf
	xdg-open $<

example.pdf: example.py f60/*.py
	python $< $@

