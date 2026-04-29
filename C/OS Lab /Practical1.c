#include<stdio.h>
#include<stdlib.h>
void sort(int process[], int at[], int bt[], int n) 
{
    for (int i = 0; i < n - 1; i++) 
    {
        for (int j = i + 1; j < n; j++) 
        {
            if (bt[i] < bt[j]) 
            { 
                int temp = bt[i];
                bt[i] = bt[j];
                bt[j] = temp;

                temp = at[i];
                at[i] = at[j];
                at[j] = temp;

                temp = process[i];
                process[i] = process[j];
                process[j] = temp;
            }
        }
    }
}

void calc(int process[], int at[], int bt[], int n) 
{
    int wt[n], tat[n];
    int total_wt = 0, total_tat = 0;

    wt[0] = 0;
    tat[0] = bt[0];
    total_tat += tat[0];

    for (int i = 1; i < n; i++) 
    {
        wt[i] = wt[i - 1] + bt[i - 1];
        tat[i] = wt[i] + bt[i];
        total_wt += wt[i];
        total_tat += tat[i];
    }

    printf("\nProcess\tArrival Time\tBurst Time\tWaiting Time\tTurnaround Time\n");

    for (int i = 0; i < n; i++) 
    {
        printf("P%d\t%d\t\t%d\t\t%d\t\t%d\n", process[i], at[i], bt[i], wt[i], tat[i]);
    }

    float avg_wt = (float)total_wt / n;
    float avg_tat = (float)total_tat / n;

    printf("\nAverage Waiting Time: %.2f", avg_wt);
    printf("\nAverage Turnaround Time: %.2f\n", avg_tat);
}

int main() 
{
    int process[] = {1, 2, 3, 4};
    int at[] = {0, 0, 0, 0};
    int bt[] = {6, 8, 7, 3};
    int n = sizeof(process) / sizeof(process[0]);
    sort(process, at, bt, n);
    calc(process, at, bt, n);
    return 0;
}