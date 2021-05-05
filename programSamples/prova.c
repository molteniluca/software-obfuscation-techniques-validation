int fun(int a);

int _start(){
	int a=0x27;
	a++;
	a--;
	fun(a);
	return a;
}

int fun(int a){
	int b=a;
	return b++;
}

