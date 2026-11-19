#  LinkedIn Architecture & Data Structures (DSA) Simulator

This a project which is only created for the purpose of understanding DSA concepts in social media platforms. Designed specifically as an simple & easy to understand.

---

##  Quick Start & Compilation

### 1. Run Directly with Python
No third-party libraries required (standard Python standard library only: `tkinter`, `heapq`, `collections`, `math`, `time`, `random`):
```bash
py linkedin_simulator.py
# or
python linkedin_simulator.py
```

### 2. Run the Automated Unit Test Suite
```bash
py -m unittest test_linkedin_simulator.py -v
```
Output:
```text
Ran 16 tests in 0.002s
OK
```

### 3. Compile to a Single Standalone Windows `.exe`
Package the entire simulator into an independent portable executable without background terminal windows:
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name "LinkedIn_DSA_Simulator" linkedin_simulator.py
```
The resulting executable will be located in:
```text
dist/LinkedIn_DSA_Simulator.exe
```

---

##  System Architecture: The Split-Screen Philosophy

The application features a hybrid split-screen layout (`1220x720` resolution with high-DPI scaling awareness):

```
┌──────────────────────────────────────┬───────────────────────────────────────────┐
│       LEFT PANEL: THE PRODUCT        │         RIGHT PANEL: THE ENGINE           │
│    (LinkedIn Corporate UI System)    │    (Dark Cyber Visualizer & Telemetry)    │
├──────────────────────────────────────┼───────────────────────────────────────────┤
│ • Branded LinkedIn Clean Aesthetic   │ • Dark Theme Canvas (#0B1120)             │
│ • Tabs: Network | Feed | Chat | Trie │ • Subtle Dot-Grid Spatial Coordinate Web  │
│ • Interactive Controls & Form Inputs │ • Multi-Ring Glowing Nodes & Active Edges │
│ • DSA In-Depth Educational Cards     │ • Live HUD: V, E, N, Depth, Big-O Metrics │
│ • Instant Presets & Event Triggers   │ • Cubic-Eased Frame Animations            │
└──────────────────────────────────────┴───────────────────────────────────────────┘
```

---

##  Data Structures & Algorithmic Analysis

### 1. Connections — Undirected Graph (`GraphNetwork`)
* **Underlying Structure**: Adjacency list backed by Python hash sets: `dict[str, set[str]]`.
* **Complexity**:
  * **Add / Delete Vertex**: $O(1)$ amortized average / $O(\text{deg}(v))$ for edge purges.
  * **Add / Delete Edge**: $O(1)$ amortized average.
  * **Mutual Connections**: Computed via hash set intersection `adj[A] & adj[B]`.
  * **Time Complexity**: $O(\min(\text{deg}(A), \text{deg}(B)))$ — optimal for high-degree hub nodes in power-law social distributions.
  * **Space Complexity**: $O(V + E)$.
* **Visualizer Engine**:
  * Circular trigonometric graph distribution: $x = c_x + r_x \cos(\theta)$, $y = c_y + r_y \sin(\theta)$.
  * **Selected Members (A & B)**: Glowing Blue (`#38BDF8`) with outer glow rings.
  * **Mutual Connections**: Glowing Emerald Green (`#22C55E`).
  * **Shared Edges**: Bold Canary Yellow (`#FACC15`, width 4) linking $A \rightarrow \text{Mutual} \leftarrow B$.

---

### 2. Home Feed — Max-Heap Priority Queue (`MaxHeapFeed`)
* **Underlying Structure**: Priority Queue built on Python's standard `heapq` module using inverted scores (`-score`), alongside a synchronized complete binary tree array (`tree_nodes[]`).
* **Complete Binary Tree Indexing**:
  * $\text{Parent}(i) = \lfloor (i - 1) / 2 \rfloor$
  * $\text{Left}(i) = 2i + 1$
  * $\text{Right}(i) = 2i + 2$
* **Complexity**:
  * **Insertion (Heapify-Up)**: $O(\log N)$ swaps.
  * **Extract-Max (Heapify-Down)**: $O(\log N)$ sifts.
  * **Peek Top**: $O(1)$.
* **Visualizer Engine**:
  * Dynamically scaled tree layout based on binary tree depth: $\text{depth} = \lfloor \log_2(i + 1) \rfloor$.
  * **Smooth Heapify-Up Animation**: Newly published post begins at the bottom leaf node (highlighted in purple), then visually glides up to its parent using cubic interpolation until the heap invariant $\text{Parent.score} \ge \text{Child.score}$ is restored.
  * **Extract-Max Animation**: Root is popped, the last leaf replaces the root, and smoothly sifts down to its mathematically correct position.

---

### 3. Messaging — FIFO Pipeline Queue (`MessagingQueue`)
* **Underlying Structure**: Double-ended queue (`collections.deque`) implemented in C as a doubly-linked list of fixed-size blocks.
* **Complexity**:
  * **Enqueue (Tail push)**: `deque.append()` in strict $O(1)$ time.
  * **Dequeue (Head pop)**: `deque.popleft()` in strict $O(1)$ time.
  * **FIFO Guarantee**: First-In, First-Out packet delivery invariant.
* **Visualizer Engine**:
  * Horizontal pipeline conduit with cybernetic blue guide rails (`#0284C7`) and directional markers.
  * **Enqueue Slide**: New message card enters from the right edge with quartic ease-out deceleration and locks into the queue tail.
  * **Dequeue Slide**: Oldest message at the head smoothly slides out the exit boundary into the conversation transcript, while trailing messages simultaneously slide left.
  * Active pointers visualized with bidirectional yellow connectors (`◀──▶`).

---

### 4. Search Typeahead — Prefix Tree (`SearchTrie`)
* **Underlying Structure**: Multi-way Prefix Tree (`TrieNode`) with child pointers stored in hash maps: `children: dict[str, TrieNode]`.
* **Complexity**:
  * **Prefix Traversal**: $O(L)$ where $L = \text{length of query}$.
  * **Asymptotic Independence**: Query search latency is strictly bounded by string length and is completely independent of the dictionary size $N$ (e.g. millions of LinkedIn profiles).
* **Visualizer Engine**:
  * **Recursive Branch Layout**: Supports arbitrary traversal depths, calculating horizontal bounding boxes dynamically to prevent child overlap.
  * **Real-time Traversal Feedback**: Bound to the `<KeyRelease>` event. As the user types, the exact characters along the active path light up with concentric glowing yellow rings.
  * **Dead Branch Detection**: If a typed prefix does not exist in the Trie, a red alert indicator (`#EF4444`) instantly flags the invalid path.

---

##  Unit Testing Architecture

The project includes an automated test harness in `test_linkedin_simulator.py`:

| Test Case | Target Structure | Method Tested | Verified Invariant |
|---|---|---|---|
| `test_default_initialization` | Graph | `__init__` | Network initializes with $\ge 8$ vertices and $\ge 14$ edges |
| `test_add_and_remove_user` | Graph | `add_user`, `remove_user` | Vertex insertion, deduplication, edge purge |
| `test_add_and_remove_connection`| Graph | `add_connection`, `remove_connection` | Undirected symmetry & removal |
| `test_mutual_connections_set_intersection` | Graph | `get_mutual_connections` | Set intersection correctness: $\text{adj}[u] \cap \text{adj}[v]$ |
| `test_heap_invariant_on_initialization` | Max-Heap | `__init__` | Every $\text{parent.score} \ge \text{child.score}$, root is max |
| `test_prepare_insert_heapify_up` | Max-Heap | `prepare_insert` | $O(\log N)$ swaps bubble element to correct level |
| `test_prepare_extract_heapify_down`| Max-Heap | `prepare_extract` | Sift-down restores heap invariant |
| `test_depth_calculation` | Max-Heap | `depth` | $\lfloor \log_2(N) \rfloor + 1$ accuracy |
| `test_fifo_ordering` | FIFO Queue | `enqueue`, `dequeue` | Strict First-In, First-Out packet delivery |
| `test_peek` | FIFO Queue | `peek` | Inspect head element without popping |
| `test_prefix_search_valid` | Trie | `search_prefix` | $O(L)$ path trace & word suggestions match |
| `test_prefix_search_invalid` | Trie | `search_prefix` | Miss detection & empty suggestion return |
| `test_case_insensitivity` | Trie | `search_prefix` | Lowercase/uppercase query normalization |
| `test_custom_insert_and_retrieval`| Trie | `insert` | Dynamic vocabulary insertion & prefix retrieval |

---

## Project Details

* **Language & Framework**: Python 3.10+ / `tkinter` / `ttk`
