#include <stdio.h>
#include <limits.h>
#include <time.h> // For time measurement

// Function to perform Matrix Chain Multiplication using Dynamic Programming
int matrixChainMultiplication(int arr[], int n) {
    int dp[n][n]; // Table to store the minimum number of multiplications
    
    // Initialize diagonal elements to 0 (single matrix multiplication cost is 0)
    for (int i = 1; i < n; i++)
        dp[i][i] = 0;

    // L is the chain length
    for (int L = 2; L < n; L++) { 
        for (int i = 1; i < n - L + 1; i++) {
            int j = i + L - 1;
            dp[i][j] = INT_MAX;

            // Try different places to split the product
            for (int k = i; k < j; k++) {
                int cost = dp[i][k] + dp[k + 1][j] + arr[i - 1] * arr[k] * arr[j];

                // Store the minimum cost
                if (cost < dp[i][j])
                    dp[i][j] = cost;
            }
        }
    }

    return dp[1][n - 1]; // Return the minimum multiplication cost
}

int main() {
    // Matrix dimensions array
    int arr[] = {40, 20, 30, 10, 30};  
    int n = sizeof(arr) / sizeof(arr[0]); // Number of matrices = n-1

    // Measure execution time
    clock_t start, end;
    start = clock();

    // Compute the minimum cost of matrix multiplication
    int minCost = matrixChainMultiplication(arr, n);

    end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    // Output the results
    printf("Minimum number of multiplications: %d\n", minCost);
    printf("Time taken: %f seconds\n", time_taken);

    return 0;
}
