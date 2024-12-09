class container_most_water:
    def container_with_most_water(self,nums):
        left=0
        right=len(nums)-1
        max_area=0
        while(left<right):
            height = min(nums[left],nums[right])
            width = right-left
            area = height*width
            max_area=max(max_area,area)
            if(nums[left]<nums[right]):
                left+=1
            else:
                right-=1    
        return max_area     
    def main(self):
        result = self.container_with_most_water([8,7,2,1])
        print(result)

if __name__=="__main__":
    cmw = container_most_water()
    cmw.main()        