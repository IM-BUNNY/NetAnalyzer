#include <stdio.h>
#include <string.h>

// Function to find LCS length of three sequences
int LCS3(char X[], char Y[], char Z[]) {
    int m = strlen(X), n = strlen(Y), o = strlen(Z);
    int dp[m + 1][n + 1][o + 1]; // 3D DP table

    // Initialize the DP table
    for (int i = 0; i <= m; i++)
        for (int j = 0; j <= n; j++)
            for (int k = 0; k <= o; k++)
                dp[i][j][k] = 0;  // Base case: LCS of empty strings is 0

    // Fill the DP table using Bottom-Up approach
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            for (int k = 1; k <= o; k++) {
                if (X[i - 1] == Y[j - 1] && Y[j - 1] == Z[k - 1]) {
                    dp[i][j][k] = dp[i - 1][j - 1][k - 1] + 1;  // If characters match
                } else {
                    dp[i][j][k] = 
                        (dp[i - 1][j][k] > dp[i][j - 1][k]) ? 
                        ((dp[i - 1][j][k] > dp[i][j][k - 1]) ? dp[i - 1][j][k] : dp[i][j][k - 1]) : 
                        ((dp[i][j - 1][k] > dp[i][j][k - 1]) ? dp[i][j - 1][k] : dp[i][j][k - 1]); 
                }
            }
        }
    }

    return dp[m][n][o];  // The final answer
}

// Driver Code
int main() {
    char X[] = "ABCBDAB";
    char Y[] = "BDCABA";
    char Z[] = "BADACB";

    printf("Length of Longest Common Subsequence: %d\n", LCS3(X, Y, Z));  
    // Expected Output: 4 (BDAB)

    return 0;
}
