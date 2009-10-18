#include <stdio.h>

int do_sum(int n) 
{
    int i, sum;
    sum = 0;
    for(i=0;i<n;++i) {
	sum += i;
    }
    return sum;
    
}

int main(int argc, char *argv[]) 
{
    int sum;

    sum = do_sum(1000);
    printf("Total sum is: %d\n", sum);

    return 0;
}
