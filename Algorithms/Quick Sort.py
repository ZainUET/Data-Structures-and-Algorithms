def quickSort(array, start, end):
    if start < end:
        pivotIndex = partition(array, start, end)
        quickSort(array, start, pivotIndex - 1)
        quickSort(array, pivotIndex + 1, end)
    return array 
   
def partition(array, start, end):
    idx = start - 1
    pivot = array[end]
    for j in range(start, end):
        if array[j] < pivot:     
            idx += 1
            array[idx], array[j] = array[j], array[idx]
    idx += 1
    array[idx], array[end] = array[end], array[idx]
    return idx

array = [1, 2, 7, 5, 9, 6]
n = len(array)
print("Sorted array is:", quickSort(array, 0, n - 1))
