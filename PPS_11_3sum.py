class Solution:    
    
        

    def three_sum(self,nums):
        # Sort the input array
        nums.sort()
        result = []
        
        # Iterate through the array
        for i in range(len(nums)):
            # Avoid duplicates for the first number
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            
            # Two-pointer approach for the rest of the numbers
            left, right = i + 1, len(nums) - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                
                if total == 0:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    
                    # Avoid duplicates for the second and third numbers
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                
                elif total < 0:
                    left += 1  # Need a larger sum
                else:
                    right -= 1  # Need a smaller sum
        
        return result


    def main(self):
        result_3 = self.three_sum([-1,0,1,2,-1,-4])
        print(result_3)



if __name__=="__main__":
    sol = Solution()
    sol.main()
