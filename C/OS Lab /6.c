#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    pid_t pid; // Process ID

    pid = fork(); // Create a new process

    if (pid < 0) {
        // Fork failed
        perror("Fork failed");
        exit(1);
    } else if (pid == 0) {
        // Child process
        printf("I am the child process with PID %d.\n", getpid());
        printf("Child process is terminating.\n");
        exit(0); // Child process terminates
    } else {
        // Parent process
        printf("I am the parent process with PID %d.\n", getpid());
        printf("My child’s PID is %d.\n", pid);

        // Parent does not call wait(), causing the child process to remain as a zombie
        sleep(10); // Sleep to allow observation of the zombie process in the process table
        printf("Parent process is terminating without cleaning up the child.\n");
    }

    return 0;
}
