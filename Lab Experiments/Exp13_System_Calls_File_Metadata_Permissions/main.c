#include <stdio.h> 
#include <sys/stat.h> 
  
void show(char *name) 
{ 
    struct stat st; 
    if (stat(name, &st) < 0) { perror("stat"); return; } 
    printf("File name   : %s\n", name); 
    printf("Inode       : %lu\n", (unsigned long)st.st_ino); 
    printf("Size        : %ld bytes\n", (long)st.st_size); 
    printf("Links       : %lu\n", (unsigned long)st.st_nlink); 
    printf("Owner UID   : %d\n", st.st_uid); 
    printf("Permissions : %o\n\n", st.st_mode & 0777); 
} 
  
int main() 
{ 
    FILE *fp = fopen("data.txt", "w"); 
    fprintf(fp, "file metadata demo\n"); 
    fclose(fp); 
  
    printf("Before chmod:\n"); 
    show("data.txt"); 
    if (chmod("data.txt", 0754) == 0) 
        printf("Permissions changed to 754\n\n"); 
    printf("After chmod:\n"); 
    show("data.txt"); 
    return 0; 
}
