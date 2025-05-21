import zipfile
import os
import sys

def dict_attack(zip_path, wordlist_path):
    print('dict_attack')

def main():
	if sys.argv[1] == 'wordlist':
		print("wordlist")
	if sys.argv[1] == 'mask':
		print('mask')
	if sys.argv[1] == 'bomb':
		print('bomb')
	return 0

if __name__ == '__main__':
	main()
