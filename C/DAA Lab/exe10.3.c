#include <stdio.h>
#include <limits.h>

#define MAX 1000

// Bottom-Up DP Approach
int coinChange_DP(int coins[], int n, int sum) {
    int dp[MAX];

    // Initialize the dp array with a high value
    for (int i = 0; i <= sum; i++) {
        dp[i] = INT_MAX;
    }
    dp[0] = 0; // Base case: 0 coins needed to make sum 0

    // Fill the dp table
    for (int i = 1; i <= sum; i++) {
        for (int j = 0; j < n; j++) {
            if (coins[j] <= i && dp[i - coins[j]] != INT_MAX) {
                dp[i] = (dp[i - coins[j]] + 1 < dp[i]) ? dp[i - coins[j]] + 1 : dp[i];
            }
        }
    }

    return (dp[sum] == INT_MAX) ? -1 : dp[sum];
}

int main() {
    int coins[] = {1,2,5,10}; 
    int sum = 6;
    int n = sizeof(coins) / sizeof(coins[0]);

    int result = coinChange_DP(coins, n, sum);
    if (result == -1) {
        printf("Not possible\n");
    } else {
        printf("Minimum coins required (DP): %d\n", result);
    }
    return 0;
}
