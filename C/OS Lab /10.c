#include <stdio.h>

void sortProcesses(int processes[], int burst_time[], int priority[], int n) 
{
    for (int i = 0; i < n - 1; i++) 
    {
        for (int j = i + 1; j < n; j++) 
        {
            if (priority[i] > priority[j]) 
            {
                // Swap burst times
                int temp = burst_time[i];
                burst_time[i] = burst_time[j];
                burst_time[j] = temp;

                // Swap process IDs
                int temp_id = processes[i];
                processes[i] = processes[j];
                processes[j] = temp_id;

                // Swap priorities
                int temp_priority = priority[i];
                priority[i] = priority[j];
                priority[j] = temp_priority;
            }
        }
    }
}

void calculateTimes(int processes[], int burst_time[], int priority[], int n) 
{
    int waiting_time[n], turnaround_time[n];
    int total_waiting_time = 0, total_turnaround_time = 0;

    waiting_time[0] = 0;
    turnaround_time[0] = burst_time[0];
    total_turnaround_time = turnaround_time[0]; // Include the first process TAT

    for (int i = 1; i < n; i++) 
    {
        waiting_time[i] = waiting_time[i - 1] + burst_time[i - 1];
        turnaround_time[i] = waiting_time[i] + burst_time[i];
        
        total_waiting_time += waiting_time[i];
        total_turnaround_time += turnaround_time[i];
    }

    printf("\nProcess\tBurst Time\tPriority\tWaiting Time\tTurnaround Time\n");
    for (int i = 0; i < n; i++) 
    {
        printf("P%d\t%d ms\t\t%d\t\t%d ms\t\t%d ms\n", processes[i], burst_time[i], priority[i], waiting_time[i], turnaround_time[i]);
    }

    float avg_waiting_time = (float)total_waiting_time / n;
    float avg_turnaround_time = (float)total_turnaround_time / n;
    
    printf("\nAverage Waiting Time: %.2f ms", avg_waiting_time);
    printf("\nAverage Turnaround Time: %.2f ms\n", avg_turnaround_time);
}

int main() 
{
    int processes[] = {1, 2, 3, 4, 5};
    int burst_time[] = {10, 1, 2, 1, 5};  
    int priority[] = {3, 1, 4, 5, 2};  
    int n = sizeof(processes) / sizeof(processes[0]);

    sortProcesses(processes, burst_time, priority, n);

    calculateTimes(processes, burst_time, priority, n);

    return 0;
}