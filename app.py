#to run this sorting visualizer write python app.py
from flask import Flask, render_template, request, jsonify
import time
import webbrowser
import threading

app = Flask(__name__)

def bubble_sort(arr):
    steps = []
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                steps.append((arr[:], [j, j + 1]))  
    return steps

def insertion_sort(arr):
    steps = []
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        steps.append((arr[:], [i, j + 1]))
    return steps

def selection_sort(arr):
    steps = []
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append((arr[:], [i, min_idx]))
    return steps

def quick_sort(arr):
    steps = []

    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append((arr[:], [i, j]))
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        steps.append((arr[:], [i + 1, high]))
        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort_recursive(low, pi - 1)
            quick_sort_recursive(pi + 1, high)

    quick_sort_recursive(0, len(arr) - 1)
    return steps

def merge_sort(arr):
    steps = []

    def merge(left, mid, right):
        left_half = arr[left:mid+1]
        right_half = arr[mid+1:right+1]

        i, j, k = 0, 0, left

        while i < len(left_half) and j < len(right_half):
            if left_half[i] <= right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            steps.append((arr[:], [k]))
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            steps.append((arr[:], [k]))
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            steps.append((arr[:], [k]))
            j += 1
            k += 1

    def merge_sort_recursive(left, right):
        if left < right:
            mid = (left + right) // 2
            merge_sort_recursive(left, mid)
            merge_sort_recursive(mid + 1, right)
            merge(left, mid, right)

    merge_sort_recursive(0, len(arr) - 1)
    return steps

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sort', methods=['POST'])
def sort():
    data = request.get_json()
    algorithm = data['algorithm']
    array = data['array']

    sorting_algorithms = {
        'bubble': bubble_sort,
        'insertion': insertion_sort,
        'selection': selection_sort,
        'quick': quick_sort,
        'merge': merge_sort
    }

    if algorithm in sorting_algorithms:
        steps = sorting_algorithms[algorithm](array[:])
        return jsonify({"steps": steps})  # Fixed response structure
    
    return jsonify({"steps": []})

# Auto-open browser
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == '__main__':  # Fixed the incorrect `_name_` and `_main_`
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True)
