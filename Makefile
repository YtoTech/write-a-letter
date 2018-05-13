install:
	# Install mrzool letter template.
	git clone https://github.com/mrzool/letter-boilerplate.git templates/mrzool-letter

output:
	cd templates/mrzool-letter && make output.pdf
