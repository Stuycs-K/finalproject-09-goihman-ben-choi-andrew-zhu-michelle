.PHONY: wordlist mask bomb

wordlist: 
	@python3 main.py wordlist $(ARGS)

mask: 
	@python3 main.py mask $(ARGS)

bomb: 
	@python3 main.py bomb $(ARGS)

