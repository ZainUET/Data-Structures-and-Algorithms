# core/sorting_algorithms.py
import time
import math
from typing import List, Any, Callable, Tuple
from collections import defaultdict, deque

class SortingAlgorithms:
    """Complete implementation of all required sorting algorithms"""
    
    @staticmethod
    def measure_time(func: Callable) -> Callable:
        """Decorator to measure sorting time in milliseconds"""
        def wrapper(*args, **kwargs):
            start_time = time.time() * 1000  # Convert to milliseconds
            result = func(*args, **kwargs)
            end_time = time.time() * 1000
            execution_time = round(end_time - start_time, 2)
            return result, execution_time
        return wrapper
    
    # ========== CLASS ALGORITHMS ==========
    
    @staticmethod
    @measure_time
    def bubble_sort(data: List[Any], key: str = None, reverse: bool = False) -> List[Any]:
        """Bubble Sort - O(n²)"""
        if not data:
            return data
            
        arr = data.copy()
        n = len(arr)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                # Get values for comparison
                if key:
                    val_j = getattr(arr[j], key) if hasattr(arr[j], key) else arr[j].get(key, "")
                    val_j1 = getattr(arr[j + 1], key) if hasattr(arr[j + 1], key) else arr[j + 1].get(key, "")
                else:
                    val_j = arr[j]
                    val_j1 = arr[j + 1]
                
                # Convert to string for consistent comparison
                try:
                    compare_j = float(val_j) if str(val_j).replace('.', '').isdigit() else str(val_j).lower()
                    compare_j1 = float(val_j1) if str(val_j1).replace('.', '').isdigit() else str(val_j1).lower()
                except:
                    compare_j = str(val_j).lower()
                    compare_j1 = str(val_j1).lower()
                
                # Swap condition
                swap_needed = (compare_j > compare_j1) if not reverse else (compare_j < compare_j1)
                
                if swap_needed:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        
        return arr
    
    @staticmethod
    @measure_time
    def insertion_sort(data: List[Any], key: str = None, reverse: bool = False) -> List[Any]:
        """Insertion Sort - O(n²)"""
        if not data:
            return data
            
        arr = data.copy()
        
        for i in range(1, len(arr)):
            key_item = arr[i]
            j = i - 1
            
            while j >= 0:
                # Get values for comparison
                if key:
                    current_val = getattr(arr[j], key) if hasattr(arr[j], key) else arr[j].get(key, "")
                    key_val = getattr(key_item, key) if hasattr(key_item, key) else key_item.get(key, "")
                else:
                    current_val = arr[j]
                    key_val = key_item
                
                # Convert for comparison
                try:
                    compare_current = float(current_val) if str(current_val).replace('.', '').isdigit() else str(current_val).lower()
                    compare_key = float(key_val) if str(key_val).replace('.', '').isdigit() else str(key_val).lower()
                except:
                    compare_current = str(current_val).lower()
                    compare_key = str(key_val).lower()
                
                # Compare condition
                if reverse:
                    should_shift = compare_current < compare_key
                else:
                    should_shift = compare_current > compare_key
                
                if should_shift:
                    arr[j + 1] = arr[j]
                    j -= 1
                else:
                    break
            
            arr[j + 1] = key_item
        
        return arr
    
    @staticmethod
    @measure_time
    def selection_sort(data: List[Any], key: str = None, reverse: bool = False) -> List[Any]:
        """Selection Sort - O(n²)"""
        if not data:
            return data
            
        arr = data.copy()
        n = len(arr)
        
        for i in range(n):
            extreme_idx = i
            
            for j in range(i + 1, n):
                # Get values for comparison
                if key:
                    val_extreme = getattr(arr[extreme_idx], key) if hasattr(arr[extreme_idx], key) else arr[extreme_idx].get(key, "")
                    val_j = getattr(arr[j], key) if hasattr(arr[j], key) else arr[j].get(key, "")
                else:
                    val_extreme = arr[extreme_idx]
                    val_j = arr[j]
                
                # Convert for comparison
                try:
                    compare_extreme = float(val_extreme) if str(val_extreme).replace('.', '').isdigit() else str(val_extreme).lower()
                    compare_j = float(val_j) if str(val_j).replace('.', '').isdigit() else str(val_j).lower()
                except:
                    compare_extreme = str(val_extreme).lower()
                    compare_j = str(val_j).lower()
                
                # Find min/max
                if reverse:
                    if compare_j > compare_extreme:
                        extreme_idx = j
                else:
                    if compare_j < compare_extreme:
                        extreme_idx = j
            
            arr[i], arr[extreme_idx] = arr[extreme_idx], arr[i]
        
        return arr
    
    @staticmethod
    def _quick_sort_partition(arr: List[Any], low: int, high: int, key: str, reverse: bool) -> int:
        """Helper function for Quick Sort"""
        pivot = arr[high]
        i = low - 1
        
        for j in range(low, high):
            # Get values for comparison
            if key:
                val_j = getattr(arr[j], key) if hasattr(arr[j], key) else arr[j].get(key, "")
                val_pivot = getattr(pivot, key) if hasattr(pivot, key) else pivot.get(key, "")
            else:
                val_j = arr[j]
                val_pivot = pivot
            
            # Convert for comparison
            try:
                compare_j = float(val_j) if str(val_j).replace('.', '').isdigit() else str(val_j).lower()
                compare_pivot = float(val_pivot) if str(val_pivot).replace('.', '').isdigit() else str(val_pivot).lower()
            except:
                compare_j = str(val_j).lower()
                compare_pivot = str(val_pivot).lower()
            
            # Compare condition
            if reverse:
                should_swap = compare_j >= compare_pivot
            else:
                should_swap = compare_j <= compare_pivot
            
            if should_swap:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
    
    @staticmethod
    def _quick_sort_recursive(arr: List[Any], low: int, high: int, key: str, reverse: bool):
        """Recursive Quick Sort implementation"""
        if low < high:
            pi = SortingAlgorithms._quick_sort_partition(arr, low, high, key, reverse)
            SortingAlgorithms._quick_sort_recursive(arr, low, pi - 1, key, reverse)
            SortingAlgorithms._quick_sort_recursive(arr, pi + 1, high, key, reverse)
    
    @staticmethod
    @measure_time
    def quick_sort(data: List[Any], key: str = None, reverse: bool = False) -> List[Any]:
        """Quick Sort - O(n log n) average, O(n²) worst"""
        if not data:
            return data
            
        arr = data.copy()
        SortingAlgorithms._quick_sort_recursive(arr, 0, len(arr) - 1, key, reverse)
        return arr
    
    @staticmethod
    def _merge(left: List[Any], right: List[Any], key: str, reverse: bool) -> List[Any]:
        """Merge two sorted arrays"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            # Get values for comparison
            if key:
                left_val = getattr(left[i], key) if hasattr(left[i], key) else left[i].get(key, "")
                right_val = getattr(right[j], key) if hasattr(right[j], key) else right[j].get(key, "")
            else:
                left_val = left[i]
                right_val = right[j]
            
            # Convert for comparison
            try:
                compare_left = float(left_val) if str(left_val).replace('.', '').isdigit() else str(left_val).lower()
                compare_right = float(right_val) if str(right_val).replace('.', '').isdigit() else str(right_val).lower()
            except:
                compare_left = str(left_val).lower()
                compare_right = str(right_val).lower()
            
            # Compare condition
            if reverse:
                if compare_left >= compare_right:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            else:
                if compare_left <= compare_right:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    @staticmethod
    @measure_time
    def merge_sort(data: List[Any], key: str = None, reverse: bool = False) -> List[Any]:
        """Merge Sort - O(n log n)"""
        if len(data) <= 1:
            return data
            
        mid = len(data) // 2
        left = SortingAlgorithms.merge_sort(data[:mid], key, reverse)
        right = SortingAlgorithms.merge_sort(data[mid:], key, reverse)
        
        return SortingAlgorithms._merge(left, right, key, reverse)
    
    @staticmethod
    @measure_time
    def counting_sort(data: List[Any], key: str = None, reverse: bool = False) -> List[Any]:
        """Counting Sort - O(n + k) for integers"""
        if not data:
            return data
            
        # Extract integer values
        int_values = []
        for item in data:
            if key:
                val = getattr(item, key) if hasattr(item, key) else item.get(key, 0)
            else:
                val = item
            
            try:
                int_val = int(float(val))
                int_values.append(int_val)
            except:
                int_val = hash(str(val)) % 1000  # Fallback for non-numeric
                int_values.append(int_val)
        
        # Counting sort logic
        if not int_values:
            return data.copy()
            
        max_val = max(int_values)
        min_val = min(int_values)
        
        count_range = max_val - min_val + 1
        count = [0] * count_range
        
        for num in int_values:
            count[num - min_val] += 1
        
        # Build output array
        output = []
        for i in range(count_range):
            idx = i if not reverse else count_range - 1 - i
            output.extend([item for item in data if 
                         int(float(getattr(item, key) if key and hasattr(item, key) else item.get(key, 0) if key else item)) == idx + min_val])
        
        return output
    
    @staticmethod
    @measure_time
    def radix_sort(data: List[Any], key: str = None, reverse: bool = False) -> List[Any]:
        """Radix Sort - O(nk) for integers"""
        if not data:
            return data
            
        # Extract integer values
        int_values = []
        for item in data:
            if key:
                val = getattr(item, key) if hasattr(item, key) else item.get(key, 0)
            else:
                val = item
            
            try:
                int_val = int(float(val))
                int_values.append((int_val, item))
            except:
                int_val = hash(str(val)) % 10000  # Fallback
                int_values.append((int_val, item))
        
        if not int_values:
            return data.copy()
        
        # Find maximum number to know number of digits
        max_num = max(abs(val) for val, _ in int_values)
        
        # Do counting sort for every digit
        exp = 1
        while max_num // exp > 0:
            int_values = SortingAlgorithms._radix_counting_sort(int_values, exp, reverse)
            exp *= 10
        
        return [item for _, item in int_values]
    
    @staticmethod
    def _radix_counting_sort(arr: List[Tuple[int, Any]], exp: int, reverse: bool) -> List[Tuple[int, Any]]:
        """Helper for Radix Sort"""
        n = len(arr)
        output = [0] * n
        count = [0] * 10
        
        # Store count of occurrences
        for i in range(n):
            index = (abs(arr[i][0]) // exp) % 10
            count[index] += 1
        
        # Change count[i] so it contains actual position
        for i in range(1, 10):
            count[i] += count[i - 1]
        
        # Build output array
        i = n - 1
        while i >= 0:
            index = (abs(arr[i][0]) // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            i -= 1
        
        if reverse:
            output.reverse()
        
        return output
    
    @staticmethod
    @measure_time
    def bucket_sort(data: List[Any], key: str = None, reverse: bool = False) -> List[Any]:
        """Bucket Sort - O(n + k)"""
        if not data or len(data) <= 1:
            return data.copy()
            
        # Extract float values
        float_values = []
        for item in data:
            if key:
                val = getattr(item, key) if hasattr(item, key) else item.get(key, 0)
            else:
                val = item
            
            try:
                float_val = float(val)
                float_values.append((float_val, item))
            except:
                float_val = hash(str(val)) / 1000.0  # Fallback
                float_values.append((float_val, item))
        
        if not float_values:
            return data.copy()
        
        # Create buckets
        n = len(float_values)
        buckets = [[] for _ in range(n)]
        
        # Put array elements in different buckets
        max_val = max(val for val, _ in float_values)
        min_val = min(val for val, _ in float_values)
        
        if max_val == min_val:
            return data.copy()
        
        for val, item in float_values:
            index = int((val - min_val) * (n - 1) / (max_val - min_val))
            buckets[index].append((val, item))
        
        # Sort individual buckets
        for i in range(n):
            buckets[i] = sorted(buckets[i], key=lambda x: x[0], reverse=reverse)
        
        # Concatenate all buckets into output
        result = []
        for bucket in buckets:
            for _, item in bucket:
                result.append(item)
        
        return result
    
    # ========== ADDITIONAL ALGORITHMS ==========
    
    @staticmethod
    @measure_time
    def pigeonhole_sort(data: List[Any], key: str = None, reverse: bool = False) -> List[Any]:
        """Pigeonhole Sort - O(n + Range) for integers"""
        if not data:
            return data
            
        # Extract integer values
        int_values = []
        for item in data:
            if key:
                val = getattr(item, key) if hasattr(item, key) else item.get(key, 0)
            else:
                val = item
            
            try:
                int_val = int(float(val))
                int_values.append((int_val, item))
            except:
                int_val = hash(str(val)) % 1000  # Fallback
                int_values.append((int_val, item))
        
        if not int_values:
            return data.copy()
        
        # Find min and max values
        min_val = min(val for val, _ in int_values)
        max_val = max(val for val, _ in int_values)
        
        if min_val == max_val:
            return data.copy()
        
        # Create pigeonholes
        size = max_val - min_val + 1
        holes = [[] for _ in range(size)]
        
        # Put items in pigeonholes
        for val, item in int_values:
            holes[val - min_val].append(item)
        
        # Collect items from pigeonholes
        result = []
        if reverse:
            for i in range(size - 1, -1, -1):
                result.extend(holes[i])
        else:
            for i in range(size):
                result.extend(holes[i])
        
        return result
    
    @staticmethod
    def _heapify(arr: List[Any], n: int, i: int, key: str, reverse: bool):
        """Heapify a subtree rooted with node i which is an index in arr[]"""
        extreme = i  # Initialize extreme as root
        left = 2 * i + 1
        right = 2 * i + 2
        
        # Get root value
        if key:
            root_val = getattr(arr[extreme], key) if hasattr(arr[extreme], key) else arr[extreme].get(key, "")
        else:
            root_val = arr[extreme]
        
        try:
            compare_root = float(root_val) if str(root_val).replace('.', '').isdigit() else str(root_val).lower()
        except:
            compare_root = str(root_val).lower()
        
        # Compare with left child
        if left < n:
            if key:
                left_val = getattr(arr[left], key) if hasattr(arr[left], key) else arr[left].get(key, "")
            else:
                left_val = arr[left]
            
            try:
                compare_left = float(left_val) if str(left_val).replace('.', '').isdigit() else str(left_val).lower()
            except:
                compare_left = str(left_val).lower()
            
            if reverse:
                if compare_left > compare_root:
                    extreme = left
            else:
                if compare_left < compare_root:
                    extreme = left
        
        # Compare with right child
        if right < n:
            if key:
                right_val = getattr(arr[extreme], key) if hasattr(arr[extreme], key) else arr[extreme].get(key, "")
            else:
                right_val = arr[extreme]
            
            try:
                compare_extreme = float(right_val) if str(right_val).replace('.', '').isdigit() else str(right_val).lower()
            except:
                compare_extreme = str(right_val).lower()
            
            if key:
                right_val_new = getattr(arr[right], key) if hasattr(arr[right], key) else arr[right].get(key, "")
            else:
                right_val_new = arr[right]
            
            try:
                compare_right = float(right_val_new) if str(right_val_new).replace('.', '').isdigit() else str(right_val_new).lower()
            except:
                compare_right = str(right_val_new).lower()
            
            if reverse:
                if compare_right > compare_extreme:
                    extreme = right
            else:
                if compare_right < compare_extreme:
                    extreme = right
        
        # Change root if needed
        if extreme != i:
            arr[i], arr[extreme] = arr[extreme], arr[i]
            # Heapify the root
            SortingAlgorithms._heapify(arr, n, extreme, key, reverse)
    
    @staticmethod
    @measure_time
    def heap_sort(data: List[Any], key: str = None, reverse: bool = False) -> List[Any]:
        """Heap Sort - O(n log n)"""
        if not data:
            return data
            
        arr = data.copy()
        n = len(arr)
        
        # Build a maxheap or minheap
        for i in range(n // 2 - 1, -1, -1):
            SortingAlgorithms._heapify(arr, n, i, key, reverse)
        
        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]  # swap
            SortingAlgorithms._heapify(arr, i, 0, key, reverse)
        
        return arr
    
    # ========== MULTI-LEVEL SORTING ==========
    
    @staticmethod
    @measure_time
    def multi_level_sort(data: List[Any], sort_criteria: List[Tuple[str, bool, str]]) -> List[Any]:
        """
        Multi-level sorting
        sort_criteria: [(key1, reverse1, algorithm1), (key2, reverse2, algorithm2), ...]
        """
        if not data or not sort_criteria:
            return data.copy()
        
        sorted_data = data.copy()
        
        # Apply sorting criteria in reverse order (stable sort principle)
        for key, reverse, algorithm in reversed(sort_criteria):
            if algorithm == "bubble":
                sorted_data = SortingAlgorithms.bubble_sort(sorted_data, key, reverse)[0]
            elif algorithm == "insertion":
                sorted_data = SortingAlgorithms.insertion_sort(sorted_data, key, reverse)[0]
            elif algorithm == "selection":
                sorted_data = SortingAlgorithms.selection_sort(sorted_data, key, reverse)[0]
            elif algorithm == "quick":
                sorted_data = SortingAlgorithms.quick_sort(sorted_data, key, reverse)[0]
            elif algorithm == "merge":
                sorted_data = SortingAlgorithms.merge_sort(sorted_data, key, reverse)[0]
            elif algorithm == "counting":
                sorted_data = SortingAlgorithms.counting_sort(sorted_data, key, reverse)[0]
            elif algorithm == "radix":
                sorted_data = SortingAlgorithms.radix_sort(sorted_data, key, reverse)[0]
            elif algorithm == "bucket":
                sorted_data = SortingAlgorithms.bucket_sort(sorted_data, key, reverse)[0]
            elif algorithm == "pigeonhole":
                sorted_data = SortingAlgorithms.pigeonhole_sort(sorted_data, key, reverse)[0]
            elif algorithm == "heap":
                sorted_data = SortingAlgorithms.heap_sort(sorted_data, key, reverse)[0]
        
        return sorted_data
    
    # ========== ALGORITHM INFORMATION ==========
    
    @staticmethod
    def get_algorithm_info() -> dict:
        """Get information about all available algorithms"""
        return {
            "bubble": {
                "name": "Bubble Sort",
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "stable": True,
                "description": "Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order."
            },
            "insertion": {
                "name": "Insertion Sort",
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "stable": True,
                "description": "Builds the final sorted array one item at a time by inserting each item into its correct position."
            },
            "selection": {
                "name": "Selection Sort",
                "time_complexity": "O(n²)",
                "space_complexity": "O(1)",
                "stable": False,
                "description": "Repeatedly finds the minimum element from unsorted part and puts it at the beginning."
            },
            "quick": {
                "name": "Quick Sort",
                "time_complexity": "O(n log n) average, O(n²) worst",
                "space_complexity": "O(log n)",
                "stable": False,
                "description": "Divide and conquer algorithm that picks an element as pivot and partitions the array around the pivot."
            },
            "merge": {
                "name": "Merge Sort",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(n)",
                "stable": True,
                "description": "Divide and conquer algorithm that divides the array into halves, sorts them, and merges them."
            },
            "counting": {
                "name": "Counting Sort",
                "time_complexity": "O(n + k)",
                "space_complexity": "O(k)",
                "stable": True,
                "description": "Counts the number of objects having distinct key values, then does arithmetic to calculate positions."
            },
            "radix": {
                "name": "Radix Sort",
                "time_complexity": "O(nk)",
                "space_complexity": "O(n + k)",
                "stable": True,
                "description": "Sorts numbers by processing individual digits starting from least significant digit to most significant."
            },
            "bucket": {
                "name": "Bucket Sort",
                "time_complexity": "O(n + k)",
                "space_complexity": "O(n)",
                "stable": True,
                "description": "Distributes elements into a number of buckets, sorts individual buckets, and concatenates results."
            },
            "pigeonhole": {
                "name": "Pigeonhole Sort",
                "time_complexity": "O(n + Range)",
                "space_complexity": "O(n + Range)",
                "stable": True,
                "description": "Similar to counting sort but works for lists where items are keys themselves."
            },
            "heap": {
                "name": "Heap Sort",
                "time_complexity": "O(n log n)",
                "space_complexity": "O(1)",
                "stable": False,
                "description": "Uses a binary heap data structure to sort elements by building a heap and repeatedly extracting the maximum/minimum."
            }
        }