# scripts
Scripts for handy tasks

ExtractInfoFromFile
To get desired columns from a file into another one based on seleceted column matches.

usage: ExtractInfoFromFile.py [-h] -f1 F1 -f2 F2 [-fo FO] [-sep SEP]
                              [--cols_f1 COLS_F1] [--cols_f2 COLS_F2]
                              [--cols_to_extract_from_f2 COLS_TO_EXTRACT_FROM_F2]
                              

Get colums from the second file for the first file


optional arguments:

  -h, --help            show this help message and exit
  
  -f1 F1                the file that lacks the ID column
  
  -f2 F2                the file that has the ID column
  
  -fo FO                output file name
  
  -sep SEP              split character
  
  --cols_f1 COLS_F1     index of columns to consider to match from file 1. For
                        example to consider chromsome and position write 0,1
                        
  --cols_f2 COLS_F2     index of columns to consider to match from file 1, it
                        should have the same number of columns as cols_f1
                        
  --cols_to_extract_from_f2 COLS_TO_EXTRACT_FROM_F2
  
                        index of the columns to be extracted from file 2 and
                        added to the matches in file1, to just get id from the
                        second file write 2
                        

