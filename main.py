import zipfile
import os
import sys
import itertools
import string
import shutil
import tempfile
import select
import json

def save_progress(zip_path, wordlist_path, line_num):
    with open("where.txt", "w") as f:
        f.write(f"{zip_path}\n{wordlist_path}\n{line_num}\n")

def load_progress():
    if os.path.exists("where.txt"):
        with open("where.txt", "r") as f:
            lines = f.read().strip().split('\n')
            if len(lines) == 3:
                return lines[0], lines[1], int(lines[2])
    return None, None, 0

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


def save_brute_progress(zip_path, mask, combination_index):
    with open("brute_where.txt", "w") as f:
        f.write(f"{zip_path}\n{mask}\n{combination_index}\n")

def load_brute_progress():
    if os.path.exists("brute_where.txt"):
        with open("brute_where.txt", "r") as f:
            lines = f.read().strip().split('\n')
            if len(lines) == 3:
                return lines[0], lines[1], int(lines[2])
    return None, None, 0

def brute_mask(zip_path, mask, start_index=0):
    unknown_positions = [i for i, char in enumerate(mask) if char == '_']
    
    if not unknown_positions:
        return attack(zip_path, [mask])
    
    charset = string.ascii_letters + string.digits
    
    try:
        if not os.path.exists(zip_path):
            print(f"Error: Zip file '{zip_path}' not found")
            return None

        with zipfile.ZipFile(zip_path) as zip_file:
            combination_index = 0
            for combination in itertools.product(charset, repeat=len(unknown_positions)):
                if combination_index < start_index:
                    combination_index += 1
                    continue
                    
                password = list(mask)
                for i, char in enumerate(combination):
                    password[unknown_positions[i]] = char
                password = ''.join(password)
                
                # Check if user pressed 'q'
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    key = sys.stdin.read(1)
                    print(f"Key pressed: {key}")
                    if key.lower() == 'q':
                        save_brute_progress(zip_path, mask, combination_index)
                        print(f"Saved brute force progress at combination {combination_index}")
                        return None
                
                try:
                    zip_file.extractall(pwd=password.encode())
                    print(f"Password found: {password}")
                    if os.path.exists("brute_where.txt"):
                        os.remove("brute_where.txt")
                    return password
                except:
                    pass
                
                combination_index += 1
            
            print("Password not found in brute force attack")
            if os.path.exists("brute_where.txt"):
                os.remove("brute_where.txt")
            return None

    except zipfile.BadZipFile:
        print("Error: Invalid zip file")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def mask_attack(zip_path, wordlist_path, mask, start_line=0):
    if not os.path.exists(wordlist_path):
        print(f"Error: Wordlist file '{wordlist_path}' not found")
        return None
    
    try:
        with zipfile.ZipFile(zip_path) as zip_file:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            matching_words = []
            for i, word in enumerate(lines):
                if i < start_line:
                    continue
                if matches_mask(word.strip(), mask):
                    matching_words.append((i, word.strip()))
            
            for line_num, password in matching_words:
                if not password:
                    continue
                
                # Check if user pressed 'q'
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    key = sys.stdin.read(1)
                    print(f"Key pressed: {key}")
                    if key.lower() == 'q':
                        save_progress(zip_path, wordlist_path, line_num)
                        print(f"Saved progress at line {line_num}")
                        return None
                
                try:
                    zip_file.extractall(pwd=password.encode())
                    print(f"Password found: {password}")
                    if os.path.exists("where.txt"):
                        os.remove("where.txt")
                    return password
                except:
                    continue
            
            print("Password not found in mask attack")
            if os.path.exists("where.txt"):
                os.remove("where.txt")
            return None

    except zipfile.BadZipFile:
        print("Error: Invalid zip file")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def dict_attack(zip_path, wordlist_path, start_line=0):
    if not os.path.exists(wordlist_path):
        print(f"Error: Wordlist file '{wordlist_path}' not found")
        return None
    
    try:
        with zipfile.ZipFile(zip_path) as zip_file:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            for i in range(start_line, len(lines)):
                password = lines[i].strip()
                if not password:
                    continue
                
                # Check if user pressed 'q'
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    key = sys.stdin.read(1)
                    print(f"Key pressed: {key}")
                    if key.lower() == 'q':
                        save_progress(zip_path, wordlist_path, i)
                        print(f"Saved progress at line {i}")
                        return None
                
                try:
                    zip_file.extractall(pwd=password.encode())
                    print(f"Password found: {password}")
                    if os.path.exists("where.txt"):
                        os.remove("where.txt")
                    return password
                except:
                    continue

            print("Password not found in wordlist")
            if os.path.exists("where.txt"):
                os.remove("where.txt")
            return None

    except zipfile.BadZipFile:
        print("Error: Invalid zip file")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def bomb_detection(zip_path):
    MAX_C_RATIO = 50
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
    if not file_names:
        print("No input files provided")
        return None
        
    MIN_PATTERN = 5
    MAX_PATTERN = 100
    compressed_size = 0
    original_size = 0
    binary_files = {} # store all of the files in binary with the key being file name
    all_patterns = {} # store every pattern found
    file_sizes = {} # store file sizes to write to the binary, used for decompressing
    compressed_files = {} # store the binaries for each file (compressed)
    for file in file_names:
        with open(file, 'rb') as f:
            binary_files[file] = f.read() # store as binary
    
    global_patterns = {}
    for file, binary in binary_files.items():
        for sequence_len in range(MIN_PATTERN, min(MAX_PATTERN, len(binary) + 1)):
            for i in range(len(binary) - sequence_len + 1):
                pattern = binary[i:i+sequence_len]
                if pattern not in global_patterns:
                    global_patterns[pattern] = []
                global_patterns[pattern].append((file, i)) # store the file name and the position for the pattern
    
    selected_patterns = {} # patterns used for compression later
    pid = 0 # counter
    for pattern, occurrences in global_patterns.items():
        total_occurrences = len(occurrences)
        pattern_length = len(pattern)
        space_saved = (total_occurrences * pattern_length) - (total_occurrences * 4) - pattern_length
        
        if space_saved > 0 and total_occurrences > 1:
            selected_patterns[pattern] = pid # assign a pattern id to a pattern if it saces space
            all_patterns[pid] = pattern
            pid += 1
            if pid >= 65536:  # Maximum number of patterns (2^16)
                break
    
    for file, binary in binary_files.items():
        new_data = binary
        
        sorted_patterns = sorted(selected_patterns.items(), key=lambda x: len(x[0]), reverse=True)
        
        for pattern, pattern_id in sorted_patterns:
            marker = b'\xFF\xFE' # marker for compressed patterns, acts like a flag 
            flag = marker + pattern_id.to_bytes(2, 'big')
            new_data = new_data.replace(pattern, flag)
        
        compressed_files[file] = new_data # store compressed result
        file_sizes[file] = len(new_data)
        original_size += len(binary)
        compressed_size += len(new_data)
    
    print(f'Original size: {original_size}')
    print(f'Compressed size: {compressed_size}')
    print(f'Compression ratio: {compressed_size/original_size:.2%}')
    print(f'Patterns used: {len(all_patterns)}')
    
    header_marker = b'\xFF\xFE\xFD\xFC' # marker for header data
    with open('compressed_output.bin', 'wb') as output_file:
        output_file.write(len(compressed_files).to_bytes(4, 'big')) # write No. of files
        for filename, compressed_data in compressed_files.items():
            output_file.write(len(filename.encode('utf-8')).to_bytes(2, 'big')) # file length
            output_file.write(filename.encode('utf-8')) # filename
            output_file.write(file_sizes[filename].to_bytes(4, 'big')) # size
        output_file.write(header_marker) # write the separator
        
        for filename, compressed_data in compressed_files.items():
            output_file.write(compressed_data)
    
    save_patterns(all_patterns) # save pattern dictionary, used when decompressing
    return compressed_files

def decompress_file(compressed_filename, pattern_dict):
    with open(compressed_filename, 'rb') as f:
        file_count = int.from_bytes(f.read(4), 'big')
        file_info = []
        # get file count, then for each file read the length of name, filename, and filesize
        for i in range(file_count):
            name_len = int.from_bytes(f.read(2), 'big')
            filename = f.read(name_len).decode('utf-8')
            file_size = int.from_bytes(f.read(4), 'big')
            file_info.append((filename, file_size))
        sep = f.read(4)
        # read the marker
        compressed_data = f.read()
    
    offset = 0
    for fname, fsize in file_info:
        # get the data for the current file
        file_data = compressed_data[offset:offset + fsize]
    
        result = bytearray()
        i = 0
        marker = b'\xFF\xFE'   
        while i < len(file_data): 
            if i + 1 < len(file_data) and file_data[i:i+2] == marker: # if encounters a marker
                if i + 3 < len(file_data):
                    pattern_id = int.from_bytes(file_data[i+2:i+4], 'big') # read the pattern id
                    if pattern_id in pattern_dict:
                        result.extend(pattern_dict[pattern_id]) # replace the pattern
                    i += 4 
                else:
                    result.append(file_data[i])
                    i += 1
            else:
                result.append(file_data[i])
                i += 1
        
        with open(fname, 'wb') as out_f:
            out_f.write(bytes(result))
        
        offset += fsize
        print(f'Decompressed: {fname}')


def save_patterns(pattern_dict):
    filename='patterns.bin'
    with open(filename, 'wb') as f:
        f.write(len(pattern_dict).to_bytes(4, 'big')) # write the length of dictionary
        for p_id, pattern in pattern_dict.items():
            f.write(p_id.to_bytes(2, 'big')) # write the pattern id
            f.write(len(pattern).to_bytes(4, 'big')) # write the length of the pattern
            f.write(pattern) # write the pattern

def load_patterns():
    filename='patterns.bin' # load the patterns based off of how they were added in save_patterns
    patterns = {}
    with open(filename, 'rb') as f:
        num_patterns = int.from_bytes(f.read(4), 'big')
        for _ in range(num_patterns):
            p_id = int.from_bytes(f.read(2), 'big')
            p_len = int.from_bytes(f.read(4), 'big')
            pattern = f.read(p_len)
            patterns[p_id] = pattern   
    return patterns

def main():
    if len(sys.argv) < 2:
        print("Usage: make wordlist <zip_file> <wordlist_file>")
        print("       make wordlist <zip_file> <wordlist_file> cont")
        print("       make mask <zip_file> <wordlist_file> <mask>")
        print("       make mask <zip_file> <wordlist_file> <mask> cont")
        print("       make brute <zip_file> <mask>")
        print("       make brute <zip_file> <mask> cont")
        print("       make detect_bomb <zip_file>")
        print("       make make_zip <file1> <file2>...")
        print("       make make_encrypted_zip <zip_file> <password> <file1> <file2>...")
        print("       make decompress <file.bin>")
        return 1
    
    if sys.argv[1] == 'wordlist':
        if len(sys.argv) < 4:
            print("Usage: make wordlist <zip_file> <wordlist_file> [cont]")
            return 1
        
        zip_file = sys.argv[2]
        wordlist_file = sys.argv[3]
        start_line = 0
        
        if len(sys.argv) == 5 and sys.argv[4] == 'cont':
            saved_zip, saved_wordlist, saved_line = load_progress()
            if saved_zip == zip_file and saved_wordlist == wordlist_file:
                start_line = saved_line
                print(f"Continuing from line {start_line}")
            else:
                print("No matching progress found, starting from beginning")
        
        dict_attack(zip_file, wordlist_file, start_line)
        
    elif sys.argv[1] == 'mask':
        if len(sys.argv) == 4:
            brute_mask(sys.argv[2], sys.argv[3])
        elif len(sys.argv) == 5:
            if sys.argv[4] == 'cont':
                zip_file = sys.argv[2]
                mask = sys.argv[3]
                start_index = 0
                
                saved_zip, saved_mask, saved_index = load_brute_progress()
                if saved_zip == zip_file and saved_mask == mask:
                    start_index = saved_index
                    print(f"Continuing brute force from combination {start_index}")
                else:
                    print("No matching brute force progress found, starting from beginning")
                
                brute_mask(zip_file, mask, start_index)
            else:
                mask_attack(sys.argv[2], sys.argv[3], sys.argv[4])
        elif len(sys.argv) == 6:
            if sys.argv[5] == 'cont':
                zip_file = sys.argv[2]
                wordlist_file = sys.argv[3] 
                mask = sys.argv[4]
                start_line = 0
                
                saved_zip, saved_wordlist, saved_line = load_progress()
                if saved_zip == zip_file and saved_wordlist == wordlist_file:
                    start_line = saved_line
                    print(f"Continuing mask attack from line {start_line}")
                else:
                    print("No matching progress found, starting from beginning")
                
                mask_attack(zip_file, wordlist_file, mask, start_line)
            else:
                print("Usage: make mask <zip_file> <mask>")
                print("   or: make mask <zip_file> <wordlist_file> <mask>") 
                print("   or: make mask <zip_file> <wordlist_file> <mask> cont")
                return 1
        else:
            print("Usage: make mask <zip_file> <mask>")
            print("   or: make mask <zip_file> <mask> cont")
            print("   or: make mask <zip_file> <wordlist_file> <mask>")
            print("   or: make mask <zip_file> <wordlist_file> <mask> cont")
            return 1
    elif sys.argv[1] == 'brute':
        if len(sys.argv) == 4:
            brute_mask(sys.argv[2], sys.argv[3])
        elif len(sys.argv) == 5 and sys.argv[4] == 'cont':
            zip_file = sys.argv[2]
            mask = sys.argv[3]
            start_index = 0
            
            # Check if continuing from saved progress
            saved_zip, saved_mask, saved_index = load_brute_progress()
            if saved_zip == zip_file and saved_mask == mask:
                start_index = saved_index
                print(f"Continuing brute force from combination {start_index}")
            else:
                print("No matching brute force progress found, starting from beginning")
            
            brute_mask(zip_file, mask, start_index)
        else:
            print("Usage: make brute <zip_file> <mask>")
            print("   or: make brute <zip_file> <mask> cont")
            return 1
    elif sys.argv[1] == 'make_bomb':
        if len(sys.argv) != 3:
            print('Usage: make make_bomb <zip_file>')
            return 1
        make_bomb(sys.argv[2])
    elif sys.argv[1] == 'detect_bomb':
        if len(sys.argv) != 3:
            print('Usage: make detect_bomb <zip_file>')
            return 1
        bomb_detection(sys.argv[2])
    elif sys.argv[1] == 'make_zip':
        if len(sys.argv) < 3:
            print('Usage: make make_zip <file1> <file2>...')
            return -1
        make_zip(sys.argv[2:])
    elif sys.argv[1] == 'decompress':
        if len(sys.argv) != 3:
            print('Usage: make decompress <file.bin>')
            return -1
        decompress_file(sys.argv[2], load_patterns())
    return 0

if __name__ == '__main__':
    main()