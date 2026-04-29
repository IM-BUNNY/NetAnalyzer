#include <stdio.h>
#include <limits.h>

int maxSubarraySum_n2(int arr[], int n) {
    int max_sum = INT_MIN;

    for (int i = 0; i < n; i++) 
    {
        int current_sum = 0;
        for (int j = i; j < n; j++) 
        {
            current_sum += arr[j];
            if (current_sum > max_sum) 
            {
                max_sum = current_sum;
            }
        }
    }
    return max_sum;
}

int main() 
{
    int arr[] = {12, 4 , 3 ,-1 , 4 , 3 , 66};
    int n = sizeof(arr) / sizeof(arr[0]);
    
    printf("Maximum Subarray Sum (O(n^2)): %d\n", maxSubarraySum_n2(arr, n));
    return 0;
}
