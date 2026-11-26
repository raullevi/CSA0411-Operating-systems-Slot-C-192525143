#include <stdio.h> 
  
int main() 
{ 
    int n, i, q, bt[10], rt[10], ct[10], t = 0, left; 
    float twt = 0, ttat = 0; 
  
    printf("Enter number of processes: "); 
    scanf("%d", &n); 
    for (i = 0; i < n; i++) { 
        printf("Enter burst time of P%d: ", i + 1); 
        scanf("%d", &bt[i]); 
        rt[i] = bt[i]; 
    } 
    printf("Enter time quantum: "); 
    scanf("%d", &q); 
  
    left = n; 
    printf("\nGantt Chart: "); 
    while (left > 0) { 
        for (i = 0; i < n; i++) { 
            if (rt[i] == 0) continue; 
            int run = rt[i] > q ? q : rt[i]; 
            printf("| P%d (%d-%d) ", i + 1, t, t + run); 
            t += run; 
            rt[i] -= run; 
            if (rt[i] == 0) { ct[i] = t; left--; } 
        } 
    } 
    printf("|\n\nProcess\tBT\tCT\tTAT\tWT\n"); 
    for (i = 0; i < n; i++) { 
        int tat = ct[i], wt = ct[i] - bt[i]; 
        twt += wt; 
        ttat += tat; 
        printf("P%d\t%d\t%d\t%d\t%d\n", i + 1, bt[i], ct[i], tat, wt); 
    } 
    printf("\nAverage Waiting Time    = %.2f\n", twt / n); 
    printf("Average Turnaround Time = %.2f\n", ttat / n); 
    return 0; 
}
