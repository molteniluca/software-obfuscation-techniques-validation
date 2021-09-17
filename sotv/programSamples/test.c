int fun(int a);

int main(){
	int a=0x27;
	a++;
	return fun(a);
}

int fun(int a){
	int b=a;
	return b++;
}

