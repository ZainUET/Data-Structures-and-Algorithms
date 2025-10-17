def countSort(arr):

    n=len(arr)
    maxval=max(arr)

    count=[0]*(maxval+1)

    for i in arr:
        count[i]+=1

    for i in range(1,maxval+1):
        count[i]+=count[i-1]

    output=[0]*n
    for i in range (n-1,-1,-1):
        j=arr[i]
        output[count[j]-1]=j
        count[j]-=1
   
    return output

arr=[4,2,2,8,3,3,1]
print(countSort(arr))

