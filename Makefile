.PHONY: install-dependencies test deploy

install-dependencies:
	@pip install -r requirements.txt

test:
	@nosetests --rednose

deploy:
	cf push fogeybot
