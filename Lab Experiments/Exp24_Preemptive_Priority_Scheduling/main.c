#include <stdio.h> 
  
int main() 
{ 
    int n, i, at[10], bt[10], pr[10], rt[10], ct[10], tat, wt; 
    int t = 0, completed = 0, k, prev = -1; 
    float twt = 0, ttat = 0; 
  
    printf("Enter number of processes: "); 
    scanf("%d", &n); 
    for (i = 0; i < n; i++) { 
        printf("Enter arrival time, burst time and priority of P%d: ", i + 1); 
        scanf("%d %d %d", &at[i], &bt[i], &pr[i]); 
        rt[i] = bt[i]; 
    } 
    printf("\nExecution order: "); 
    while (completed < n) { 
        k = -1; 
        for (i = 0; i < n; i++) 
            if (at[i] <= t && rt[i] > 0 && (k == -1 || pr[i] < pr[k])) 
                k = i; 
        if (k == -1) { t++; continue; } 
        if (k != prev) { printf("P%d(t=%d) ", k + 1, t); prev = k; } 
        rt[k]--; 
        t++; 
        if (rt[k] == 0) { ct[k] = t; completed++; } 
    } 
    printf("\n\nProcess\tAT\tBT\tPRI\tCT\tTAT\tWT\n"); 
    for (i = 0; i < n; i++) { 
        tat = ct[i] - at[i]; 
        wt = tat - bt[i]; 
        twt += wt; 
        ttat += tat; 
        printf("P%d\t%d\t%d\t%d\t%d\t%d\t%d\n", i + 1, at[i], bt[i], pr[i], ct[i], tat, 
wt); 
    } 
    printf("\nAverage Waiting Time    = %.2f\n", twt / n); 
    printf("Average Turnaround Time = %.2f\n", ttat / n); 
    return 0; 
}
