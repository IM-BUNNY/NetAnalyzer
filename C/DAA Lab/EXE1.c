#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

// Divide and Conquer (Greedy) approach
int coinExchangeDC(int coins[], int n, int amount) {
    int count = 0;
    for (int i = 0; i < n; i++) {
        count += amount / coins[i];
        amount %= coins[i];
    }
    return (amount != 0) ? -1 : count;
}

// Recursive approach to find the minimum number of coins
int coinExchangeRecHelper(int coins[], int n, int amount) {
    if (amount == 0) return 0;
    if (amount < 0) return INT_MAX;

    int minCoins = INT_MAX;
    for (int i = 0; i < n; i++) {
        int res = coinExchangeRecHelper(coins, n, amount - coins[i]);
        if (res != INT_MAX) {
            minCoins = (res + 1 < minCoins) ? res + 1 : minCoins;
        }
    }
    return minCoins;
}

int coinExchangeRec(int coins[], int n, int amount) {
    int result = coinExchangeRecHelper(coins, n, amount);
    return (result == INT_MAX) ? -1 : result;
}

// Dynamic Programming approach
int coinExchangeDP(int coins[], int n, int amount) {
    int dp[amount + 1];
    for (int i = 0; i <= amount; i++)
        dp[i] = INT_MAX;
    
    dp[0] = 0; // Base case

    for (int i = 1; i <= amount; i++) {
        for (int j = 0; j < n; j++) {
            if (i >= coins[j] && dp[i - coins[j]] != INT_MAX) {
                if (dp[i - coins[j]] + 1 < dp[i])
                    dp[i] = dp[i - coins[j]] + 1;
            }
        }
    }
    
    return (dp[amount] == INT_MAX) ? -1 : dp[amount];
}

int main() {
    int n, amount;

    printf("Enter number of coin denominations: ");
    scanf("%d", &n);

    int coins[n];
    printf("Enter coin denominations separated by space: ");
    for (int i = 0; i < n; i++) {
        scanf("%d", &coins[i]);
    }

    printf("Enter target amount: ");
    scanf("%d", &amount);

    // Sort coins in descending order for Greedy approach
    for (int i = 0; i < n - 1; i++) {
        for (int j = i + 1; j < n; j++) {
            if (coins[i] < coins[j]) {
                int temp = coins[i];
                coins[i] = coins[j];
                coins[j] = temp;
            }
        }
    }

    int resultDC = coinExchangeDC(coins, n, amount);
    printf("Divide and Conquer (Greedy) result: %d\n", resultDC);

    int resultRec = coinExchangeRec(coins, n, amount);
    printf("Recursive result: %d\n", resultRec);

    int resultDP = coinExchangeDP(coins, n, amount);
    printf("Dynamic Programming result: %d\n", resultDP);

    return 0;
}
