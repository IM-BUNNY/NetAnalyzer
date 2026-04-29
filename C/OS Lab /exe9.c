#include <stdio.h>

void sortByArrival(int n, int at[], int bt[], int pid[]) 
{
    for (int i = 0; i < n - 1; i++) 
    {
        for (int j = 0; j < n - i - 1; j++) 
        {
            if (at[j] > at[j + 1]) 
            {

                int temp = at[j];
                at[j] = at[j + 1];
                at[j + 1] = temp;

                temp = bt[j];
                bt[j] = bt[j + 1];
                bt[j + 1] = temp;

                temp = pid[j];
                pid[j] = pid[j + 1];
                pid[j + 1] = temp;
            }
        }
    }
}

void calculateTimes(int n, int at[], int bt[], int ct[], int tat[], int wt[]) 
{
    int currentTime = 0;
    
    for (int i = 0; i < n; i++) 
    {
        if (currentTime < at[i]) 
        {
            currentTime = at[i];  
        }
        
        ct[i] = currentTime + bt[i];  // Completion Time
        tat[i] = ct[i] - at[i];       // Turnaround Time = CT - AT
        wt[i] = tat[i] - bt[i];       // Waiting Time = TAT - BT
        
        currentTime = ct[i];  // Update current time
    }
}

void displayResults(int n, int at[], int bt[], int ct[], int tat[], int wt[], int pid[]) {
    float totalWT = 0, totalTAT = 0;
    
    printf("\nProcess\tAT\tBT\tCT\tTAT\tWT\n");
    for (int i = 0; i < n; i++) {
        printf("%d\t%d\t%d\t%d\t%d\t%d\n", pid[i], at[i], bt[i], ct[i], tat[i], wt[i]);
        totalWT += wt[i];
        totalTAT += tat[i];
    }
    
    printf("\nAverage Waiting Time: %.2f", totalWT / n);
    printf("\nAverage Turnaround Time: %.2f\n", totalTAT / n);
}

// Main function
int main() {
    int n;
    
    printf("Enter the number of processes: ");
    scanf("%d", &n);
    
    int at[n], bt[n], ct[n], tat[n], wt[n], pid[n];
    
    for (int i = 0; i < n; i++) {
        pid[i] = i + 1;  // Assign Process IDs
        printf("Enter Arrival Time and Burst Time for Process %d: ", i + 1);
        scanf("%d %d", &at[i], &bt[i]);
    }
    
    sortByArrival(n, at, bt, pid);
    calculateTimes(n, at, bt, ct, tat, wt);
    displayResults(n, at, bt, ct, tat, wt, pid);
    
    return 0;
}
