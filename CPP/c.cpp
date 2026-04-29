#include<iostream>
#include<vector>
#include<algorithm>
#include<climits>

using namespace std;

class CoinExchangeDivideAndConquer {
public:
    CoinExchangeDivideAndConquer(const vector<int>& coins) {
        this->coins = coins;
        sort(this->coins.begin(), this->coins.end(), greater<int>());
    }
    int exchange(int amount) {
        int count = 0;
        for (int coin : coins) {
            count += amount / coin;
            amount %= coin;
        }
        return (amount != 0) ? -1 : count;
    }
private:
    vector<int> coins;
};

class CoinExchangeRecursive {
public:
    CoinExchangeRecursive(const vector<int>& coins) : coins(coins) {}
    int exchange(int amount) {
        int result = exchangeHelper(amount);
        return (result == INT_MAX) ? -1 : result;
    }
private:
    vector<int> coins;
    int exchangeHelper(int amount) {
        if (amount == 0)
            return 0;
        if (amount < 0)
            return INT_MAX;
        int minCoins = INT_MAX;
        for (int coin : coins) {
            int res = exchangeHelper(amount - coin);
            if (res != INT_MAX) {
                minCoins = min(minCoins, res + 1);
            }
        }
        return minCoins;
    }
};

class CoinExchangeDP {
public:
    CoinExchangeDP(const vector<int>& coins) : coins(coins) {}
    int exchange(int amount) {
        vector<int> dp(amount + 1, INT_MAX);
        dp[0] = 0;
        for (int i = 1; i <= amount; i++) {
            for (int coin : coins) {
                if (i - coin >= 0 && dp[i - coin] != INT_MAX) {
                    dp[i] = min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        return dp[amount] == INT_MAX ? -1 : dp[amount];
    }
private:
    vector<int> coins;
};

int main() {
    int n, amount;
    cout << "Enter number of coin denominations: ";
    cin >> n;
    
    vector<int> coins(n);
    cout << "Enter coin denominations separated by space: ";
    for (int i = 0; i < n; i++) {
        cin >> coins[i];
    }
    
    cout << "Enter target amount: ";
    cin >> amount;
    
    CoinExchangeDivideAndConquer coinDC(coins);
    int resultDC = coinDC.exchange(amount);
    cout << "Divide and Conquer (Greedy) result: " << resultDC << "\n";
    
    CoinExchangeRecursive coinRec(coins);
    int resultRec = coinRec.exchange(amount);
    cout << "Recursive result: " << resultRec << "\n";
    
    CoinExchangeDP coinDP(coins);
    int resultDP = coinDP.exchange(amount);
    cout << "Dynamic Programming result: " << resultDP << "\n";
    
    return 0;
}