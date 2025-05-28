.PHONY: wordlist mask bomb

wordlist: 
	@python3 main.py wordlist $(ARGS)

mask: 
	@python3 main.py mask $(ARGS)

make_bomb: 
	@python3 main.py make_bomb $(ARGS)

detect_bomb:
	@python3 main.py detect_bomb $(ARGS)

make_zip:
	@python3 main.py make_zip $(ARGS)