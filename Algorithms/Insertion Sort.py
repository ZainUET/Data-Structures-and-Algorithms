def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def printArray(arr):
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print()

arr = [9,1,67,54,56,6]
insertionSort(arr)
printArray(arr)

    