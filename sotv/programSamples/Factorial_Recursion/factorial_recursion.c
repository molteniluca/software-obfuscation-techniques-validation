long int fact(int n);

int main() {
    return fact(100);
}

long int fact(int n) {
    if (n>=1)
        return n*fact(n-1);
    else
        return 1;
}