#include<stdio.h>
#include<limits.h>
#define MAX 1000

int coinChange(int coins[], int n, int sum, int dp[]) 
{
    if (sum == 0) return 0;
    if (sum < 0) return INT_MAX;
    if (dp[sum] != -1) return dp[sum];

    int minCoins = INT_MAX;
    for (int i = 0; i < n; i++) 
    {
        int res = coinChange(coins, n, sum - coins[i], dp);
        if (res != INT_MAX) 
        {
            minCoins = (res + 1 < minCoins) ? res + 1 : minCoins;
        }
    }
    dp[sum] = minCoins;
    return minCoins;
}

int main ()
{
    int coins[]= {1,2,5,10};
    int sum ;
    int n = sizeof(coins) / sizeof(coins[0]);

    printf("Enter the amount you want : ");
    scanf("%d", &sum);
    if (sum < 0) 
    {
        printf("Not possible\n");
        return 0;
    }

    int dp[MAX];
    for (int i = 0; i <= sum; i++) 
    {
        dp[i] = -1;
    }
    int result = coinChange(coins, n, sum, dp);
    if (result == INT_MAX) 
    {
        printf("Not possible\n");
    } 
    else 
    {
        printf("Minimum coins required (Recursion + Memoization): %d\n", result);
    }
    return 0;
}