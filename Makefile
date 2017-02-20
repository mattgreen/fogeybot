.PHONY: install-dependencies test deploy

install-dependencies:
	@pip install -r requirements.txt

test:
	@green3

deploy:
	cf push fogeybot
