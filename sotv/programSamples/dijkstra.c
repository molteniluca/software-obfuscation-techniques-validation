#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <limits.h>

typedef struct temp1{
    int destinationVertex;
    int length;
    struct temp1 *next;
}proximity_list;

typedef struct temp2{
    int vertex;
    int distance;
}heap_node;

typedef struct  temp3{
    int *position;
    int size;
    heap_node **nodeList;
}heap;

typedef struct Point{
    int size;
    proximity_list **list;
}node;

node *ArrayBuffer;
heap_node *reset;
heap *minHeap;
int rankLength = 0;

int Parent(int i){
    return (i - 1) / 2;
};

int Left(int i){
    return i*2 +1;
}

int Right(int i){
    return i*2 +2;
}
void swap(heap_node **list,int i, int max){
    heap_node* temp = list[max];
    list[max] = list[i];
    list[i] = temp;
}
void minHeapify(int i){
    int left = Left(i);
    int right = Right(i);
    int posMax;
    if(left <= minHeap->size && minHeap->nodeList[left]->distance<minHeap->nodeList[i]->distance){
        posMax = left;
    } else
        posMax = i;
    if(right <= minHeap->size && minHeap->nodeList[right]->distance<minHeap->nodeList[posMax]->distance){
        posMax = right;
    }
    if(posMax!=i){
        minHeap->position[minHeap->nodeList[posMax]->vertex] = i;
        minHeap->position[minHeap->nodeList[i]->vertex] = posMax;
        swap(minHeap->nodeList,i,posMax);
        minHeapify(posMax);
    }
}

void Create_Min_Heap(int nodeListLength){
    minHeap = malloc(sizeof (heap*));
    minHeap->nodeList = malloc(nodeListLength * sizeof(heap_node*));
    minHeap->size = 0;
    minHeap->position = malloc(nodeListLength * sizeof(int));
}

void Insert(int index,int i,int distance){
    if(index==0){
        minHeap->nodeList[i] = malloc(sizeof (heap_node));
        if(i==0){
            reset = minHeap->nodeList[i];
        }
    }
    minHeap->nodeList[i]->vertex = i;
    minHeap->nodeList[i]->distance = distance;
}

void decreaseKey(int vert, int dist) {
    int i = minHeap->position[vert];
    minHeap->nodeList[i]->distance = dist;
    while (i!=0 && minHeap->nodeList[i]->distance < minHeap->nodeList[Parent(i)]->distance) {
        minHeap->position[minHeap->nodeList[i]->vertex] = Parent(i);
        minHeap->position[minHeap->nodeList[Parent(i)]->vertex] = i;
        swap(minHeap->nodeList,i, Parent(i));
        i = Parent(i);
    }
}

heap_node *extractMin(){
    if (minHeap->size<1)
        return NULL;
    heap_node *heapRoot = minHeap->nodeList[0];
    heap_node *heapLeaf = minHeap->nodeList[minHeap->size - 1];
    minHeap->nodeList[0] = heapLeaf;
    minHeap->position[heapLeaf->vertex] = 0;
    minHeap->position[heapRoot->vertex] = minHeap->size - 1;
    minHeap->size = minHeap->size - 1;
    minHeapify(0);
    return heapRoot;
}

void ResetHeap(int index, int *distance){
    minHeap->size = 0;
    heap_node *flag = reset;
    for(int i = 0; i < ArrayBuffer->size; i++){
        distance[i] = INT_MAX;
        Insert(index,i,distance[i]);
        minHeap->position[i] = i;
    }
    distance[0] = 0;
    minHeap->size = ArrayBuffer->size;
}

void DijkstraQueue(){
    int temp;
    heap_node *heapNode;
    int distance[ArrayBuffer->size];
    ResetHeap(0,distance);
    while(minHeap->size != 0){
        heapNode = extractMin();
        temp = heapNode->vertex;
        if(temp == 0){
            reset = heapNode;
        }
        proximity_list *list = ArrayBuffer->list[temp];
        int vTemp;
        while(list != NULL){
            vTemp = list->destinationVertex;
            if (distance[temp] < INT_MAX && list->length + distance[temp] < distance[vTemp]){
                distance[vTemp] = distance[temp] + list->length;
                decreaseKey(vTemp,distance[vTemp]);
            }
            list = list->next;
        }
    }
};

void Insert_List(int vertex) {
    proximity_list *head = NULL;
    proximity_list *prev, *next= ArrayBuffer->list[vertex], *temp;
    proximity_list *temp1;
    prev = NULL;
    int length;
    int number = 0;
    for (int i=0; i<40; i++) {
        length = rand();
        if (length != 0 && vertex != number && number != 0) {
            temp = malloc(sizeof(proximity_list));
            if (prev == NULL) {
                head = temp;
            } else
                prev->next = temp;
            temp->length = length;
            temp->destinationVertex = number;
            temp->next = NULL;
            prev = temp;
        }
        number++;
    }
    ArrayBuffer->list[vertex] = head;
}

void main() {
    ArrayBuffer = malloc(sizeof(node*));
    int sizeLine;
    int k;
    k = 40;
    Create_Min_Heap(k);
    for (int i = 0; i<k; i++){
        Insert_List(i);
    }
    DijkstraQueue();
}