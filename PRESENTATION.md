# ZIP BOMBBBBBBBBBBB!

## Table of Contents
1. Wordlist attack
2. Mask attack with wordlist
3. Pause and Resume Functionality
4. Brute force mask attack
5. Zip bomb detection
6. Zip bomb maker

## Libraries
1. zipfile - open, read, write, and inspect ZIP archives
2. os - check against missing input files
3. sys - access command-line arguments
4. itertools - iterate over all combinations of unknown characters in the mask, enabling a brute‐force loop without manual nested loops
5. string - build character set used for brute‐forcing masked passwords
6. select - check for user input without blocking the main attack loop
7. signal - handle ctrl c

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
This feature combines a wordlist with a mask pattern. The mask uses '_' as a wildcard character, and only passwords from the wordlist that match the mask pattern are tried. For example, if the mask is "pass___", it will only try passwords from the wordlist that start with "pass" followed by any three characters. To do this it first makes a wordlist of valid passwords from the wordlist that match the mask pattern, than does the same dictionary attack just with the new wordlist.

```python
def mask_attack(zip_path, wordlist_path, mask):
    if not os.path.exists(wordlist_path):
        print(f"Error: Wordlist file '{wordlist_path}' not found")
        return None
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
        wordlist = [word for word in wordlist if matches_mask(word.strip(), mask)]
        return attack(zip_path, wordlist)
```

### Pause and Resume Functionality
This feature allows users to pause  attacks by pressing 'q' and resume them later using the `cont` parameter. Progress is saved to files (`where.txt` for wordlist/mask attacks, `brute_where.txt` for brute force) and validated when resuming to ensure no errors. This however doesn't let ctrl c work. So I added a signal handler to handle ctrl c.

```python
# Handle ctrl c
def sigint_handler(signum, frame):
    os.kill(os.getpid(), signal.SIGTERM)

signal.signal(signal.SIGINT, sigint_handler)

# Check if user pressed 'q' to pause
if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
    key = sys.stdin.read(1)
    if key.lower() == 'q':
        save_progress(zip_path, wordlist_path, line_num)
        return None
```

### Brute force mask attack
This feature performs a brute force attack using a mask pattern. For each '_' in the mask, it tries all possible characters (letters and numbers) in that position. This is useful when you know part of the password but need to guess the rest. This makes it slower than the normal mask attach but when only missing a few characters it can be worth the trade off.

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
- Directory depth (max 5 levels)
- Compression ratio (max 50:1)
- Presence of nested ZIP files

```python
def bomb_detection(zip_path):
    MAX_C_RATIO = 50
    MAX_DEPTH = 5
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            files = zip_file.namelist()
            
            # Check directory depth
            max_d = 0
            for file in files:
                curr_d = file.count('/')
                max_d = max(curr_d, max_d)
            if max_d > MAX_DEPTH:
                print(f"Exceeded max depth of {MAX_DEPTH}, currently has a max depth of {max_d}")
                return True
            
            # Check compression ratio and nested zip files
        
        return False
    except zipfile.BadZipFile:
        print("Bad zip file")
        return False
```

### Zip bomb maker
This feature creates a simple zip bomb by generating a ZIP file containing 1000 small text files. While this is a basic example, it demonstrates how zip bombs can be created. It writes 1000 files, each containing 1MB of 'a' characters.

```python
def make_bomb(zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for i in range(1000):
            zip_file.writestr(f'file_{i}.txt', 'a'*1000000)
```

### Custom Compression (make_zip)
This feature implements a custom compression algorithm that uses pattern matching to identify and compress repeated sequences in files. It works by:
1. Finding repeated patterns in the input files
2. Replacing these patterns with shorter markers
3. Storing the patterns in a separate dictionary file
4. Creating a compressed binary output file

```python
def make_zip(file_names):
    # Find repeated patterns across files
    # Replace patterns with markers
    # Save patterns to patterns.bin
    # Create compressed_output.bin
```

### Custom Decompression (decompress_file)
This feature decompresses files that were compressed using the custom compression algorithm. It:
1. Reads the compressed binary file
2. Loads the pattern dictionary
3. Replaces markers with original patterns
4. Reconstructs the original files

```python
def decompress_file(compressed_filename, pattern_dict):
    # Read compressed file structure
    # Load pattern dictionary
    # Replace markers with patterns
    # Write decompressed files
```
