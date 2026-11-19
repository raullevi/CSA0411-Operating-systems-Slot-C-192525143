#include <stdio.h>
#include <stdlib.h>

void calculate_raid_specs(int num_disks, double disk_cap_tb, double afr, double mttr_hours) {
    printf("=======================================================================\n");
    printf("  RAID SPECIFICATIONS & RELIABILITY MODEL (HOSPITAL RECORDS SERVER)\n");
    printf("  Array Config: %d Disks of %.1f TB each (Raw Total: %.1f TB)\n",
           num_disks, disk_cap_tb, num_disks * disk_cap_tb);
    printf("  Annual Failure Rate (AFR) = %.2f%%, MTTR Rebuild Window = %.1f Hours\n",
           afr * 100.0, mttr_hours);
    printf("=======================================================================\n\n");

    printf("%-10s %-14s %-14s %-16s %-16s %-14s\n",
           "Level", "Usable Space", "Efficiency", "Fault Tolerance", "Write Penalty", "Read Speedup");
    printf("-----------------------------------------------------------------------------------------\n");

    /* RAID 0 */
    double cap_r0 = num_disks * disk_cap_tb;
    printf("%-10s %10.1f TB %12.1f%% %-16s %-16s %-14s\n",
           "RAID 0", cap_r0, (cap_r0 / (num_disks * disk_cap_tb)) * 100.0,
           "0 Disks (None)", "1x (No penalty)", "Nx (Max speed)");

    /* RAID 1 (Duplex / Mirrors) */
    double cap_r1 = (num_disks / 2.0) * disk_cap_tb;
    printf("%-10s %10.1f TB %12.1f%% %-16s %-16s %-14s\n",
           "RAID 1", cap_r1, (cap_r1 / (num_disks * disk_cap_tb)) * 100.0,
           "1 disk per pair", "2x (Dual write)", "Nx (Load balance)");

    /* RAID 5 */
    double cap_r5 = (num_disks - 1) * disk_cap_tb;
    printf("%-10s %10.1f TB %12.1f%% %-16s %-16s %-14s\n",
           "RAID 5", cap_r5, (cap_r5 / (num_disks * disk_cap_tb)) * 100.0,
           "1 Any Disk", "4x (2R, 2W)", "(N-1)x");

    /* RAID 6 */
    double cap_r6 = (num_disks - 2) * disk_cap_tb;
    printf("%-10s %10.1f TB %12.1f%% %-16s %-16s %-14s\n",
           "RAID 6", cap_r6, (cap_r6 / (num_disks * disk_cap_tb)) * 100.0,
           "2 Any Disks", "6x (3R, 3W)", "(N-2)x");

    /* RAID 10 */
    double cap_r10 = (num_disks / 2.0) * disk_cap_tb;
    printf("%-10s %10.1f TB %12.1f%% %-16s %-16s %-14s\n",
           "RAID 10", cap_r10, (cap_r10 / (num_disks * disk_cap_tb)) * 100.0,
           "Up to 3 Disks", "2x (Mirrored)", "Nx");
    printf("-----------------------------------------------------------------------------------------\n\n");

    /* Probability of Data Loss Calculations */
    double tau_years = mttr_hours / 8760.0;
    double p_rebuild = afr * tau_years;

    /* RAID 1 (2-disk mirror pair) */
    double prob_loss_r1 = afr * p_rebuild;

    /* RAID 5 (6-disk array) */
    double prob_loss_r5 = (double)num_disks * afr * ((double)(num_disks - 1) * p_rebuild);

    /* RAID 6 (6-disk array) */
    double prob_loss_r6 = (double)num_disks * afr * ((double)(num_disks - 1) * p_rebuild) * ((double)(num_disks - 2) * p_rebuild);

    printf("=======================================================================\n");
    printf("  PROBABILITY OF DATA LOSS DURING REBUILD (P_loss)\n");
    printf("=======================================================================\n");
    printf("Single Disk Failure Probability during %.0f-hr Rebuild: %.6f%%\n",
           mttr_hours, p_rebuild * 100.0);
    printf("1. RAID 1 Mirror Pair Data Loss Probability : %.8f%% (1 in %ld)\n",
           prob_loss_r1 * 100.0, (long)(1.0 / prob_loss_r1));
    printf("2. RAID 5 (6 Disks) Data Loss Probability   : %.8f%% (1 in %ld)\n",
           prob_loss_r5 * 100.0, (long)(1.0 / prob_loss_r5));
    printf("3. RAID 6 (6 Disks) Data Loss Probability   : %.12f%% (1 in %lld)\n",
           prob_loss_r6 * 100.0, (long long)(1.0 / prob_loss_r6));
    printf("-----------------------------------------------------------------------\n");
    printf("Risk Comparison: RAID 5 is %.1fx MORE LIKELY to lose hospital patient data\n",
           prob_loss_r5 / prob_loss_r1);
    printf("than RAID 1/10 during an active rebuild cycle!\n");
    printf("=======================================================================\n");
}

int main(void) {
    calculate_raid_specs(6, 4.0, 0.02, 24.0);
    return 0;
}
