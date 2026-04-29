#include <stdio.h>
#include <stdlib.h>

#define BUFFER_SIZE 3

int buffer[BUFFER_SIZE]; 
int in = 0, out = 0; 

void displayBuffer() {
    printf("The buffer status is:\n");
    for (int i = 0; i < BUFFER_SIZE; i++) {
        printf("%d  ", buffer[i]);
    }
    printf("\nin = %d\nout = %d\n", in, out);
}

int main() {
    int choice, item;
    int count=0;
    for (int i = 0; i < BUFFER_SIZE; i++) {
        buffer[i] = 0;
    }

    while (1) {
        printf("\n1. Producer\n2. Consumer\n3. Exit\n");
        displayBuffer();
        printf("\nEnter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1: // Producer
                if (count==BUFFER_SIZE)
                
                {
                    printf("Buffer is full!!\n");
                } else {
                    printf("Produce an integer item: ");
                    scanf("%d", &item);
                    buffer[in] = item;
                    in = (in + 1) % BUFFER_SIZE;
                    count++;
                }
                break;

            case 2: // Consumer
                if (count==0) {
                    printf("Buffer is empty!!\n");
                } else {
                    printf("Consumed item: %d\n", buffer[out]);
                    buffer[out] = 0; // Reset slot after consuming
                    out = (out + 1) % BUFFER_SIZE;
                    count--;
                }
                break;

            case 3: // Exit
                exit(0);

            default:
                printf("Invlaid chiche ifb\n");
        }
    }

    return 0;
}
