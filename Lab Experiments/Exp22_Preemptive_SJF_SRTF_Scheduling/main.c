#include <stdio.h> 
  
int main() 
{ 
    int n, i, at[10], bt[10], rt[10], ct[10], tat[10], wt[10]; 
    int t = 0, completed = 0, k, prev = -1; 
    float twt = 0, ttat = 0; 
  
    printf("Enter number of processes: "); 
    scanf("%d", &n); 
    for (i = 0; i < n; i++) { 
        printf("Enter arrival time and burst time of P%d: ", i + 1); 
        scanf("%d %d", &at[i], &bt[i]); 
        rt[i] = bt[i]; 
    } 
    printf("\nExecution order: "); 
    while (completed < n) { 
        k = -1; 
        for (i = 0; i < n; i++) 
            if (at[i] <= t && rt[i] > 0 && (k == -1 || rt[i] < rt[k])) 
                k = i; 
        if (k == -1) { t++; continue; } 
        if (k != prev) { printf("P%d(t=%d) ", k + 1, t); prev = k; } 
        rt[k]--; 
        t++; 
        if (rt[k] == 0) { 
            ct[k] = t; 
            completed++; 
        } 
    } 
    printf("\n\nProcess\tAT\tBT\tCT\tTAT\tWT\n"); 
    for (i = 0; i < n; i++) { 
        tat[i] = ct[i] - at[i]; 
        wt[i] = tat[i] - bt[i]; 
        twt += wt[i]; 
        ttat += tat[i]; 
        printf("P%d\t%d\t%d\t%d\t%d\t%d\n", i + 1, at[i], bt[i], ct[i], tat[i], wt[i]); 
    } 
    printf("\nAverage Waiting Time    = %.2f\n", twt / n); 
    printf("Average Turnaround Time = %.2f\n", ttat / n); 
    return 0; 
}
