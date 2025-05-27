[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/am3xLbu5)
# ZIP Password Cracker

### Team: The_Girl_And_Her_Pigs
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
   Example: `make wordlist ARGS="protected.zip passwords.txt"`

2. **Mask Attack with Wordlist**
   ```bash
   make mask ARGS="<zip_file> <wordlist_file> <mask>"
   ```
   Example: `make mask ARGS="protected.zip passwords.txt "mask"`

3. **Brute Force Mask Attack**
   ```bash
   make mask ARGS="<zip_file> <mask>"
   ```
   Example: `make mask ARGS="protected.zip "mask"`

4. **ZIP Bomb Detection**
   ```bash
   make detect_bomb ARGS="<zip_file>"
   ```
   Example: `make detect_bomb ARGS="suspicious.zip"`

### Resources & References

- [Python ZIP File Documentation](https://docs.python.org/3/library/zipfile.html)
- [Understanding ZIP Bombs](https://www.microsoft.com/en-us/windows/learning-center/what-is-a-zip-bomb)