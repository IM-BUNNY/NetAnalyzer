#include <stdio.h>

#define PARTITIONS 6
#define PROCESSES 4

int main() {
    int partitions[PARTITIONS] = {150,350};
    int process[PROCESSES] = {300,25,125,50};
    int allocation[PROCESSES];
    int used[PARTITIONS] = {0}; // Track used partitions

    // Initialize allocations to -1 
    for (int i = 0; i < PROCESSES; i++)
        allocation[i] = -1;

    // Best-Fit Allocation
    for (int i = 0; i < PROCESSES; i++) {
        int bestIdx = -1;
        for (int j = 0; j < PARTITIONS; j++) {
            if (!used[j] && partitions[j] >= process[i]) {
                if (bestIdx == -1 || partitions[j] < partitions[bestIdx])
                    bestIdx = j;
            }
        }

        if (bestIdx != -1) {
            allocation[i] = bestIdx;
            used[bestIdx] = 1;
        }
    }

    // Output results
    printf("Process No.\tProcess Size\tAllocated Partition\n");
    for (int i = 0; i < PROCESSES; i++) {
        printf("P%d\t\t%d KB\t\t", i + 1, process[i]);
        if (allocation[i] != -1)
            printf("%d KB (Partition %d)\n", partitions[allocation[i]], allocation[i] + 1);
        else
            printf("Not Allocated\n");
    }

    // Show memory status
    printf("\nPartition No.\tPartition Size\tStatus\n");
    for (int i = 0; i < PARTITIONS; i++) {
        printf("%d\t\t%d KB\t\t%s\n", i + 1, partitions[i], used[i] ? "Occupied" : "Free");
    }

    // Calculate external fragmentation
    int external_frag = 0;
    for (int i = 0; i < PARTITIONS; i++) {
        if (!used[i])
            external_frag += partitions[i];
    }

    printf("\nExternal Fragmentation: %d KB\n", external_frag);

    return 0;
}