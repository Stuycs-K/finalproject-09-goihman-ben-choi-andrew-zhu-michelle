import zipfile
import os
import sys
import itertools
import string

def dict_attack(zip_path, wordlist_path):
    try:
        if not os.path.exists(zip_path):
            print(f"Error: Zip file '{zip_path}' not found")
            return None
        if not os.path.exists(wordlist_path):
            print(f"Error: Wordlist file '{wordlist_path}' not found")
            return None

        with zipfile.ZipFile(zip_path) as zip_file:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
                for password in wordlist:
                    password = password.strip()
                    if not password:
                        continue
                    
                    try:
                        zip_file.extractall(pwd=password.encode())
                        print(f"Password found: {password}")
                        return password
                    except:
                        continue
            
            print("Password not found in wordlist")
            return None

    except zipfile.BadZipFile:
        print("Error: Invalid zip file")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def mask_attack(zip_path, mask):
      return None;

def main():
	if len(sys.argv) < 3:
		print("Usage: python main.py wordlist <zip_file> <wordlist_file>")
		return 1
	
	if sys.argv[1] == 'wordlist':
		if len(sys.argv) != 4:
			print("Usage: python main.py wordlist <zip_file> <wordlist_file>")
			return 1
		dict_attack(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == 'mask':
		if len(sys.argv) != 4:
			print("Usage: python main.py mask <zip_file> <mask>")
			return 1
		mask_attack(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == 'bomb':
		print('bomb')
	return 0

if __name__ == '__main__':
	main()
