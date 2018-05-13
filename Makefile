install:
	# Install mrzool letter template.
	git clone https://github.com/mrzool/letter-boilerplate.git templates/mrzool-letter

output:
	cd templates/mrzool-letter && make output.pdf

output-online: output-latex
	pipenv run python online.py compile templates/mrzool-letter/output.latex templates/mrzool-letter/output.pdf

output-latex:
	cd templates/mrzool-letter && pandoc -s -o output.latex -t latex --template=template.tex letter.md
