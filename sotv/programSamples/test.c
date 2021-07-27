int fun(int a);

int global=0;

int main(){
	int a=0x27;
	a++;
	a--;
	fun(a);
	return a;
}

int fun(int a){
	int b=a;
	global++;
	return b++;
}

