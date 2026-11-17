# 🚀 LinkedIn Architecture & Data Structures (DSA) Simulator v2.0

A high-performance, standalone desktop application built with Python and `tkinter` that simulates four core architectural features of LinkedIn. Designed specifically as an advanced university-level demonstration uniting real-world software engineering with core computer science theory.

---

## 🌟 What's New in v2.0 (The 9.5+ Upgrade)

- **↔ Interactive Draggable Splitter / Resizer**: An interactive vertical divider (`⋮`) sits between the left product panel and the right engine visualizer. Hovering changes the cursor to horizontal resize (`size_we`) and highlights in luminous LinkedIn blue (`#38BDF8`); clicking and dragging smoothly resizes both panels in real time with responsive dynamic text wrapping and automatic canvas redrawing.
- **🎨 Cyberpunk / Dark-Tech Engine Aesthetic**: Canvas visualizer enhanced with a subtle engineering dot-grid background (`#1A2744`), multi-ring glowing pulse effects around active nodes, and refined status HUD telemetry.
- **✨ Multi-Phase Animated Visualizer Engine Across All 4 DSA Features**:
  - **1. Network & Mutual Connections (Undirected Graph)**: Replaced static instant color snaps with a multi-phase discovery sequence:
    - *Phase 1 (Focus)*: Radar beacon shockwaves pulse outward from Member A and Member B with elastic scaling.
    - *Phase 2 (Traversal)*: Electric signal packets travel outward along neighbor edges to visualize querying adjacency hash sets $\text{adj}[A]$ and $\text{adj}[B]$.
    - *Phase 3 (Discovery & Laser Edges)*: Mutual nodes explode with radiant emerald green shockwaves and elastic bounce; golden laser bridge edges unfurl outward from $A$ and $B$ to mutuals with sparkling tips.
    - *Phase 4 (Ambient Glow)*: Continuous gentle breathing pulse keeps mutual nodes and shared edges alive.
    - *Graph Mutations*: Adding users, linking edges, and disconnecting links trigger dedicated pop-in, laser-shoot, and disconnect ripple animations.
  - **2. Feed Ranking & Priority Queue (Max-Heap)**:
    - *Leaf Pop-In*: New posts spawn with an elastic overshoot scale-in (`ease_out_back`) and purple beacon ring.
    - *Comparison Radar*: Pulsing indicator beams preview each comparison between parent and child scores before swapping.
    - *2.5D Orbital Arced Swaps*: Swapping nodes orbit along curved paths with luminous motion blur trails rather than colliding linearly.
    - *Extract-Max Dissipation*: Popped root post elevates upward with golden dissipation rings, while the promoted leaf glides smoothly into the root position.
  - **3. Messaging Pipeline (FIFO Queue)**:
    - *Conveyor Rail Ambiance*: Active conveyor chevrons drift continuously inside the pipeline guide rails to visually reinforce First-In, First-Out directionality.
    - *Elastic Enqueue*: Incoming message cards fly in from the right with elastic docking (`ease_out_back`), docking ripple rings, and a dynamic double-ended pointer (`◀──▶`) that unfurls with a golden spark.
    - *Head Dequeue & Chute Slide*: Head card pulses green, unlinks, and accelerates smoothly out through the exit chute with motion blur, while remaining queue cards glide left simultaneously.
  - **4. Search Typeahead & Prefix Tree (Trie)**:
    - *Sequential Laser Cascade*: Typing triggers a laser beam shooting down the branches from ROOT node to the query tip node at $O(L)$ depth.
    - *Valid Prefix Arrival*: Radiant golden shockwave at the traversal tip, with candidate completion subtrees shimmering in soft emerald green.
    - *Dead-End / Mismatch Alert*: Non-existent prefixes trigger a bright red shockwave, vibration shake, and floating mismatch badge.
    - *Ambient Path Breathing*: Active query prefix branches softly breathe while inspecting results.
- **🔄 Dynamic Graph Mutation at Runtime**: Users can now dynamically add new profiles, create undirected edges between members, and disconnect links on the fly, with automatic canvas redraws.
- **🌲 Adaptive Recursive Trie Visualizer**: The Trie visualizer layout is now fully recursive. It dynamically prioritizes matching prefix branches and renders arbitrary search depths without overlapping nodes.
- **📊 Real-time HUD Telemetry & Operation Counters**: Displays live vertices ($V$), edges ($E$), heap elements ($N$), binary tree depth, active queue buffer size, trie nodes, max depth, and total algorithmic operations performed.
- **🧪 Comprehensive Unit Test Suite**: 16 exhaustive unit tests in `test_linkedin_simulator.py` covering edge cases, invariant proofs, and asymptotic behavior across all four data structures.

---

## 🚀 Quick Start & Compilation

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

## 🖥️ System Architecture: The Split-Screen Philosophy

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

## 📊 Data Structures & Algorithmic Analysis

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

## 🧪 Unit Testing Architecture

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

## 👨‍💻 Author & Coursework Details

* **Student / Author**: Indrajit
* **Coursework**: Data Structures & Algorithms (DSA) Practical Project
* **Language & Framework**: Python 3.10+ / `tkinter` / `ttk`
* **Version**: 2.0 (Enhanced UI/UX, Eased Animations, Unit Tested)
