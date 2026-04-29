#include <stdio.h>
#include <limits.h>

// Recursive function (Divide and Conquer)
int minCoinsRecursive(int coins[], int n, int amount) {
    if (amount == 0) return 0;  
    if (amount < 0) return INT_MAX;
    int minCoins = INT_MAX;

    for (int i = 0; i < n; i++) {
        int res = minCoinsRecursive(coins, n, amount - coins[i]);

        if (res != INT_MAX && res + 1 < minCoins)
            minCoins = res + 1;
    }

    return minCoins;
}

int main() {
    int coins[] = {1, 2, 5};
    int amount;
    int n = sizeof(coins) / sizeof(coins[0]);

    printf("Enter the amount: ");
    scanf("%d", &amount);

    int result = minCoinsRecursive(coins, n, amount);
    if (result == INT_MAX)
        printf("Amount cannot be formed using given coins\n");
    else
        printf("Minimum coins required: %d\n", result);

    return 0;
}
