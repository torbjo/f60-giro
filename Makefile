all: test

main:
	python main.py out.pdf
	xpdf out.pdf

test:
	python test.py out.pdf
	xpdf out.pdf
