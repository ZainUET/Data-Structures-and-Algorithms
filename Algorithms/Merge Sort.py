def merge_sort(arr):
    if len(arr)<=1:
        return arr
    
    mid=len(arr)//2
    left_array=arr[:mid]
    right_array=arr[mid:]
    left_array= merge_sort(left_array)
    right_array=merge_sort(right_array)
    return merge(left_array,right_array)

def merge(left_array,right_array):
    new=[]
    i,j=0,0
    
    while i<len(left_array) and j<len(right_array):
        if left_array[i]<right_array[j]:
            new.append(left_array[i])
            i+=1
        else:
            new.append(right_array[j])
            j+=1
    new.extend(left_array[i:])
    new.extend(right_array[j:])
    return new

arr=[5,3,1,2,4]
print(merge_sort(arr))
    