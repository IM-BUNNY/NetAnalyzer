#include<stdio.h>
#include<stdlib.h>

#define MAX 10000  // Assumption: The max possible number in the array

int findPair(int nums[], int size, int target) 
{
    int hash[MAX] = {0};  
    for (int i = 0; i < size; i++)
    {
        int complement = target - nums[i];

        if (complement >= 0 && hash[complement] == 1) 
        {
            printf("(%d, %d)\n", nums[i], complement);
            return 1;
        }

        // Store current number in hash table
        hash[nums[i]] = 1;
    }

    // If no pair is found
    printf("(-1, -1)\n");
    return 0;
}

int main() {
    int nums1[] = {8, 7, 2, 5, 3, 1};
    int target1 = 10;
    int size1 = sizeof(nums1) / sizeof(nums1[0]);

    int nums2[] = {5, 2, 6, 8, 1, 9};
    int target2 = 10;
    int size2 = sizeof(nums2) / sizeof(nums2[0]);

    // Test cases
    findPair(nums1, size1, target1); 
    findPair(nums2, size2, target2); 

    return 0;
}
