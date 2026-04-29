#include <stdio.h>
#include <limits.h>
#include <string.h>

#define MAX_AMOUNT 1000

// Memoization table
int dp[MAX_AMOUNT];

// Recursive function with memoization
int minCoinsMemoized(int coins[], int n, int amount) {
    if (amount == 0) return 0;
    if (amount < 0) return INT_MAX;

    if (dp[amount] != -1) return dp[amount];

    int minCoins = INT_MAX;

    for (int i = 0; i < n; i++) {
        int res = minCoinsMemoized(coins, n, amount - coins[i]);

        if (res != INT_MAX && res + 1 < minCoins)
            minCoins = res + 1;
    }

    return dp[amount] = minCoins;
}

// Driver code
int main() {
    int coins[] = {1, 2, 5,10};
    int amount;
    int n = sizeof(coins) / sizeof(coins[0]);

    printf("Enter the amount: ");
    scanf("%d", &amount);
    memset(dp, -1, sizeof(dp));  
    int result = minCoinsMemoized(coins, n, amount);
    if (result == INT_MAX)
        printf("Amount cannot be formed using given coins\n");
    else
        printf("Minimum coins required (Memoized DP): %d\n", result);

    return 0;
}
