install-dependencies:
	@pip install -r requirements.txt

.PHONY: test
test:
	@nosetests --rednose

deploy:
	cf push fogeybot
