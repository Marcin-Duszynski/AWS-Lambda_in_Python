/opt/virtual_env:
	# create virtual env if folder not exists
	python3 -m venv /opt/virtual_env

virtual: /opt/virtual_env

requirements: 
	pip3 install -r requirements.txt
	pip3 install requests -t .

install: virtual requirements
