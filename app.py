import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
import time

st.set_page_config(page_title="Algorithms Dashboard", page_icon="📘", layout="wide")

def parse_numbers(text):
    try:
        values = [int(x.strip()) for x in text.split(",") if x.strip()]
        if not values:
            raise ValueError("Enter at least one integer.")
        return values
    except ValueError:
        st.error("Please enter comma-separated integers, for example: 12, 5, 8, 20.")
        return None
def linear_search_steps(arr, key):
    steps = []
    for i, value in enumerate(arr):
        steps.append((i, value, value == key))
        if value == key:
            return i, steps
    return -1, steps
def binary_search_steps(arr, key):
    if arr != sorted(arr):
        return None, [], "Binary Search requires a sorted list."
    low, high = 0, len(arr) - 1
    steps = []
    while low <= high:
        mid = (low + high) // 2
        steps.append((low, high, mid, arr[mid]))
        if arr[mid] == key:
            return mid, steps, None
        elif key < arr[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return -1, steps, None
def bubble_sort(a):
    a = a.copy()
    trace = [a.copy()]
    n = len(a)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                trace.append(a.copy())
    return a, trace
def selection_sort(a):
    a = a.copy()
    trace = [a.copy()]
    n = len(a)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            trace.append(a.copy())
    return a, trace
def insertion_sort(a):
    a = a.copy()
    trace = [a.copy()]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
            trace.append(a.copy())
        a[j + 1] = key
        trace.append(a.copy())
    return a, trace
def merge_sort(a):
    trace = []
    def merge_sort_rec(values):
        if len(values) <= 1:
            return values
        mid = len(values) // 2
        left = merge_sort_rec(values[:mid])
        right = merge_sort_rec(values[mid:])
        merged, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        trace.append(merged.copy())
        return merged
    result = merge_sort_rec(a.copy())
    return result, [a.copy()] + trace + [result.copy()]
def quick_sort(a):
    trace = []
    def quick_sort_rec(values):
        if len(values) <= 1:
            return values
        pivot = values[0]
        left = [x for x in values[1:] if x <= pivot]
        right = [x for x in values[1:] if x > pivot]
        trace.append((left.copy(), pivot, right.copy()))
        return quick_sort_rec(left) + [pivot] + quick_sort_rec(right)
    result = quick_sort_rec(a.copy())
    return result, [a.copy()] + trace + [result.copy()]
st.title("📘 Algorithms Interactive Dashboard")
# st.caption("Searching • Sorting • Greedy Algorithms")

with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Choose a topic",
        ["Overview", "Searching Algorithms", "Sorting Algorithms",
         "Sorting Comparison", "Greedy Algorithms"]
    )

SORTS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
}

COMPARISON = pd.DataFrame([
    ["Bubble Sort", "Θ(n²)", "Θ(n²)", "Θ(n²)", "Θ(1)", "Yes", "Yes"],
    ["Selection Sort", "Θ(n²)", "Θ(n²)", "Θ(n²)", "Θ(1)", "No", "Yes"],
    ["Insertion Sort", "Θ(n)", "Θ(n²)", "Θ(n²)", "Θ(1)", "Yes", "Yes"],
    ["Merge Sort", "Θ(n log n)", "Θ(n log n)", "Θ(n log n)", "Θ(n)", "Yes", "No"],
    ["Quick Sort*", "Θ(n log n)", "Θ(n log n)", "Θ(n²)", "Θ(n)", "No", "No"],
], columns=["Algorithm", "Best Time", "Average Time", "Worst Time",
            "Auxiliary Space", "Stable", "In-place"])

if page == "Overview":
    st.subheader("Explore the algorithms")
    c1, c2, c3 = st.columns(3)
    c1.metric("Searching methods", "2")
    c2.metric("Sorting methods", "5")
    c3.metric("Greedy methods", "2")
    st.markdown("""
    - **Searching:** Linear Search checks items sequentially; Binary Search repeatedly halves a sorted search interval.
    - **Sorting:** Bubble, Selection, Insertion, Merge, and Quick Sort arrange values in ascending order.
    - **Greedy:** Change-Making selects the largest suitable coin denomination; Talk Scheduling repeatedly selects the compatible talk with earliest finish time.
    """)
elif page == "Searching Algorithms":
    st.subheader("Searching Algorithms")
    st.write("Enter a list of integers and a target value.")
    raw = st.text_input("Array (comma-separated)", "12, 5, 8, 20, 7")
    key = st.number_input("Target value", value=20, step=1)
    arr = parse_numbers(raw)
    method = st.selectbox("Search method", ["Linear Search", "Binary Search"])
    if arr is not None:
        if method == "Linear Search":
            idx, steps = linear_search_steps(arr, int(key))
            st.markdown("**Pseudocode**")
            st.code("""procedure LinearSearch(A, n, key)
    for i := 0 to n - 1
        if A[i] = key then return i
    return -1""", language="text")
            st.write("Check each element from left to right.")
            st.dataframe(pd.DataFrame(
                [{"Step": s+1, "Index": i, "Value checked": v,
                  "Match?": "Yes" if found else "No"} for s,(i,v,found) in enumerate(steps)]
            ), use_container_width=True)
        else:
            idx, steps, error = binary_search_steps(arr, int(key))
            st.markdown("**Pseudocode**")
            st.code("""procedure BinarySearch(A, n, key)
    low := 0; high := n - 1
    while low <= high
        mid := floor((low + high) / 2)
        if A[mid] = key then return mid
        else if key < A[mid] then high := mid - 1
        else low := mid + 1
    return -1""", language="text")
            if error:
                st.warning(error)
            else:
                st.dataframe(pd.DataFrame(
                    [{"Step": s+1, "Low": lo, "High": hi, "Mid": mid,
                      "Middle value": val} for s,(lo,hi,mid,val) in enumerate(steps)]
                ), use_container_width=True)
        if idx is not None:
            if idx >= 0:
                st.success(f"Target {key} found at index {idx} (zero-based indexing).")
            else:
                st.error(f"Target {key} was not found. Returned index: -1.")

elif page == "Sorting Algorithms":
    st.subheader("Sorting Demonstration")
    raw = st.text_input("Array to sort (comma-separated)", "5, 1, 4, 2, 8", key="sort_arr")
    algorithm = st.selectbox("Sorting algorithm", list(SORTS.keys()))
    arr = parse_numbers(raw)
    if arr is not None:
        result, trace = SORTS[algorithm](arr)
        st.write("**Pseudocode**")
        pseudo = {
            "Bubble Sort": "for i := 0 to n-2\n    for j := 0 to n-i-2\n        if A[j] > A[j+1] then swap",
            "Selection Sort": "for i := 0 to n-2\n    minIndex := i\n    for j := i+1 to n-1\n        if A[j] < A[minIndex] then minIndex := j\n    swap A[i], A[minIndex]",
            "Insertion Sort": "for i := 1 to n-1\n    key := A[i]\n    j := i-1\n    while j >= 0 and A[j] > key\n        A[j+1] := A[j]\n        j := j-1\n    A[j+1] := key",
            "Merge Sort": "Divide A into two halves\nRecursively sort both halves\nMerge the sorted halves",
            "Quick Sort": "Choose a pivot\nPartition into L (<= pivot) and R (> pivot)\nReturn QuickSort(L) + pivot + QuickSort(R)",
        }
        st.code(pseudo[algorithm], language="text")
        st.write("**Progress snapshots**")
        for i, state in enumerate(trace):
            st.write(f"Step {i}: `{state}`")
        st.success(f"Sorted result: {result}")

elif page == "Sorting Comparison":
    st.subheader("Comparison of Five Sorting Algorithms")
    st.dataframe(COMPARISON, use_container_width=True, hide_index=True)
    st.caption("* Quick Sort space is Θ(n) for the recursive list-based implementation shown here. In-place partition-based variants use different auxiliary space.")
    st.markdown("""
    **Key observations**
    - Insertion Sort is efficient for already sorted or nearly sorted small inputs.
    - Merge Sort guarantees Θ(n log n) time but needs extra memory.
    - Quick Sort is Θ(n log n) on average, but can degrade to Θ(n²).
    - Selection Sort performs Θ(n²) comparisons even when the input is already sorted.
    - Bubble Sort is stable in the adjacent-swap form shown.
    """)

elif page == "Greedy Algorithms":
    st.subheader("Greedy Algorithms")
    tab1, tab2 = st.tabs(["Change-Making", "Talk Scheduling"])
    with tab1:
        st.write("Greedy U.S. coin change using 25¢, 10¢, 5¢, and 1¢.")
        amount = st.number_input("Amount in cents", min_value=0, max_value=100000, value=67, step=1)
        remaining = int(amount)
        rows = []
        for coin, name in [(25,"Quarter"),(10,"Dime"),(5,"Nickel"),(1,"Penny")]:
            count = remaining // coin
            remaining %= coin
            rows.append({"Coin": name, "Value": coin, "Count": count})
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
        st.metric("Total coins", sum(r["Count"] for r in rows))
        st.code("""procedure MakeChange(amount)
    denominations := [25, 10, 5, 1]
    for each coin in denominations
        count := floor(amount / coin)
        output count coins of denomination coin
        amount := amount mod coin""", language="text")
        st.caption("The fewest-coin guarantee applies to this specified U.S. coin system; it is not true for every possible set of denominations.")
    with tab2:
        st.write("Enter talks as start and finish times. The algorithm chooses talks by earliest finish time.")
        default_talks = pd.DataFrame({
            "Talk": ["T1","T2","T3","T4","T5","T6"],
            "Start": [1,3,0,5,8,5],
            "Finish": [4,5,6,7,9,9]
        })
        talks = st.data_editor(default_talks, num_rows="dynamic", use_container_width=True)
        if st.button("Schedule talks"):
            try:
                records = talks.dropna(subset=["Start","Finish"]).to_dict("records")
                ordered = sorted(records, key=lambda x: float(x["Finish"]))
                selected, last_finish = [], float("-inf")
                for talk in ordered:
                    start, finish = float(talk["Start"]), float(talk["Finish"])
                    if start >= last_finish:
                        selected.append(talk)
                        last_finish = finish
                st.success("Selected compatible talks: " + ", ".join(x["Talk"] for x in selected))
                st.dataframe(pd.DataFrame(selected), hide_index=True, use_container_width=True)
            except Exception as exc:
                st.error(f"Please check the talk start and finish values: {exc}")
        st.code("""procedure ScheduleTalks(talks)
    arrange talks in increasing order of finish time
    selected := empty list
    lastFinish := -infinity
    for each talk (start, finish) in talks
        if start >= lastFinish then
            add talk to selected
            lastFinish := finish
    return selected""", language="text")

st.divider()
# st.caption("Algorithms Chapter 3 learning dashboard • Educational demonstrations")
