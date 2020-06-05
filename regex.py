"""" main.py
*   Author : Yvain RAYNAUD
*   Date : 05/06/2020
*   Object : file for all regex related function
"""

import re


def getDateDoc(text):
    """
    Try to return probable date or null if not exist
    :param text: str
    Date format " DD/MM/AAAA" with  01 ≤ DD ≤ 31,  01 ≤ MM ≤ 12 and 2000 ≤ AAAA ≤ 2049
    """
    #removing weird tuple https://stackoverflow.com/questions/24593824/why-does-re-findall-return-a-list-of-tuples-when-my-pattern-only-contains-one-gr
    res = ["".join(x) for x in re.findall(r'([0-3][0-9]\/0[0-9]\/20[0-9]{2,})|([0-3][0-9]\/1[0-2]\/20[0-5][0-9])', text)]
    if (not res):
        return None
    else:
        return res[0]

def getAuthor(text):
    """
    Try to return probable Author or null  if not exist
    :param text: str
    last pattern of "dr". + str + endline 
    """
    #removing weird tuple https://stackoverflow.com/questions/24593824/why-does-re-findall-return-a-list-of-tuples-when-my-pattern-only-contains-one-gr
    res = ["".join(x) for x in re.findall(r'(?i)\bdr[ \.].{3,}\b', text)]
    if (not res):
        return None
    else :
        return res[-1] #last elem of the array