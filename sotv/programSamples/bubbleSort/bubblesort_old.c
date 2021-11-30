int main()
{
  int array[10]={9,32,7,90,5,4,3,56,1,0}, n, c, d, swap;
	n=10;


  for (c = 0 ; c < n - 1; c++)
  {
    for (d = 0 ; d < n - c - 1; d++)
    {
      if (array[d] > array[d+1])
      {
        swap       = array[d];
        array[d]   = array[d+1];
        array[d+1] = swap;
      }
    }
  }
    exit(0);
  return 0;
}