.PHONY:
	@echo "targets: wordlist, mask, or bomb"

wordlist: 
	@python3 main.py wordlist $(ARGS)

mask: 
	@python3 main.py wordlist $(ARGS)

bomb: 
	@python3 main.py wordlist $(ARGS)

