class Solution:
    def valid_palindrome(self,s):
        newstr=""
        lowertext = s.lower()
        for c in lowertext:
            if (c >= 'a' and c<= 'z') or (c>='0' and c<='9'):
                newstr = newstr+c
        n = len(newstr)
        for i in range(n//2):
            if newstr[i]!= newstr[n-i-1]:
                return False
        return True    

    def main(self):
        test_str = "0P"
        result = self.valid_palindrome(test_str)
        print(result)

if __name__=="__main__":
    solution = Solution()
    solution.main()