//Fibonacci Series using Dynamic Programming
#include<stdio.h>

#define ARRAY_SIZE 40
 
 #include <time.h>
#define _GNU_SOURCE             /* See feature_test_macros(7) */
#include <sched.h>
#include <unistd.h>

int fib(int n)
{
  /* Declare an array to store Fibonacci numbers. */
  int f[n+2];   // 1 extra to handle case, n = 0
  int i;
 
  /* 0th and 1st number of the series are 0 and 1*/
  f[0] = 0;
  f[1] = 1;
 
  for (i = 2; i <= n; i++)
  {
      /* Add the previous 2 numbers in the series
         and store it */
      f[i] = f[i-1] + f[i-2];
  }
 
  return f[n];
}
 
int main ()
{
  int n = ARRAY_SIZE;
  //printf("%d\n", fib(n));
  //getchar();
  return 0;
}


int main(){
    cpu_set_t my_set;        /* Define your cpu_set bit mask. */
    CPU_ZERO(&my_set);       /* Initialize it all to 0, i.e. no CPUs selected. */
    CPU_SET(7, &my_set);     /* set the bit that represents core 7. 1=LITTLE 7=BIG */
    sched_setaffinity(0, sizeof(cpu_set_t), &my_set);

    clock_t tic = clock();
  
  int n = ARRAY_SIZE;


    clock_t toc = clock();
    double tot_time = (double)(toc - tic) / CLOCKS_PER_SEC;
    printf("Elapsed: %f seconds\n%dms per iteration\n", tot_time, (int) (tot_time / iter * 1000) );
      return 0;
}
