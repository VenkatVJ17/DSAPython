from collections import Counter
"""
Problem Statement:

Given two strings s and t, write a function to determine if t is an anagram of s.

An anagram is a word or phrase formed by rearranging the letters of a different word or phrase, using all the original letters exactly once.

Constraints:

The strings s and t consist of lowercase English letters.
The lengths of s and t may vary.

Input:
s = "anagram"
t = "nagaram"

Output: True

Input:
s = "rat"
t = "car"

Output: False

"""

def validAnagramImproved(s1,s2):
    if len(s1) != len(s2):
        return False
    return Counter(s1) == Counter(s2)

def validAnagram(s1,s2):
    s1dict = Counter(s1)
    for char in s2:
        if char in s1dict:
            s1dict[char]-= 1
        else:
            return False
    return True        

def main():
    print(validAnagramImproved("anagram","nagaram"))
    print(validAnagramImproved("car","cat"))

if __name__=="__main__":
    main()
