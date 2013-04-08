#include <stdio.h>
#include <stdio.h>

int max(int x[], int n);

int main(void)
{
	int myarray[5];
	myarray[0] = 2;
	myarray[1] = 3;
	myarray[2] = 6;
	myarray[3] = 9;
	myarray[4] = 12;
	int max_num = max(myarray,5);
	printf("Max is %d\n",max_num);
}

int max(int x[], int n)
{
	int i=1;
	int max=x[0];
	for(i;i<n;i++)
	{
		if(x[i] > max)
		{
			max = x[i];
		}
	}
	return max;
}
