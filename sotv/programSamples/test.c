#include <stdlib.h>

int fun(int a);

int main(){
	int a=0x27;
	a++;
	malloc(0x1222);
	return fun(a);
}

int fun(int a){
	int b=a;
	return b++;
}

