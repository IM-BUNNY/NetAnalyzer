#include <stdio.h>
#define SIZE 3

int main() {
    int arr[SIZE] = {0}; // Initialize buffer with 0
    int item, x, i;
    int signal = 0; // Tracks the number of items in the buffer
    int wait = SIZE; // Tracks the number of empty slots in the buffer

    while (1) {
        printf("Enter the operation:\n1. Produce\n2. Consume\n3. Display\n0. Exit\n");
        scanf("%d", &x);

        if (x == 0) {
            printf("Exiting...\n");
            break;
        }

        switch (x) {
            case 1: // Produce
                if (signal < SIZE) {
                    printf("Enter the item to produce: ");
                    scanf("%d", &item);
                    arr[signal] = item; // Add item to the buffer
                    signal++;
                    wait--;
                    printf("Produced: %d\n", item);
                } else {
                    printf("Buffer is full. Cannot produce more items.\n");
                }
                break;

            case 2: // Consume
                if (signal > 0) {
                    printf("Consumed: %d\n", arr[0]);
                    for (i = 0; i < signal - 1; i++) {
                        arr[i] = arr[i + 1]; // Shift items in the buffer
                    }
                    arr[signal - 1] = 0; // Clear the last slot
                    signal--;
                    wait++;
                } else {
                    printf("Buffer is empty. Nothing to consume.\n");
                }
                break;

            case 3: // Display
                printf("Buffer: ");
                for (i = 0; i < SIZE; i++) {
                    printf("%d ", arr[i]);
                }
                printf("\nSignal: %d\tWait: %d\n", signal, wait);
                break;

            default:
                printf("Invalid option. Please try again.\n");
                break;
        }
    }

    return 0;
}