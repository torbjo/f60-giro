
all: out.pdf
	xpdf out.pdf

out.pdf: main.py f60/*.py
	python main.py out.pdf

