.PHONY: wordlist mask bomb

wordlist: 
	@python3 main.py wordlist $(ARGS)

mask: 
	@python3 main.py mask $(ARGS)

brute:
	@python3 main.py brute $(ARGS)
	
make_bomb: 
	@python3 main.py make_bomb $(ARGS)

detect_bomb:
	@python3 main.py detect_bomb $(ARGS)

make_zip:
	@python3 main.py make_zip $(ARGS)

decompress:
	@python3 main.py decompress $(ARGS)