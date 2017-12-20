# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 20:52:51 2017

@author: Alexander
"""
#!/usr/bin/env python3
###
def string_switch(file_name,old_words,new_words,switch_option=1):
    with open(file_name, "r", encoding="utf-8") as file_open:
        #readlines in the form of list
        lines = file_open.readlines()
 
    with open(file_name, "w", encoding="utf-8") as file_write:
        # define a number to indicate where it is in the file
        line_number = 0
        # default option, only replace the first 
        if switch_option == 1:
            for line in lines:
                if old_words in line:
                    line = line.replace(old_words,new_words)
                    file_write.write(line)
                    line_number += 1
                    break
                file_write.write(line)
                line_number += 1
            # output the residue file
            for i in range(line_number,len(lines)):
                file_write.write(lines[i])
        # global match and replace
        elif switch_option == 'g':
            for line in lines:
                if old_words in line:
                    line = line.replace(old_words, new_words)
                file_write.write(line)

def main():
    print(r'!')
    

if __name__ == "__main__":
    main()