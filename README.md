[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/am3xLbu5)

### Video Demo: https://drive.google.com/file/d/1dYn4qY5XWoaQSWWmF3e-PHS8URLRdvPH/view?usp=sharing

### Team: The_Decompressors
- Benjamin Goihman
- Andrew Choi
- Michelle Zhu
       
### Project Description

A powerful Python-based ZIP archive password cracking tool that provides multiple methods to recover passwords from protected archives. The tool is designed to be both efficient and user-friendly, offering various attack methods:
1. Wordlist attack with logging and various wordlist formats  
2. Mask attacks, which will allow for patterns to crack passwords  
3. ZIP bomb detection, analyzing compression ratios and detect archive structures
4. Additional features like protecting zip archives and support for other archive formats  
This would be run through the command line, with options in the README.
  
### Instructions:

#### Installation
1. Ensure you have Python 3.x installed on your system
2. Clone this repository:
   ```bash
   git clone git@github.com:Stuycs-K/finalproject-09-goihman-ben-choi-andrew-zhu-michelle.git
   cd finalproject-09-goihman-ben-choi-andrew-zhu-michelle
   ```
3. No additional dependencies are required as the program uses Python's built-in libraries

### Usage

The program provides several attack methods through a simple command-line interface:

1. **Wordlist Attack**
   ```bash
   make wordlist ARGS="<zip_file> <wordlist_file>"
   ```
   Example: `make wordlist ARGS="demo/test.zip demo/passwords.txt"`

2. **Mask Attack with Wordlist**
   ```bash
   make mask ARGS="<zip_file> <wordlist_file> <mask>"
   ```
   Example: `make mask ARGS="demo/test.zip demo/passwords.txt areallycoollongpassw___"`

3. **Brute Force Mask Attack**
   ```bash
   make mask ARGS="<zip_file> <mask>"
   ```
   Example: `make mask ARGS="demo/test.zip areallycoollongpasswor_"`

4. **Dedicated Brute Force Attack**
   ```bash
   make brute ARGS="<zip_file> <mask>"
   ```
   Example: `make brute ARGS="demo/test.zip areallycoollongpasswor_"`

5. **ZIP Bomb Detection**
   ```bash
   make detect_bomb ARGS="<zip_file>"
   ```
   Example: `make detect_bomb ARGS="demo/bomb.zip"`

6. **ZIP Bomb Maker**
    ```bash
   make make_bomb ARGS="<zip_file>"
   ```
   Example: `make make_bomb ARGS="demo/bomb1.zip"`

7. **Custom Compression**
    ```bash
   make make_zip ARGS="<file1> <file2> ..."
   ```
   Example: `make make_zip ARGS="demo/test1.txt demo/test2.txt demo/bigfile.txt"`
   This will create:
   - `compressed_output.bin`: The compressed data
   - `patterns.bin`: The pattern dictionary used for compression

8. **Custom Decompression**
    ```bash
   make decompress ARGS="<compressed_file>"
   ```
   Example: `make decompress ARGS="compressed_output.bin"`
   Note: Requires `patterns.bin` to be present in the same directory
   Note: The default output for this is compressed_output.bin, so the argument should always be compressed_output.bin unless the name is changed.

### Continuation Feature

All attack methods support resuming from where they left off if interrupted:

- **Continue Wordlist Attack**: `make wordlist ARGS="<zip_file> <wordlist_file> cont"`
  Example: `make wordlist ARGS="demo/test.zip demo/rockyou.txt cont"`
  For this one rockyou.txt must be downloaded and you have to add areallycoollongpassword around the 100k line, can not add to git due to file size

- **Continue Mask Attack**: `make mask ARGS="<zip_file> <wordlist_file> <mask> cont"`
  Example: `make mask ARGS="demo/test.zip demo/passwords.txt areallycoollongpassw___ cont"`

- **Continue Brute Force**: `make brute ARGS="<zip_file> <mask> cont"`
  Example: `make brute ARGS="demo/test.zip areallycoollongpasswor_ cont"`

**How it works:**
- Press 'q' during any attack to save progress and exit
- Use the `cont` parameter to resume from the saved position
- Progress is automatically saved to `where.txt` (wordlist/mask attacks) or `brute_where.txt` (brute force attacks)
- Progress files are automatically cleaned up when attacks complete successfully

### Resources & References

1. Python Standard Libraries
- [zipfile](https://docs.python.org/3/library/zipfile.html) - For handling ZIP archive operations
- [os](https://docs.python.org/3/library/os.html) - For file system operations
- [sys](https://docs.python.org/3/library/sys.html) - For command-line argument handling
- [itertools](https://docs.python.org/3/library/itertools.html) - For password generation and combinations
- [string](https://docs.python.org/3/library/string.html) - For character set operations
- [subprocess](https://docs.python.org/3/library/subprocess.html) - For running commands in test suite
- [tempfile](https://docs.python.org/3/library/tempfile.html) - For temporary file operations in testing
- [select](https://docs.python.org/3/library/select.html) - For waiting for user input without blocking the main attack loop
- [signal](https://docs.python.org/3/library/signal.html) - For handling ctrl c
2. External Resources
- [Understanding ZIP Bombs](https://www.microsoft.com/en-us/windows/learning-center/what-is-a-zip-bomb) - For ZIP bomb detection and creation features
- [GNU Make Manual](https://www.gnu.org/software/make/manual/make.html) - For command-line interface implementation
- [How to get stdin data](https://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data) - For reading stdin data during execution
- [Make password protected zip file](https://discussions.apple.com/thread/255212512?sortBy=rank) - For testing & demo