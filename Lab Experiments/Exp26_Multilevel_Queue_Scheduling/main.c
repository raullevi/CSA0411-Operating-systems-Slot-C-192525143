#include <stdio.h> 
  
int main() 
{ 
    int n, i, level, bt[10], qn[10], wt[10], tat[10], t = 0; 
    float twt = 0, ttat = 0; 
  
    printf("Enter number of processes: "); 
    scanf("%d", &n); 
    for (i = 0; i < n; i++) { 
        printf("Enter burst time and queue (0-system, 1-user) of P%d: ", i + 1); 
        scanf("%d %d", &bt[i], &qn[i]); 
    } 
    printf("\nGantt Chart: "); 
    for (level = 0; level <= 1; level++) { 
        for (i = 0; i < n; i++) { 
            if (qn[i] != level) continue; 
            wt[i] = t; 
            printf("| P%d (%d-%d) ", i + 1, t, t + bt[i]); 
            t += bt[i]; 
            tat[i] = t; 
        } 
    } 
    printf("|\n\nProcess\tQueue\tBT\tWT\tTAT\n"); 
    for (i = 0; i < n; i++) { 
        printf("P%d\t%s\t%d\t%d\t%d\n", i + 1, qn[i] == 0 ? "System" : "User", bt[i], 
wt[i], tat[i]); 
        twt += wt[i]; 
        ttat += tat[i]; 
    } 
    printf("\nAverage Waiting Time    = %.2f\n", twt / n); 
    printf("Average Turnaround Time = %.2f\n", ttat / n); 
    return 0; 
}
