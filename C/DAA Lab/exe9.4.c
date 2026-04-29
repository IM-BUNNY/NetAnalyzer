#include <stdio.h>
#include <string.h>

// Function to find the length of the longest palindromic subsequence
int LPS(char s[]) {
    int n = strlen(s);
    int dp[n][n];  // DP table

    // Fill the DP table
    for (int i = n - 1; i >= 0; i--) {  // Bottom-up approach
        dp[i][i] = 1;  // A single character is a palindrome of length 1
        for (int j = i + 1; j < n; j++) {
            if (s[i] == s[j]) {
                dp[i][j] = dp[i + 1][j - 1] + 2;  // Expand palindrome
            } else {
                dp[i][j] = (dp[i + 1][j] > dp[i][j - 1]) ? dp[i + 1][j] : dp[i][j - 1];
            }
        }
    }

    return dp[0][n - 1];  // The result is stored in dp[0][n-1]
}

// Driver Code
int main() {
    char str[] = "ABBDCACB";
    printf("Length of Longest Palindromic Subsequence: %d\n", LPS(str));
    // Expected Output: 5 (BCACB)

    return 0;
}
