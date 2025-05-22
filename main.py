import zipfile
import os
import sys
import itertools
import string


def attack(zip_path, wordlist):
    try:
        if not os.path.exists(zip_path):
            print(f"Error: Zip file '{zip_path}' not found")
            return None

        with zipfile.ZipFile(zip_path) as zip_file:
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
    
def matches_mask(word, mask):
    word = word.strip()
    mask = mask.strip()
    if len(word) != len(mask):
        return False
    for w_char, m_char in zip(word, mask):
        if m_char != '_' and w_char != m_char:
            return False
    return True

def mask_attack(zip_path, wordlist_path, mask):
    if not os.path.exists(wordlist_path):
        print(f"Error: Wordlist file '{wordlist_path}' not found")
        return None
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
        wordlist = [word for word in wordlist if matches_mask(word.strip(), mask)]
        return attack(zip_path, wordlist)
def dict_attack(zip_path, wordlist_path):
    if not os.path.exists(wordlist_path):
        print(f"Error: Wordlist file '{wordlist_path}' not found")
        return None
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
        return attack(zip_path, wordlist)
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
		if len(sys.argv) != 5:
			print("Usage: python main.py mask <zip_file> <wordlist_file> <mask>")
			return 1
		mask_attack(sys.argv[2], sys.argv[4], sys.argv[3])
	elif sys.argv[1] == 'bomb':
		print('bomb')
	return 0

if __name__ == '__main__':
	main()
