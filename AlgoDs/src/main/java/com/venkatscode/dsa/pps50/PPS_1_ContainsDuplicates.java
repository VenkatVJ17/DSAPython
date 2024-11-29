package com.venkatscode.dsa.pps50;

import java.util.HashSet;

public class PPS_1_ContainsDuplicates {

    public static void main(String[] args) {
        int[] intarr = {1,3,4,4,5,5,6};
        containsDuplicates(intarr);
    }

    private static void containsDuplicates(int[] intarr) {
        HashSet<Integer> uniqueSet = new HashSet<Integer>();
        HashSet<Integer> duplicateSet = new HashSet<Integer>();
        for(int elment: intarr){
            if(!uniqueSet.contains(elment)){
                uniqueSet.add(elment);
            }else{
                duplicateSet.add(elment);
            }
        }
        System.out.println(duplicateSet);
    }
}
