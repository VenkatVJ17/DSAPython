from collections import Counter

def check_valid_anagram(s1,s2):
    if(len(s1)!=len(s2)):
        return False
    else:
        return Counter(s1)==Counter(s2)

def group_anagrams(strlist) -> list[list[str]]:
    listofstrings=[]
    listoflistofstrings=[]
    for i in range(0,len(strlist)):
        listofstrings.append(strlist[i])
        for j in range(1,len(strlist)):
            if(check_valid_anagram(strlist[i],strlist[j])):
                listofstrings.append(strlist[j])
        listoflistofstrings.append(listofstrings) 
        listofstrings=[]   
    return listoflistofstrings

from collections import defaultdict

def group_anagrams_updated(strlist):
    anagrams = defaultdict(list)
    for word in strlist:
        # Use the sorted word as a key to group anagrams
        sorted_word = "".join(sorted(word))
        anagrams[sorted_word].append(word)
    return list(anagrams.values())

def main():
    print(group_anagrams_updated(["eat","tea","tan","ate","nat","bat"]))

if __name__=="__main__":
    main()