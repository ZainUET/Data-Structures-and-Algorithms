def bubbleSort(arr):
    n=len(arr)
    for i in range (n):
        swapped=False
        for j in range(0,n-i-1):
            if arr[j]>arr[j+1]:
                arr[j],arr[j+1]=arr[j+1],arr[j]
                swapped=True
        if not swapped:
            break
    return arr

arr=[20,50,10,10,30]
print("Sorted array is:",bubbleSort(arr))



