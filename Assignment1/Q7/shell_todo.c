#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void)
{
    printf("shell: running job 1\n");
    fflush(stdout); /* empty the buffer before fork() */

    // TODO 1: Create a child with fork(). In the child, replace the program with
    // execlp ("expr", "expr", "6", "*", "7", (char *) NULL) and exit (127) if exec fails.
    // In the parent, wait for the child with waitpid() and print "job 1 exit status N"
    // using WEXITSTATUS
    pid_t pid1 = fork();
    if (pid1 < 0) {
        perror("fork failed");
        exit(1);
    } else if (pid1 == 0) {
        execlp("expr", "expr", "6", "*", "7", (char *)NULL);
        exit(127);
    } else {
        int status1;
        waitpid(pid1, &status1, 0);
        printf("job 1 exit status %d\n", WEXITSTATUS(status1));
    }

    printf("shell: running job 2\n");
    fflush(stdout);
    pid_t pid = fork();
    if (pid == 0) exit(3); /* a child that fails with code 3 */
    int status;
    waitpid(pid, &status, 0);
    printf("job 2 exit status %d\n", WEXITSTATUS(status));
    return 0;
}
