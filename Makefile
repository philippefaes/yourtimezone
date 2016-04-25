help:
	@echo "Valid targetsa are:"
	@echo "  make deploy"
	@echo "  make serve"
	@echo "  make install-deps"
	
deploy:
	appcfg.py -A yourtimezone --oauth2 update .
	
serve:
	dev_appserver.py .
	
install-deps:
	pip install -r requirements.txt -t lib