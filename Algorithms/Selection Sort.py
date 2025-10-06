def selectionSort(array, size):
    for ind in range(size):
        min_index = ind

        for j in range(ind + 1, size):
            if array[j] < array[min_index]:
                min_index = j
        (array[ind], array[min_index]) = (array[min_index], array[ind])
    return array

array = [20, 50, 40, 10, 30]
print("Unsorted array is:", array)
print("Sorted array is:", selectionSort(array, len(array)))