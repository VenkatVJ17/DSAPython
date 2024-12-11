"""
Problem Description:
You are given an array of integers, arr, containing n elements. Your task is to identify all the elements that appear more than once in the array. 
If no duplicates exist, return an empty list.

Input:

An array of integers, arr, of size n where 1 ≤ n ≤ 10^5.
The integers in the array can be both positive and negative and lie in the range -10^6 ≤ arr[i] ≤ 10^6.
Output:

A list of integers representing the duplicate elements in the array.
The output list can be in any order, but each duplicate element should appear only once in the output.
Input: arr = [1, 1, 2]
Output: [1]
Explanation: Only 1 appears more than once in the array.

"""
def containsDuplicatesUsingSet(intarr):
    uniqueElements = set()
    duplicateElements = set()
    for i in intarr:
        if i not in uniqueElements:
            uniqueElements.add(i)
        else:
            duplicateElements.add(i)
    print(duplicateElements)        

def containsDuplicates(intarr):
    myDict = {}
    for i in range(len(intarr)):
        if intarr[i] in myDict:
            myDict[intarr[i]]=myDict[intarr[i]]+1
        else:
            myDict[intarr[i]]=1    
    duplicates = [key for key, value in myDict.items() if value > 1]
    print(duplicates)

def main():
    # Sample input list
    intarr = [1, 2, 3, 4, 5, 5,4,2]
    containsDuplicatesUsingSet(intarr)

if __name__=="__main__":
    main()