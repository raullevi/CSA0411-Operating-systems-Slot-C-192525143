#include <stdio.h> 
  
int main() 
{ 
    int n, i, level, bt[10], rt[10], ct[10], t = 0; 
    int quantum[3] = {2, 4, 1000}; 
    float twt = 0, ttat = 0; 
  
    printf("Enter number of processes: "); 
    scanf("%d", &n); 
    for (i = 0; i < n; i++) { 
        printf("Enter burst time of P%d: ", i + 1); 
        scanf("%d", &bt[i]); 
        rt[i] = bt[i]; 
    } 
    for (level = 0; level < 3; level++) { 
        printf("\nQueue Q%d: ", level); 
        for (i = 0; i < n; i++) { 
            if (rt[i] == 0) continue; 
            int run = rt[i] < quantum[level] ? rt[i] : quantum[level]; 
            printf("P%d(%d-%d) ", i + 1, t, t + run); 
            t += run; 
            rt[i] -= run; 
            if (rt[i] == 0) ct[i] = t; 
        } 
    } 
    printf("\n\nProcess\tBT\tCT\tTAT\tWT\n"); 
    for (i = 0; i < n; i++) { 
        printf("P%d\t%d\t%d\t%d\t%d\n", i + 1, bt[i], ct[i], ct[i], ct[i] - bt[i]); 
        twt += ct[i] - bt[i]; 
        ttat += ct[i]; 
    } 
    printf("\nAverage Waiting Time    = %.2f\n", twt / n); 
    printf("Average Turnaround Time = %.2f\n", ttat / n); 
    return 0; 
}
