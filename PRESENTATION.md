# ZIP BOMBBBBBBBBBBB!

## Table of Contents
1. Wordlist attack
2. Mask attack with wordlist
3. Brute force mask attack
4. Zip bomb detection
5. Zip bomb maker

## Libraries
1. zipfile - open, read, write, and inspect ZIP archives
2. os - check against missing input files
3. sys - access command-line arguments
4. itertools - iterate over all combinations of unknown characters in the mask, enabling a brute‐force loop without manual nested loops
5. string - build character set used for brute‐forcing masked passwords

## Features Explanation

### Wordlist Attack
The wordlist attack attempts to crack a ZIP file's password by trying each password from a provided wordlist file. It reads the wordlist line by line and attempts to extract the ZIP file with each password until it finds the correct one.

```python
def dict_attack(zip_path, wordlist_path):
    if not os.path.exists(wordlist_path):
        print(f"Error: Wordlist file '{wordlist_path}' not found")
        return None
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
        return attack(zip_path, wordlist)
```

### Mask attack with wordlist
This feature combines a wordlist with a mask pattern. The mask uses '_' as a wildcard character, and only passwords from the wordlist that match the mask pattern are tried. For example, if the mask is "pass___", it will only try passwords from the wordlist that start with "pass" followed by any three characters.

```python
def mask_attack(zip_path, wordlist_path, mask):
    if not os.path.exists(wordlist_path):
        print(f"Error: Wordlist file '{wordlist_path}' not found")
        return None
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
        wordlist = [word for word in wordlist if matches_mask(word.strip(), mask)]
        return attack(zip_path, wordlist)
```

### Brute force mask attack
This feature performs a brute force attack using a mask pattern. For each '_' in the mask, it tries all possible characters (letters and numbers) in that position. This is useful when you know part of the password but need to guess the rest.

```python
def brute_mask(zip_path, mask):
    unknown_positions = [i for i, char in enumerate(mask) if char == '_']
    charset = string.ascii_letters + string.digits
    
    with zipfile.ZipFile(zip_path) as zip_file:
        for combination in itertools.product(charset, repeat=len(unknown_positions)):
            password = list(mask)
            for i, char in enumerate(combination):
                password[unknown_positions[i]] = char
            password = ''.join(password)
            # Try to extract with the generated password
```

### Zip bomb detection
This feature analyzes a ZIP file for potential zip bomb characteristics by checking:
- Number of files (max 100)
- Directory depth (max 5 levels)
- Compression ratio (max 50:1)
- Presence of nested ZIP files

```python
def bomb_detection(zip_path):
    MAX_C_RATIO = 50
    MAX_FILES = 100
    MAX_DEPTH = 5
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            files = zip_file.namelist()
            # Check file count, depth, and compression ratio
            if len(files) > MAX_FILES:
                return True
            # Additional checks for depth and compression...
```

### Zip bomb maker
This feature creates a simple zip bomb by generating a ZIP file containing 1000 small text files. While this is a basic example, it demonstrates how zip bombs can be created.

```python
def make_bomb(zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for i in range(1000):
            zip_file.writestr(f'file_{i}.txt', 'Hello, world!')
```
