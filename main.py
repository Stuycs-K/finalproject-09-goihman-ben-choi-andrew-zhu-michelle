import zipfile
import os
import sys
import itertools
import string
import shutil
import tempfile


def attack(zip_path, wordlist):
    try:
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


def brute_mask(zip_path, mask):
    unknown_positions = [i for i, char in enumerate(mask) if char == '_']
    
    if not unknown_positions:
        return attack(zip_path, [mask])
    
    charset = string.ascii_letters + string.digits
    
    try:
        if not os.path.exists(zip_path):
            print(f"Error: Zip file '{zip_path}' not found")
            return None

        with zipfile.ZipFile(zip_path) as zip_file:
            for combination in itertools.product(charset, repeat=len(unknown_positions)):
                password = list(mask)
                for i, char in enumerate(combination):
                    password[unknown_positions[i]] = char
                password = ''.join(password)
                
                try:
                    zip_file.extractall(pwd=password.encode())
                    print(f"Password found: {password}")
                    return password
                except:
                    continue
            
            print("Password not found in brute force attack")
            return None

    except zipfile.BadZipFile:
        print("Error: Invalid zip file")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def mask_attack(zip_path, wordlist_path, mask):
    if not os.path.exists(wordlist_path):
        print(f"Error: Wordlist file '{wordlist_path}' not found")
        return None
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
        wordlist = [word for word in wordlist if matches_mask(
            word.strip(), mask)]
        return attack(zip_path, wordlist)


def dict_attack(zip_path, wordlist_path):
    if not os.path.exists(wordlist_path):
        print(f"Error: Wordlist file '{wordlist_path}' not found")
        return None
    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as wordlist:
        return attack(zip_path, wordlist)


def bomb_detection(zip_path):
    MAX_C_RATIO = 50
    MAX_FILES = 100
    MAX_DEPTH = 5
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            files = zip_file.namelist()
            max_d = 0
            for file in files:
                curr_d = file.count('/')
                max_d = max(curr_d, max_d)
            if max_d > MAX_DEPTH:
                print(f"Exceeded max depth of {MAX_DEPTH}, currently has a max depth of {max_d}")
                return True
            compressed = 0
            uncompressed = 0
            # check for nested files
            for file in zip_file.filelist:
                if str(file).lower().endswith(".zip"):
                    print("Detected a nested zipfile, potentially harmful")
                    return True
                compressed+= file.compress_size
                uncompressed+= file.file_size
            if compressed > 0:
                compression_ratio = uncompressed / compressed
                if compression_ratio > MAX_C_RATIO:
                    print(f"Very high compression ratio: exceeds max of {MAX_C_RATIO}, ratio is {compression_ratio}")
                    return True
        print(zip_file.filelist)
        return False
    except zipfile.BadZipFile:
        print("Bad zip file")
        return False
    except Exception as E:
        print(E)
        return False

def make_bomb(zip_path):
    temp_dir = tempfile.mkdtemp()
    try:
        for i in range(1000):
            file_path = os.path.join(temp_dir, f'file_{i}.txt')
            with open(file_path, 'w') as f:
                f.write('a' * 1000000) # 1MB of 'a' characters per file
        
        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zip_file.write(file_path, arcname)
        
        print(f"Zip bomb created: {zip_path}")
        
    finally:
        shutil.rmtree(temp_dir)

def make_zip(file_names):
    MIN_PATTERN = 4
    MAX_PATTERN = 100
    compressed_size = 0
    original_size = 0
    binary_files = {}
    for file in file_names:
        with open(file, 'rb') as f:
            binary_files[file] = f.read()
    compressed_files = {}
    for file, binary in binary_files.items():
        patterns = {}
        for sequence_len in range(MIN_PATTERN, min(MAX_PATTERN, len(binary))):
            for i in range(len(binary) - sequence_len + 1):
                pattern = binary[i:i+sequence_len]
                if pattern in patterns:
                    patterns[pattern].append(i)
                else:
                    patterns[pattern] = [i]
        best_patterns = {}
        for pattern, pos in patterns.items():
            if len(pos) > 1: # >1 pattern occurs
                best_patterns[pattern] = pos
        new_data = bytearray(binary)
        pid = 0
        for pattern in best_patterns:
            if len(pattern) > MIN_PATTERN:
                marker = b'\xFF\xFE'
                flag = marker + pid.to_bytes(2, 'big')
                new_data = new_data.replace(pattern, flag)
                pid+= 1
        compressed_files[file] = bytes(new_data)
        original_size+= len(binary)
        compressed_size+= len(new_data)
    print(f'Original size: {original_size}')
    print(f'Compressed size: {compressed_size}')    
    with open('compressed_output.bin', 'wb') as output_file:
        for filename, compressed_data in compressed_files.items():
            output_file.write(compressed_data)
    
    return compressed_files

def main():
    if len(sys.argv) < 3:
        print("Usage: make wordlist <zip_file> <wordlist_file>")
        print("       make mask <zip_file> <mask>") 
        print("       make mask <zip_file> <wordlist_file> <mask>")
        print("       make brute <zip_file> <mask>")
        print("       make detect_bomb <zip_file>")
        return 1
    if sys.argv[1] == 'wordlist':
        if len(sys.argv) != 4:
            print("Usage: make wordlist ARGS=<zip_file> <wordlist_file>")
            return 1
        dict_attack(sys.argv[2], sys.argv[3])
    if sys.argv[1] == 'mask':
        if len(sys.argv) != 5:
            print("Usage: make mask ARGS=<zip_file> <wordlist_file> <mask>")
            return 1
        mask_attack(sys.argv[2], sys.argv[4], sys.argv[3])
    if sys.argv[1] == 'make_bomb':
        if len(sys.argv) != 3:
            print("Usage: make make_bomb ARGS=<zip_file>")
            return 1
        make_bomb(sys.argv[2])
    elif sys.argv[1] == 'mask':
        if len(sys.argv) == 4:
            brute_mask(sys.argv[2], sys.argv[3])
        elif len(sys.argv) == 5:
            mask_attack(sys.argv[2], sys.argv[3], sys.argv[4])
        else:
            print("Usage: make mask <zip_file> <mask>")
            print("   or: make mask <zip_file> <wordlist_file> <mask>")
            return 1
    elif sys.argv[1] == 'brute':
        if len(sys.argv) != 4:
            print("Usage: make brute <zip_file> <mask>")
            return 1
        brute_mask(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'make_bomb':
        if len(sys.argv) != 3:
            print('Usage: make make_bomb ARGS=<zip_file>')
            return 1
        make_bomb(sys.argv[2])
    if sys.argv[1] == 'detect_bomb':
        if len(sys.argv) != 3:
            print('Usage: make detect_bomb ARGS=<zip_file>')
            return 1
        bomb_detection(sys.argv[2])
    if sys.argv[1] == 'make_zip':
        if len(sys.argv) < 3:
            print('Usage: make make_zip ARGS="<file1> <file2>...')
            return -1
        make_zip(sys.argv[2:])
    return 0

if __name__ == '__main__':
    main()