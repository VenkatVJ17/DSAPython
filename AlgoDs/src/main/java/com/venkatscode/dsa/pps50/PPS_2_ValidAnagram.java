package com.venkatscode.dsa.pps50;

import java.util.HashMap;
import java.util.Map;

public class PPS_2_ValidAnagram {

    public static void main(String[] args) {
        System.out.println(validAnagram("anagram","nagaram"));
        System.out.println(validAnagram("cat","car"));
    }

    private static boolean validAnagram(String s1, String s2) {
        if(s1.length()!=s2.length()){
            return false;
        }else{
            return charCountMap(s1).equals(charCountMap(s2));
        }
    }

    private static Map<Character,Integer> charCountMap(String s1) {
        Map<Character,Integer> charMap = new HashMap<>();
        for(char chr: s1.toCharArray()){
            charMap.put(chr,charMap.getOrDefault(chr,0)+1);
        }
        return charMap;
    }
}
