#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{
    pid_t pid = fork();

    if (pid > 0)
    {
        // 父进程路径
        printf("Parent: Waiting for child to finish...\n");

        int status;
        pid_t child_pid = wait(&status); // 等待子进程结束

        if (WIFEXITED(status))
        {
            printf("Parent: Child %d exited with status %d\n", child_pid, WEXITSTATUS(status));
        }
        else
        {
            printf("Parent: Child %d terminated abnormally\n", child_pid);
        }
    }
    else if (pid == 0)
    {
        // 子进程路径
        printf("Child: I am the child process with PID %d\n", getpid());
        sleep(2); // 模拟工作
        printf("Child: Work done, exiting...\n");
        return 42; // 返回退出码
    }
    else
    {
        // fork() 失败
        perror("fork failed");
        return 1;
    }

    return 0;
}
