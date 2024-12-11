from collections import Counter
class LongestSubstring:
    def has_duplicate(self,duplicate_string):
        seen = set()
        for c in duplicate_string:
            if c in seen:
                return True
            seen.add(c)
        return False    



    def longest_substring(self,longest_string):
        max_longest=""
        c=""
        for i in range(len(longest_string)):
            c = c+''+longest_string[i]
            if(self.has_duplicate(c+"")):
                c = c[1:]
            if(len(c)>len(max_longest)):
                max_longest = c    
        return len(max_longest)
    
    def main(self):
        result = self.longest_substring("abcabcbb")
        print(result)

if __name__=="__main__":
    lss = LongestSubstring()
    lss.main()