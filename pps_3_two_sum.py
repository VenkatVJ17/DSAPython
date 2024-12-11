def two_sum(nums, target):
    # Create a dictionary to store numbers and their indices
    num_to_index = {}
    
    # Iterate through the list
    for i, num in enumerate(nums):
        # Calculate the complement
        complement = target - num
        
        # Check if the complement exists in the dictionary
        if complement in num_to_index:
            # Return the indices of the two numbers
            return [num_to_index[complement], i]
        
        # Otherwise, add the current number to the dictionary
        num_to_index[num] = i
                


def main():
    result = two_sum([3,2,4],6)
    print(result)


if __name__=="__main__":
    main()        