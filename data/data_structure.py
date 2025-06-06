class MinHeap:
    def __init__(self):
        self.heap = []

    def _parent(self, i): return (i - 1) // 2
    def _left_child(self, i): return 2 * i + 1
    def _right_child(self, i): return 2 * i + 2
    def _has_parent(self, i): return self._parent(i) >= 0
    def _has_left_child(self, i): return self._left_child(i) < len(self.heap)
    def _has_right_child(self, i): return self._right_child(i) < len(self.heap)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _heapify_up(self):
        index = len(self.heap) - 1
        while self._has_parent(index) and self.heap[self._parent(index)][0] > self.heap[index][0]:
            self._swap(self._parent(index), index)
            index = self._parent(index)

    def _heapify_down(self):
        index = 0
        while self._has_left_child(index):
            smaller_child_idx = self._left_child(index)
            if self._has_right_child(index) and self.heap[self._right_child(index)][0] < self.heap[smaller_child_idx][0]:
                smaller_child_idx = self._right_child(index)

            if self.heap[index][0] < self.heap[smaller_child_idx][0]:
                break
            else:
                self._swap(index, smaller_child_idx)
                index = smaller_child_idx

    def push(self, item):
        self.heap.append(item)
        self._heapify_up()

    def pop(self):
        if not self.heap:
            raise IndexError("pop from empty heap")
        if len(self.heap) == 1:
            return self.heap.pop()

        item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down()
        return item

    def is_empty(self):
        return len(self.heap) == 0

    def __len__(self):
        return len(self.heap)

class deque:
    def __init__(self):
        self.data = []

    def append(self, item):
        self.data.append(item)

    def appendleft(self, item):
        self.data.insert(0, item)

    def pop(self):
        return self.data.pop()

    def popleft(self):
        return self.data.pop(0)

    def __len__(self):
        return len(self.data)

def heappush(heap, item):
    heap.append(item)
    _heapify_up(heap, len(heap) - 1)

def heappop(heap):
    if not heap:
        raise IndexError("heappop from empty heap")
    _swap(heap, 0, len(heap) - 1)
    item = heap.pop()
    _heapify_down(heap, 0)
    return item

def _heapify_up(heap, idx):
    while idx > 0:
        parent = (idx - 1) // 2
        if heap[idx] < heap[parent]:
            _swap(heap, idx, parent)
            idx = parent
        else:
            break

def _heapify_down(heap, idx):
    size = len(heap)
    while True:
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        if left < size and heap[left] < heap[smallest]:
            smallest = left
        if right < size and heap[right] < heap[smallest]:
            smallest = right
        if smallest == idx:
            break
        _swap(heap, idx, smallest)
        idx = smallest

def _swap(heap, i, j):
    heap[i], heap[j] = heap[j], heap[i]
