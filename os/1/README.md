熟悉进程和线程的创建。

Task 1: Create a console application, “child”, which keeps printing out “The child is talking at [system time]” (in a loop, one per 1s).

Task 2: Create another console application, “parent”. It create a child process to execute “child”. At the same time, the “parent” process keeps printing out “The parent is talking at [system time]”. (one per 1s).  Execute “parent” and explain the output you see. 

Task 3: Create a child thread in the “mainThread” program. Both the main thread and the child thread keep printing out “[ThreadID] + [System time]”.

Task 4: Create a console application, which contains a shared integer shared_var. The initial value of shared_var is 0. The application will create a child thread after it starts. The main thread keeps increasing the value of shared_var by 1, while the child thread keeps decreasing the value of shared_var by 1.  Explain the observed results.