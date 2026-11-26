#include <stdio.h> 
  
int main() 
{ 
    int n, i, at[10], bt[10], ct[10], tat[10], wt[10], done[10] = {0}; 
    int t = 0, completed = 0, k; 
    float twt = 0, ttat = 0; 
  
    printf("Enter number of processes: "); 
    scanf("%d", &n); 
    for (i = 0; i < n; i++) { 
        printf("Enter arrival time and burst time of P%d: ", i + 1); 
        scanf("%d %d", &at[i], &bt[i]); 
    } 
    printf("\nGantt Chart: "); 
    while (completed < n) { 
        k = -1; 
        for (i = 0; i < n; i++) 
            if (!done[i] && at[i] <= t && (k == -1 || bt[i] < bt[k])) 
                k = i; 
        if (k == -1) { t++; continue; } 
        printf("| P%d (%d-%d) ", k + 1, t, t + bt[k]); 
        t += bt[k]; 
        ct[k] = t; 
        tat[k] = ct[k] - at[k]; 
        wt[k] = tat[k] - bt[k]; 
        done[k] = 1; 
        completed++; 
    } 
    printf("|\n\nProcess\tAT\tBT\tCT\tTAT\tWT\n"); 
    for (i = 0; i < n; i++) { 
        printf("P%d\t%d\t%d\t%d\t%d\t%d\n", i + 1, at[i], bt[i], ct[i], tat[i], wt[i]); 
        twt += wt[i]; 
        ttat += tat[i]; 
    } 
    printf("\nAverage Waiting Time    = %.2f\n", twt / n); 
    printf("Average Turnaround Time = %.2f\n", ttat / n); 
    return 0; 
}
