class LongestConsSequence:
    def longest_consecutive(self,nums):
        if not nums:
            return 0
        
        num_set = set(nums)
        longest_streak = 0
        
        for num in num_set:
            # Only start counting if `num - 1` is not in the set (start of a sequence)
            if num - 1 not in num_set:
                current_num = num
                current_streak = 1
                
                # Count the streak
                while current_num + 1 in num_set:
                    current_num += 1
                    current_streak += 1
                
                # Update the longest streak
                longest_streak = max(longest_streak, current_streak)
        
        return longest_streak

    
    def longest_cons_sequence(self,nums):
        snums = sorted(nums)
        max_cnt=1
        cnt=1
        prev = snums[0]
        for i in range(1,len(snums)):
            if snums[i]-prev==1:
                cnt+=1
            if cnt > max_cnt:
                max_cnt=cnt
            prev = snums[i]    
        return max_cnt            

    def main(self,nums):
        result = self.longest_consecutive(nums)
        print(result)
if __name__=="__main__":
    lcs = LongestConsSequence()
    lcs.main([0,3,7,2,5,8,4,6,0,1])        

            
