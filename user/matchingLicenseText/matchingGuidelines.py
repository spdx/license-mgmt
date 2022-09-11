# Copyright 2022 Rohan Chandrashekar
# SPDX-License-Identifier:  MIT
'''Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.'''

import re

#SPDX License List Matching Guidelines, v2.1
def matchLicenses(licenseText):


    #Removing the whitespaces form the ends of the text
    licenseText = licenseText.strip()
    
    #Guideline-8: Varietal Word Spelling
    with open('user\matchingLicenseText\equivalentWords.txt') as f:
        lines = f.readlines()
        for line in lines:
          licenseText = re.sub(line.split(",")[0], line.split(",")[1], licenseText)

    #Guideline-3: Whitespaces
    licenseText = re.sub(r"[\n\t\s]+", " ", licenseText)
    
    #Guideline-4: Capitalization
    licenseText = licenseText.lower()
    
    #Guideline-5.1.3: Quotes  
    licenseText = re.sub(r"\"", "'", licenseText)

    #Guideline-5.1.2:  Hyphens, Dashes  Any hyphen, dash, en dash, em dash, or other variation should be considered equivalent.
    licenseText = re.sub(r"–", "-", licenseText)
    licenseText = re.sub(r"—", "-", licenseText)

    #Guideline-9: Copyright Symbol  
    licenseText = re.sub(r"©", "copyright", licenseText)
    licenseText = re.sub(r"(c)", "copyright", licenseText)

    #Guideline-10: HTTP Protocol  
    licenseText = re.sub(r"http://", "https://", licenseText)

    return(licenseText)
    
    