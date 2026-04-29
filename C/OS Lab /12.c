#include <stdio.h>

#define PROCESSES 3
#define RESOURCES 12 // Total resources available

void findSafeSequence(int max[], int allocated[], int available) {
    int need[PROCESSES];
    int finished[PROCESSES] = {0};
    int safeSequence[PROCESSES];
    int count = 0;
    
    // Calculate need matrix
    for (int i = 0; i < PROCESSES; i++) {
        need[i] = max[i] - allocated[i];
    }
    
    while (count < PROCESSES) {
        int found = 0;
        for (int i = 0; i < PROCESSES; i++) {
            if (!finished[i] && need[i] <= available) {
                available += allocated[i]; // Release resources after execution
                safeSequence[count++] = i;
                finished[i] = 1;
                found = 1;
            }
        }
        if (!found) {
            printf("System is in an unsafe state!\n");
            return;
        }
    }
    
    // Print safe sequence
    for (int i = 0; i < PROCESSES; i++) {
        printf("Process %d complete!\n", safeSequence[i]);
    }
}

int main() {
    int max[PROCESSES] = {10, 4, 9};
    int allocated[PROCESSES] = {5, 2, 2};
    int available = RESOURCES - (5 + 2 + 2); // Total resources - allocated resources
    
    printf("Original Case:\n");
    findSafeSequence(max, allocated, available);
    
    // Modify T2's allocated resources to 3
    allocated[2] = 3;
    available = RESOURCES - (5 + 2 + 3);
    printf("\nAfter changing T2's allocated resources to 3:\n");
    findSafeSequence(max, allocated, available);
    
    return 0;
}