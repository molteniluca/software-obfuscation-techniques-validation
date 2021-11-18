#include <stdio.h>

#define ARRAY_SIZE 5

#include <time.h>
#define _GNU_SOURCE             /* See feature_test_macros(7) */
#include <sched.h>
#include <unistd.h>

void fill_array(int* arr, int fill_sorted) {
	//printf("\n Filling the array ");
	int i;

	if(fill_sorted) {
		//printf("with sorted numbers...");

		for(i = 0; i < ARRAY_SIZE; ++i) arr[i] = i;
	} else {
		//printf("with random numbers...");

		for(i = 0; i < ARRAY_SIZE; ++i) arr[i] = rand();
	}

	//printf(" Done!");
} 
 
int main()
{

}

int main(){
    cpu_set_t my_set;        /* Define your cpu_set bit mask. */
    CPU_ZERO(&my_set);       /* Initialize it all to 0, i.e. no CPUs selected. */
    CPU_SET(7, &my_set);     /* set the bit that represents core 7. 1=LITTLE 7=BIG */
    sched_setaffinity(0, sizeof(cpu_set_t), &my_set);

    clock_t tic = clock();
  
  int c, d, k, sum = 0;
  int first[ARRAY_SIZE][ARRAY_SIZE], second[ARRAY_SIZE][ARRAY_SIZE], multiply[ARRAY_SIZE][ARRAY_SIZE];
 
  fill_array(first, ARRAY_SIZE*ARRAY_SIZE);
  fill_array(second, ARRAY_SIZE*ARRAY_SIZE);
 
    for (c = 0; c < ARRAY_SIZE; c++) {
      for (d = 0; d < ARRAY_SIZE; d++) {
        for (k = 0; k < ARRAY_SIZE; k++) {
          sum = sum + first[c][k]*second[k][d];
        }
 
        multiply[c][d] = sum;
        sum = 0;
      }
    }

    clock_t toc = clock();
    double tot_time = (double)(toc - tic) / CLOCKS_PER_SEC;
    printf("Elapsed: %f seconds\n%dms per iteration\n", tot_time, (int) (tot_time / iter * 1000) );
    
    return 0;
}
