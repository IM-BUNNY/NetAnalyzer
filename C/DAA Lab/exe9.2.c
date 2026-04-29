#include <stdio.h>
#include <string.h>

// Function to find the longest palindromic substring
char* longestPalindrome(char* s) {
    int n = strlen(s);
    if (n == 0) return "";

    int start = 0, maxLength = 1;
    int dp[n][n];

    // Initialize the table
    memset(dp, 0, sizeof(dp));

    // All substrings of length 1 are palindromes
    for (int i = 0; i < n; i++) {
        dp[i][i] = 1;
    }

    // Check for substrings of length 2
    for (int i = 0; i < n - 1; i++) {
        if (s[i] == s[i + 1]) {
            dp[i][i + 1] = 1;
            start = i;
            maxLength = 2;
        }
    }

    // Check for lengths greater than 2
    for (int len = 3; len <= n; len++) {
        for (int i = 0; i < n - len + 1; i++) {
            int j = i + len - 1;
            if (s[i] == s[j] && dp[i + 1][j - 1]) {
                dp[i][j] = 1;
                start = i;
                maxLength = len;
            }
        }
    }

    // Extract the longest palindromic substring
    static char result[1000];
    strncpy(result, s + start, maxLength);
    result[maxLength] = '\0';
    return result;
}

int main() {
    char s1[] = "bananas";
    char s2[] = "abdcbcdbdcbbc";
    char s3[] = "abracadabra";
    char s4[] = "cbbd";

    printf("Input: %s\nOutput: %s\n", s1, longestPalindrome(s1));
    printf("Input: %s\nOutput: %s\n", s2, longestPalindrome(s2));
    printf("Input: %s\nOutput: %s\n", s3, longestPalindrome(s3));
    printf("Input: %s\nOutput: %s\n", s4, longestPalindrome(s4));

    return 0;
}