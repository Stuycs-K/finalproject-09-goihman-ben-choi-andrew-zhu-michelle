# Final Project Proposal

## Group Members:

Benjamin Goihman, Andrew Choi, Michelle Zhu

# Intention:

We plan on making a cybersecurity tool in python for zips. This will include, a zip file dictionary attack, a zip file mask attack, zip bomb detection, and a zip bomb makers.    
# Intended usage:

It will be used through the terminal, with different make commands to use the different features.
  
# Technical Details:

It will be a python program that will use the zipfile library to create the different features. We will be using the argparse library to create the different commands. We will be using the os library to navigate the file system. We will be 

A description of your technical design. This should include: 
   
Dictionary attack: simple for loop through wordlist and try to extract with password
Mask attack: same as above but only try the passwords that match the mask, mask will be defined by a string of underscores (which represents a wildcard), then letters will be used to represent the characters that are known. For example _____ is any password with 5 characters. While b___a is any password with 5 characters that starts with b and ends with a.
Zip bomb: 
How you will be using the topics covered in class in the project.
     
How you are breaking down the project and who is responsible for which parts.
  
    
# Intended pacing:

5/19 - setup make and finish proposal
5/21 - zip file dictionary attack
5/25 - zip file mask attack
