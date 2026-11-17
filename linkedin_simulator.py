# ==============================================================================
# LINKEDIN DATA STRUCTURES & ALGORITHMS (DSA) SIMULATOR  v2.0
# Standalone Python Desktop Application — University Coursework Demonstration
#
# FEATURES:
#   1. Network Tab   — Undirected Graph (Adjacency List + Hash Sets)
#   2. Feed Tab      — Max-Heap Priority Queue (Complete Binary Tree)
#   3. Messaging Tab — FIFO Queue (Doubly-Linked List / collections.deque)
#   4. Search Tab    — Trie / Prefix Tree (Typeahead Auto-Complete)
#
# v2.0 HIGHLIGHTS:
#   • Smooth cubic-eased animations on every visualization
#   • Add / Remove users & connections at runtime (Network tab)
#   • Recursive Trie layout supporting arbitrary traversal depth
#   • Dot-grid engine background, glow effects, pulsing highlights
#   • Live HUD telemetry with node / edge / depth counters
#   • Unit tests in test_linkedin_simulator.py
#
# PYINSTALLER:
#   pip install pyinstaller
#   pyinstaller --onefile --noconsole --name "LinkedIn_DSA_Simulator" linkedin_simulator.py
# ==============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import collections
import heapq
import math
import time
import random

# Windows High-DPI Scaling Awareness
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass


# ==============================================================================
# COLOR PALETTE & DESIGN TOKENS
# ==============================================================================
# Left Panel — Professional LinkedIn Theme
LI_BLUE         = "#0A66C2"
LI_DARK_BLUE    = "#004182"
LI_LIGHT_BLUE   = "#E8F3FF"
LI_BG           = "#F3F2EF"
LI_CARD_BG      = "#FFFFFF"
LI_BORDER       = "#E0DFDC"
LI_TEXT_MAIN    = "#191919"
LI_TEXT_MUTED   = "#666666"
LI_GREEN        = "#057642"
LI_SECTION_BG   = "#F8FAFC"

# Right Panel — Dark Cyber Visualizer Engine
ENGINE_BG       = "#0B1120"
ENGINE_CARD     = "#1E293B"
ENGINE_CARD_ALT = "#162032"
ENGINE_BORDER   = "#334155"
ENGINE_LINE     = "#475569"
TEXT_BRIGHT     = "#F8FAFC"
TEXT_DIM        = "#94A3B8"
GRID_DOT        = "#1A2744"

# Semantic Accent Colors
COLOR_BLUE      = "#38BDF8"
COLOR_GREEN     = "#22C55E"
COLOR_YELLOW    = "#FACC15"
COLOR_PURPLE    = "#A855F7"
COLOR_RED       = "#EF4444"
COLOR_ORANGE    = "#F97316"
COLOR_CYAN      = "#06B6D4"
COLOR_PINK      = "#EC4899"

# Glow / Pulse palette (rings around highlighted nodes)
GLOW_BLUE       = "#1E40AF"
GLOW_GREEN      = "#166534"
GLOW_YELLOW     = "#854D0E"
GLOW_PURPLE     = "#6B21A8"


# ==============================================================================
# ANIMATION & MATH UTILITIES
# ==============================================================================
def ease_in_out_cubic(t: float) -> float:
    """Cubic ease-in-out for smooth acceleration / deceleration."""
    if t < 0.5:
        return 4.0 * t * t * t
    return 1.0 - pow(-2.0 * t + 2.0, 3) / 2.0


def ease_out_quart(t: float) -> float:
    """Quartic ease-out — fast start, gentle landing."""
    return 1.0 - pow(1.0 - t, 4)


def ease_out_back(t: float, s: float = 1.70158) -> float:
    """Overshoot ease-out — elastic pop / docking feel."""
    t = t - 1.0
    return t * t * ((s + 1.0) * t + s) + 1.0


def ease_out_bounce(t: float) -> float:
    """Bounce ease-out for landing / impacts."""
    if t < (1 / 2.75):
        return 7.5625 * t * t
    elif t < (2 / 2.75):
        t -= (1.5 / 2.75)
        return 7.5625 * t * t + 0.75
    elif t < (2.5 / 2.75):
        t -= (2.25 / 2.75)
        return 7.5625 * t * t + 0.9375
    else:
        t -= (2.625 / 2.75)
        return 7.5625 * t * t + 0.984375


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation between a and b."""
    return a + (b - a) * t


def hex_to_rgb(h: str):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))
    return f"#{r:02x}{g:02x}{b:02x}"


def lerp_color(c1: str, c2: str, t: float) -> str:
    """Linearly interpolate between two hex colors."""
    t = max(0.0, min(1.0, t))
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex(lerp(r1, r2, t), lerp(g1, g2, t), lerp(b1, b2, t))


# ==============================================================================
# 1. UNDIRECTED GRAPH — ADJACENCY LIST WITH HASH SETS
# ==============================================================================
class GraphNetwork:
    """
    Undirected Graph using an Adjacency List of Hash Sets.
    Supports dynamic add / remove of users and connections.

    Complexities:
        - add_user / remove_user   : O(1) average / O(deg(v))
        - add_connection / remove  : O(1) average
        - get_mutual_connections   : O(min(deg(u), deg(v)))   via set intersection
        - Space                    : O(V + E)
    """

    def __init__(self):
        self.adj: dict[str, set[str]] = collections.defaultdict(set)
        self.roles: dict[str, str] = {}
        self._initialize_default_network()

    # ---- Setup ---------------------------------------------------------------
    def _initialize_default_network(self):
        profiles = [
            ("Satya Nadella",    "CEO @ Microsoft"),
            ("Sundar Pichai",    "CEO @ Alphabet"),
            ("Sam Altman",       "CEO @ OpenAI"),
            ("Demis Hassabis",   "CEO @ Google DeepMind"),
            ("Mira Murati",      "Tech Executive"),
            ("Geoffrey Hinton",  "Turing Laureate & AI Pioneer"),
            ("Yann LeCun",       "Chief AI Scientist @ Meta"),
            ("Fei-Fei Li",       "Professor @ Stanford AI Lab"),
        ]
        for name, role in profiles:
            self.add_user(name, role)

        connections = [
            ("Satya Nadella", "Sundar Pichai"),
            ("Satya Nadella", "Sam Altman"),
            ("Satya Nadella", "Demis Hassabis"),
            ("Sundar Pichai", "Demis Hassabis"),
            ("Sundar Pichai", "Geoffrey Hinton"),
            ("Sundar Pichai", "Fei-Fei Li"),
            ("Sam Altman",    "Mira Murati"),
            ("Sam Altman",    "Demis Hassabis"),
            ("Demis Hassabis","Yann LeCun"),
            ("Demis Hassabis","Geoffrey Hinton"),
            ("Mira Murati",   "Yann LeCun"),
            ("Geoffrey Hinton","Yann LeCun"),
            ("Geoffrey Hinton","Fei-Fei Li"),
            ("Yann LeCun",    "Fei-Fei Li"),
        ]
        for u, v in connections:
            self.add_connection(u, v)

    # ---- Mutations -----------------------------------------------------------
    def add_user(self, name: str, role: str = "LinkedIn Member") -> bool:
        name = name.strip()
        if not name:
            return False
        if name not in self.adj:
            self.adj[name] = set()
            self.roles[name] = role
            return True
        return False

    def remove_user(self, name: str) -> bool:
        if name not in self.adj:
            return False
        for neighbor in list(self.adj[name]):
            self.adj[neighbor].discard(name)
        del self.adj[name]
        self.roles.pop(name, None)
        return True

    def add_connection(self, u: str, v: str) -> bool:
        if u in self.adj and v in self.adj and u != v:
            if v not in self.adj[u]:
                self.adj[u].add(v)
                self.adj[v].add(u)
                return True
        return False

    def remove_connection(self, u: str, v: str) -> bool:
        if u in self.adj and v in self.adj:
            if v in self.adj[u]:
                self.adj[u].discard(v)
                self.adj[v].discard(u)
                return True
        return False

    # ---- Queries -------------------------------------------------------------
    def get_mutual_connections(self, u: str, v: str) -> set:
        if u not in self.adj or v not in self.adj:
            return set()
        return self.adj[u] & self.adj[v]

    def get_users(self) -> list:
        return sorted(list(self.adj.keys()))

    def edge_count(self) -> int:
        return sum(len(nbrs) for nbrs in self.adj.values()) // 2

    def has_connection(self, u: str, v: str) -> bool:
        return u in self.adj and v in self.adj[u]


# ==============================================================================
# 2. HOME FEED — MAX-HEAP PRIORITY QUEUE
# ==============================================================================
class FeedPost:
    __slots__ = ("post_id", "author", "content", "score")

    def __init__(self, post_id, author, content, score):
        self.post_id = post_id
        self.author  = author
        self.content = content
        self.score   = int(score)

    def __repr__(self):
        return f"Post(id={self.post_id}, author='{self.author}', score={self.score})"


class MaxHeapFeed:
    """
    Priority Queue built on heapq with inverted scores (-score).
    Maintains a parallel complete binary tree array for visualization
    and step-by-step heapify animations.

    Complexities:
        - Insert   (heapify-up)   : O(log N)
        - Extract Max (heapify-down): O(log N)
        - Peek top               : O(1)
    """

    def __init__(self):
        self.pq: list = []
        self.tree_nodes: list[FeedPost] = []
        self.counter = 0
        self._initialize_default_feed()

    def _initialize_default_feed(self):
        sample_posts = [
            ("Demis Hassabis", "Excited to share our breakthrough in protein folding & AI!", 950),
            ("Satya Nadella",  "Empowering every person and organization on the planet to achieve more.", 820),
            ("Fei-Fei Li",    "Human-centered AI must remain our guiding compass.", 760),
            ("Sam Altman",    "Compute will be the fundamental currency of the future economy.", 640),
            ("Yann LeCun",    "Auto-regressive LLMs are not the complete path to genuine AGI.", 580),
            ("Sundar Pichai", "Quantum computing reaches an exciting new milestone today.", 490),
            ("Mira Murati",   "Safety and alignment must be integrated from the foundation up.", 320),
        ]
        for author, content, score in sample_posts:
            self.counter += 1
            post = FeedPost(self.counter, author, content, score)
            heapq.heappush(self.pq, (-post.score, self.counter, post))
            self.tree_nodes.append(post)
            curr = len(self.tree_nodes) - 1
            while curr > 0:
                parent = (curr - 1) // 2
                if self.tree_nodes[curr].score > self.tree_nodes[parent].score:
                    self.tree_nodes[curr], self.tree_nodes[parent] = (
                        self.tree_nodes[parent], self.tree_nodes[curr])
                    curr = parent
                else:
                    break

    def prepare_insert(self, author, content, score):
        self.counter += 1
        post = FeedPost(self.counter, author, content, score)
        heapq.heappush(self.pq, (-post.score, self.counter, post))
        self.tree_nodes.append(post)
        curr = len(self.tree_nodes) - 1
        swap_steps = []
        temp = list(self.tree_nodes)
        while curr > 0:
            parent = (curr - 1) // 2
            if temp[curr].score > temp[parent].score:
                swap_steps.append((curr, parent))
                temp[curr], temp[parent] = temp[parent], temp[curr]
                curr = parent
            else:
                break
        return post, swap_steps

    def execute_single_swap(self, i, j):
        if 0 <= i < len(self.tree_nodes) and 0 <= j < len(self.tree_nodes):
            self.tree_nodes[i], self.tree_nodes[j] = self.tree_nodes[j], self.tree_nodes[i]

    def prepare_extract(self):
        if not self.pq or not self.tree_nodes:
            return None, []
        _, _, popped = heapq.heappop(self.pq)
        if len(self.tree_nodes) == 1:
            self.tree_nodes.pop()
            return popped, []
        last = self.tree_nodes.pop()
        self.tree_nodes[0] = last
        swap_steps = []
        curr, n = 0, len(self.tree_nodes)
        temp = list(self.tree_nodes)
        while True:
            left, right, largest = 2*curr+1, 2*curr+2, curr
            if left < n and temp[left].score > temp[largest].score:
                largest = left
            if right < n and temp[right].score > temp[largest].score:
                largest = right
            if largest != curr:
                swap_steps.append((curr, largest))
                temp[curr], temp[largest] = temp[largest], temp[curr]
                curr = largest
            else:
                break
        return popped, swap_steps

    def depth(self) -> int:
        if not self.tree_nodes:
            return 0
        return math.floor(math.log2(len(self.tree_nodes))) + 1


# ==============================================================================
# 3. MESSAGING FIFO QUEUE — COLLECTIONS.DEQUE
# ==============================================================================
class MessagePacket:
    __slots__ = ("msg_id", "sender", "text", "timestamp", "color")

    COLORS = ["#0284C7", "#059669", "#7C3AED", "#DB2777",
              "#D97706", "#2563EB", "#0D9488", "#7C2D12"]

    def __init__(self, msg_id, sender, text, timestamp=None):
        self.msg_id    = msg_id
        self.sender    = sender
        self.text      = text
        self.timestamp = timestamp or time.strftime("%H:%M:%S")
        self.color     = random.choice(self.COLORS)


class MessagingQueue:
    """
    FIFO Queue using collections.deque (doubly-linked list).
        - Enqueue (tail) : O(1)   deque.append()
        - Dequeue (head) : O(1)   deque.popleft()
    """

    def __init__(self):
        self.queue: collections.deque = collections.deque()
        self.counter = 100
        self.delivered_history: list[MessagePacket] = []
        self._initialize_default_messages()

    def _initialize_default_messages(self):
        presets = [
            ("Satya Nadella", "Excited to partner with your AI team on this initiative!"),
            ("Sundar Pichai", "Let's schedule a brief sync regarding the research demo."),
            ("Sam Altman",    "Can we review the latency benchmarks for the new release?"),
        ]
        for sender, text in presets:
            self.enqueue(sender, text)

    def enqueue(self, sender, text) -> MessagePacket:
        self.counter += 1
        msg = MessagePacket(self.counter, sender, text)
        self.queue.append(msg)
        return msg

    def dequeue(self):
        if not self.queue:
            return None
        msg = self.queue.popleft()
        self.delivered_history.append(msg)
        return msg

    def peek(self):
        return self.queue[0] if self.queue else None


# ==============================================================================
# 4. SEARCH TYPEAHEAD — TRIE (PREFIX TREE)
# ==============================================================================
class TrieNode:
    __slots__ = ("char", "children", "is_terminal", "full_words", "x", "y")

    def __init__(self, char=""):
        self.char        = char
        self.children: dict[str, 'TrieNode'] = {}
        self.is_terminal = False
        self.full_words: list[str] = []
        self.x = 0.0
        self.y = 0.0


class SearchTrie:
    """
    Trie (Prefix Tree) where each node stores a dictionary of child characters.
        - Prefix traversal : O(L)   where L = len(query)
        - Independent of dictionary size N
    """

    def __init__(self):
        self.root = TrieNode("[ROOT]")
        self._initialize_dictionary()

    def _initialize_dictionary(self):
        terms = [
            "software engineer", "software architect", "software intern",
            "solutions architect", "soft skills trainer",
            "data scientist", "data analyst", "data engineer", "database admin",
            "product manager", "product designer", "project manager",
            "devops engineer", "developer advocate", "system admin",
            "python developer", "python backend lead",
            "machine learning engineer", "ml researcher",
            "frontend developer", "fullstack engineer",
            "satya nadella", "sundar pichai", "sam altman",
            "demis hassabis", "geoffrey hinton", "yann lecun", "fei-fei li",
        ]
        for word in terms:
            self.insert(word)

    def insert(self, word: str):
        word_clean = word.strip()
        if not word_clean:
            return
        curr = self.root
        if word_clean not in curr.full_words:
            curr.full_words.append(word_clean)
        for ch in word_clean.lower():
            if ch not in curr.children:
                curr.children[ch] = TrieNode(ch)
            curr = curr.children[ch]
            if word_clean not in curr.full_words:
                curr.full_words.append(word_clean)
        curr.is_terminal = True

    def search_prefix(self, prefix: str):
        prefix_clean = prefix.strip().lower()
        curr = self.root
        traversed = [curr]
        for ch in prefix_clean:
            if ch in curr.children:
                curr = curr.children[ch]
                traversed.append(curr)
            else:
                return traversed, [], False
        return traversed, curr.full_words, True

    def total_nodes(self) -> int:
        count = 0
        stack = [self.root]
        while stack:
            node = stack.pop()
            count += 1
            for child in node.children.values():
                stack.append(child)
        return count

    def max_depth(self) -> int:
        def _depth(node, d):
            if not node.children:
                return d
            return max(_depth(c, d + 1) for c in node.children.values())
        return _depth(self.root, 0)


# ==============================================================================
# MAIN APPLICATION — SPLIT-SCREEN UI WITH VISUALIZER ENGINE
# ==============================================================================
class LinkedInDSASimulator(tk.Tk):

    # ---- Window Setup --------------------------------------------------------
    def __init__(self):
        super().__init__()
        self.title("LinkedIn System Architecture & Data Structures Simulator  v2.0")
        self.geometry("1220x720")
        self.minsize(1080, 640)
        self.configure(bg=LI_BG)

        # Data-structure engines
        self.graph_engine     = GraphNetwork()
        self.feed_engine      = MaxHeapFeed()
        self.messaging_engine = MessagingQueue()
        self.trie_engine      = SearchTrie()

        # Animation bookkeeping
        self.active_animation = None
        self.pulse_job        = None
        self.pulse_tick       = 0
        self.last_mutual_data = None
        self.last_trie_data   = None
        self.current_tab      = "network"
        self.op_counter       = 0           # total operations performed

        self._configure_styles()
        self._build_layout()
        self.after(120, lambda: self._switch_tab_view("network"))

    # ---- ttk Styling ---------------------------------------------------------
    def _configure_styles(self):
        s = ttk.Style()
        s.theme_use("clam")

        s.configure("TNotebook", background=LI_BG, borderwidth=0)
        s.configure("TNotebook.Tab", background="#E2E8F0", foreground=LI_TEXT_MAIN,
                    font=("Segoe UI", 10, "bold"), padding=[16, 8])
        s.map("TNotebook.Tab",
              background=[("selected", LI_BLUE)],
              foreground=[("selected", "#FFFFFF")])

        s.configure("Primary.TButton", background=LI_BLUE, foreground="#FFFFFF",
                    font=("Segoe UI", 9, "bold"), borderwidth=0, padding=6)
        s.map("Primary.TButton",
              background=[("active", LI_DARK_BLUE), ("pressed", LI_DARK_BLUE)])

        s.configure("Danger.TButton", background="#DC2626", foreground="#FFFFFF",
                    font=("Segoe UI", 9, "bold"), borderwidth=0, padding=6)
        s.map("Danger.TButton",
              background=[("active", "#B91C1C"), ("pressed", "#B91C1C")])

        s.configure("Success.TButton", background="#059669", foreground="#FFFFFF",
                    font=("Segoe UI", 9, "bold"), borderwidth=0, padding=6)
        s.map("Success.TButton",
              background=[("active", "#047857"), ("pressed", "#047857")])

        s.configure("Secondary.TButton", background="#E2E8F0", foreground=LI_TEXT_MAIN,
                    font=("Segoe UI", 9), borderwidth=0, padding=5)
        s.map("Secondary.TButton", background=[("active", "#CBD5E1")])

        s.configure("Accent.TButton", background=COLOR_PURPLE, foreground="#FFFFFF",
                    font=("Segoe UI", 9, "bold"), borderwidth=0, padding=6)
        s.map("Accent.TButton",
              background=[("active", "#7C3AED"), ("pressed", "#7C3AED")])

    # ---- Main Layout ---------------------------------------------------------
    def _build_layout(self):
        self.split_container = tk.Frame(self, bg=LI_BG)
        self.split_container.pack(fill=tk.BOTH, expand=True)

        # LEFT PANEL — LinkedIn Product UI
        self.left_panel = tk.Frame(self.split_container, bg=LI_BG, width=540)
        self.left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(10, 0), pady=10)
        self.left_panel.pack_propagate(False)

        # Header
        header = tk.Frame(self.left_panel, bg=LI_CARD_BG, height=50, relief=tk.SOLID, bd=1)
        header.pack(fill=tk.X, pady=(0, 10))

        logo = tk.Label(header, text=" in ", bg=LI_BLUE, fg="#FFFFFF",
                        font=("Segoe UI", 16, "bold"), padx=6, pady=2)
        logo.pack(side=tk.LEFT, padx=10, pady=8)

        tk.Label(header, text="LinkedIn System Architecture Demonstrator",
                 bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                 font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=4)

        ver_lbl = tk.Label(header, text="v2.0", bg=LI_LIGHT_BLUE, fg=LI_BLUE,
                           font=("Consolas", 8, "bold"), padx=6, pady=1)
        ver_lbl.pack(side=tk.LEFT, padx=8)

        # Notebook
        self.notebook = ttk.Notebook(self.left_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_network   = tk.Frame(self.notebook, bg=LI_BG)
        self.tab_feed      = tk.Frame(self.notebook, bg=LI_BG)
        self.tab_messaging = tk.Frame(self.notebook, bg=LI_BG)
        self.tab_search    = tk.Frame(self.notebook, bg=LI_BG)

        self.notebook.add(self.tab_network,   text="  🌐 Network  ")
        self.notebook.add(self.tab_feed,      text="  📰 Feed  ")
        self.notebook.add(self.tab_messaging, text="  💬 Messaging  ")
        self.notebook.add(self.tab_search,    text="  🔍 Search  ")

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        self._build_network_tab()
        self._build_feed_tab()
        self._build_messaging_tab()
        self._build_search_tab()

        # INTERACTIVE RESIZABLE SPLITTER (Draggable Divider between Left & Right)
        self.splitter = tk.Frame(self.split_container, bg="#CBD5E1", width=9, cursor="size_we")
        self.splitter.pack(side=tk.LEFT, fill=tk.Y, padx=4, pady=10)
        self.splitter.pack_propagate(False)

        # Centered grip icon (⋮)
        self.splitter_grip = tk.Label(self.splitter, text="⋮", bg="#CBD5E1", fg="#64748B",
                                      font=("Segoe UI", 12, "bold"), cursor="size_we")
        self.splitter_grip.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Splitter event bindings for hover and dragging
        for widget in (self.splitter, self.splitter_grip):
            widget.bind("<Enter>", self._on_splitter_enter)
            widget.bind("<Leave>", self._on_splitter_leave)
            widget.bind("<Button-1>", self._on_splitter_press)
            widget.bind("<B1-Motion>", self._on_splitter_drag)
            widget.bind("<ButtonRelease-1>", self._on_splitter_release)

        # RIGHT PANEL — Visualizer Engine
        self.right_panel = tk.Frame(self.split_container, bg=ENGINE_BG)
        self.right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=10)

        # HUD top bar
        self.hud_bar = tk.Frame(self.right_panel, bg=ENGINE_CARD, height=44)
        self.hud_bar.pack(fill=tk.X)

        self.hud_title = tk.Label(self.hud_bar,
                                  text="ENGINE: UNDIRECTED GRAPH (ADJACENCY LIST)",
                                  bg=ENGINE_CARD, fg=COLOR_BLUE,
                                  font=("Consolas", 10, "bold"))
        self.hud_title.pack(side=tk.LEFT, padx=14, pady=8)

        self.hud_complexity = tk.Label(self.hud_bar,
                                       text="Mutuals: O(min(deg(u), deg(v)))",
                                       bg=ENGINE_CARD, fg=TEXT_BRIGHT,
                                       font=("Consolas", 9))
        self.hud_complexity.pack(side=tk.RIGHT, padx=14, pady=8)

        # HUD stats sub-bar
        self.hud_stats_bar = tk.Frame(self.right_panel, bg=ENGINE_CARD_ALT, height=24)
        self.hud_stats_bar.pack(fill=tk.X)

        self.hud_stats_lbl = tk.Label(self.hud_stats_bar,
                                      text="V=8 | E=14 | ops=0",
                                      bg=ENGINE_CARD_ALT, fg=COLOR_CYAN,
                                      font=("Consolas", 8))
        self.hud_stats_lbl.pack(side=tk.LEFT, padx=14, pady=3)

        self.hud_struct_lbl = tk.Label(self.hud_stats_bar,
                                       text="dict[str, set[str]]",
                                       bg=ENGINE_CARD_ALT, fg=TEXT_DIM,
                                       font=("Consolas", 8))
        self.hud_struct_lbl.pack(side=tk.RIGHT, padx=14, pady=3)

        # Main canvas
        self.canvas = tk.Canvas(self.right_panel, bg=ENGINE_BG, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        # Footer status
        self.hud_footer = tk.Frame(self.right_panel, bg=ENGINE_CARD, height=32)
        self.hud_footer.pack(fill=tk.X)

        self.status_lbl = tk.Label(self.hud_footer,
                                   text="▶  Engine ready. Awaiting user interaction.",
                                   bg=ENGINE_CARD, fg=TEXT_DIM,
                                   font=("Segoe UI", 9))
        self.status_lbl.pack(side=tk.LEFT, padx=12, pady=6)

    # ---- Splitter Drag & Resize Handlers ------------------------------------
    def _on_splitter_enter(self, event):
        self.splitter.configure(bg=COLOR_BLUE)
        self.splitter_grip.configure(bg=COLOR_BLUE, fg="#FFFFFF")
        if not getattr(self, "_is_dragging_splitter", False):
            self._prev_status_text = self.status_lbl.cget("text")
            self.status_lbl.config(text="↔  Splitter: Click & drag horizontally to resize Product / Engine panels.")

    def _on_splitter_leave(self, event):
        if not getattr(self, "_is_dragging_splitter", False):
            self.splitter.configure(bg="#CBD5E1")
            self.splitter_grip.configure(bg="#CBD5E1", fg="#64748B")
            if hasattr(self, "_prev_status_text"):
                self.status_lbl.config(text=self._prev_status_text)

    def _on_splitter_press(self, event):
        self._is_dragging_splitter = True
        self._splitter_start_x = event.x_root
        self._splitter_start_w = self.left_panel.winfo_width()
        self.splitter.configure(bg=LI_DARK_BLUE)
        self.splitter_grip.configure(bg=LI_DARK_BLUE, fg="#FFFFFF")

    def _on_splitter_drag(self, event):
        if not getattr(self, "_is_dragging_splitter", False):
            return
        delta = event.x_root - self._splitter_start_x
        total_w = self.split_container.winfo_width() or self.winfo_width()
        min_w = 360
        max_w = max(min_w + 60, total_w - 420)
        new_w = max(min_w, min(max_w, self._splitter_start_w + delta))
        self.left_panel.configure(width=new_w)
        self._update_left_panel_wraplength(new_w)

    def _on_splitter_release(self, event):
        self._is_dragging_splitter = False
        self.splitter.configure(bg="#CBD5E1")
        self.splitter_grip.configure(bg="#CBD5E1", fg="#64748B")
        if hasattr(self, "_prev_status_text"):
            self.status_lbl.config(text=self._prev_status_text)

    def _update_left_panel_wraplength(self, left_w):
        wrap = max(280, left_w - 60)
        if hasattr(self, "mutual_result_lbl"):
            self.mutual_result_lbl.configure(wraplength=wrap)
        if hasattr(self, "served_lbl"):
            self.served_lbl.configure(wraplength=wrap)

    # ---- Tab Switching -------------------------------------------------------
    def _on_tab_changed(self, event):
        idx = self.notebook.index(self.notebook.select())
        self._switch_tab_view(["network", "feed", "messaging", "search"][idx])

    def _switch_tab_view(self, tab):
        self.current_tab = tab
        self.cancel_active_animation()
        self._stop_pulse()
        self.pulse_tick = 0
        self.last_mutual_data = None
        self.last_trie_data = None

        if tab == "network":
            v = len(self.graph_engine.adj)
            e = self.graph_engine.edge_count()
            self.hud_title.config(text="ENGINE: UNDIRECTED GRAPH (ADJACENCY LIST)", fg=COLOR_BLUE)
            self.hud_complexity.config(text="Mutuals: O(min(deg(u), deg(v))) | Space: O(V + E)")
            self.hud_stats_lbl.config(text=f"V={v} | E={e} | ops={self.op_counter}")
            self.hud_struct_lbl.config(text="dict[str, set[str]]")
            self.status_lbl.config(text="▶  Graph view active. Select two users and click 'Check Mutuals'.")
            self.draw_graph()

        elif tab == "feed":
            n = len(self.feed_engine.tree_nodes)
            d = self.feed_engine.depth()
            self.hud_title.config(text="ENGINE: MAX-HEAP PRIORITY QUEUE", fg=COLOR_PURPLE)
            self.hud_complexity.config(text="Insert: O(log N) | Extract: O(log N) | Peek: O(1)")
            self.hud_stats_lbl.config(text=f"N={n} | depth={d} | ops={self.op_counter}")
            self.hud_struct_lbl.config(text="heapq (inverted) + tree_nodes[]")
            self.status_lbl.config(text="▶  Complete binary tree view. Root = max engagement score.")
            self.draw_heap_tree()

        elif tab == "messaging":
            q = len(self.messaging_engine.queue)
            self.hud_title.config(text="ENGINE: FIFO QUEUE (DOUBLY-LINKED LIST PIPELINE)", fg=COLOR_GREEN)
            self.hud_complexity.config(text="Enqueue (Tail): O(1) | Dequeue (Head): O(1)")
            self.hud_stats_lbl.config(text=f"buffered={q} | delivered={len(self.messaging_engine.delivered_history)} | ops={self.op_counter}")
            self.hud_struct_lbl.config(text="collections.deque")
            self.status_lbl.config(text="▶  Horizontal pipeline. FIFO order — first in, first out.")
            self.draw_messaging_pipeline()

        elif tab == "search":
            tn = self.trie_engine.total_nodes()
            md = self.trie_engine.max_depth()
            self.hud_title.config(text="ENGINE: TRIE / PREFIX TREE (TYPEAHEAD)", fg=COLOR_YELLOW)
            self.hud_complexity.config(text="Prefix Traversal: O(L) where L = len(query)")
            self.hud_stats_lbl.config(text=f"trie_nodes={tn} | max_depth={md} | ops={self.op_counter}")
            self.hud_struct_lbl.config(text="TrieNode { children: dict[str, TrieNode] }")
            self.status_lbl.config(text="▶  Cascading letter tree. Active path highlighted in real time.")
            q = self.search_entry.get() if hasattr(self, "search_entry") else ""
            self.draw_trie_tree(q)

    def cancel_active_animation(self):
        if self.active_animation is not None:
            self.after_cancel(self.active_animation)
            self.active_animation = None

    def _stop_pulse(self):
        if self.pulse_job is not None:
            self.after_cancel(self.pulse_job)
            self.pulse_job = None

    def _on_canvas_resize(self, event):
        self._switch_tab_view(self.current_tab)

    def _inc_ops(self):
        self.op_counter += 1

    # ==========================================================================
    # CANVAS DRAWING UTILITIES
    # ==========================================================================
    def _draw_grid_bg(self):
        """Subtle dot-grid background for the engine canvas."""
        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 540
        spacing = 28
        for x in range(0, w + spacing, spacing):
            for y in range(0, h + spacing, spacing):
                self.canvas.create_oval(x - 1, y - 1, x + 1, y + 1,
                                        fill=GRID_DOT, outline="")

    def _draw_glow(self, x, y, radius, color, rings=3):
        """Draw concentric glow rings around a point."""
        for i in range(rings, 0, -1):
            r = radius + i * 6
            w = max(0.4, 1.8 / i)
            self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                    outline=color, width=w)

    def _draw_shockwaves(self, coords, shockwaves):
        """Draw expanding ripple shockwaves around targeted nodes."""
        if not shockwaves:
            return
        for target, wave_t, wave_col in shockwaves:
            pos = None
            if isinstance(target, str):
                pos = coords.get(target)
            elif isinstance(target, int):
                if isinstance(coords, list) and 0 <= target < len(coords):
                    pos = coords[target]
                elif isinstance(coords, dict):
                    pos = coords.get(target)
            elif isinstance(target, (tuple, list)) and len(target) == 2:
                pos = target
            elif isinstance(coords, dict):
                pos = coords.get(target)

            if not pos:
                continue
            x, y = pos
            r = 24 + wave_t * 54
            w_line = max(1, int(3.5 * (1.0 - wave_t)))
            alpha_col = lerp_color(wave_col, ENGINE_BG, min(1.0, wave_t * 0.85))
            self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                    outline=alpha_col, width=w_line)

    def _draw_particle(self, x, y, radius, color, halo=True):
        """Draw a luminous particle dot with optional glowing halo."""
        if halo:
            self.canvas.create_oval(x - radius * 2.2, y - radius * 2.2,
                                    x + radius * 2.2, y + radius * 2.2,
                                    fill="", outline=color, width=1.0)
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                fill=color, outline="#FFFFFF", width=1.0)

    def _draw_floating_badge(self, x, y, text, bg_col, fg_col="#FFFFFF", border_col=None):
        """Draw an informative floating badge / tag."""
        border = border_col or bg_col
        bw = len(text) * 7 + 16
        bh = 22
        x1, y1 = x - bw / 2, y - bh / 2
        x2, y2 = x + bw / 2, y + bh / 2
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_col, outline=border, width=1.5)
        self.canvas.create_text(x, y, text=text, fill=fg_col, font=("Consolas", 8, "bold"))

    def _draw_legend(self, items):
        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 540
        box_w, item_h = 270, 20
        box_h = len(items) * item_h + 18
        bx = w - box_w - 14
        by = h - box_h - 14
        # background
        self.canvas.create_rectangle(bx, by, bx + box_w, by + box_h,
                                     fill=ENGINE_CARD, outline=ENGINE_BORDER, width=1)
        for i, (color, label) in enumerate(items):
            iy = by + 12 + i * item_h
            self.canvas.create_oval(bx + 12, iy - 4, bx + 20, iy + 4,
                                    fill=color, outline=color)
            self.canvas.create_text(bx + 28, iy, text=label, fill=TEXT_BRIGHT,
                                    font=("Segoe UI", 8), anchor="w")

    # ==========================================================================
    # 1. NETWORK TAB — BUILD & LOGIC
    # ==========================================================================
    def _build_network_tab(self):
        parent = self.tab_network

        # Scrollable card
        card = tk.Frame(parent, bg=LI_CARD_BG, relief=tk.SOLID, bd=1)
        card.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # Title
        tk.Label(card, text="Manage Network & Mutual Connections",
                 bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(10, 2))
        tk.Label(card, text="Explore connections, add/remove members, and discover mutuals.",
                 bg=LI_CARD_BG, fg=LI_TEXT_MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=14, pady=(0, 8))

        # ---- Add User / Add Connection Section ----
        modify_box = tk.LabelFrame(card, text=" ✚ Add User / Connection ",
                                   bg=LI_CARD_BG, fg=LI_BLUE,
                                   font=("Segoe UI", 9, "bold"), padx=10, pady=6)
        modify_box.pack(fill=tk.X, padx=14, pady=4)

        # Add user row
        add_user_row = tk.Frame(modify_box, bg=LI_CARD_BG)
        add_user_row.pack(fill=tk.X, pady=3)
        tk.Label(add_user_row, text="New User:", bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                 width=10, anchor="w", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.new_user_entry = ttk.Entry(add_user_row, width=18)
        self.new_user_entry.pack(side=tk.LEFT, padx=(0, 4))
        self.new_role_entry = ttk.Entry(add_user_row, width=14)
        self.new_role_entry.pack(side=tk.LEFT, padx=(0, 4))
        self.new_role_entry.insert(0, "AI Researcher")
        ttk.Button(add_user_row, text="➕ Add", style="Success.TButton",
                   command=self.on_add_user).pack(side=tk.LEFT, padx=2)

        # Add connection row
        conn_row = tk.Frame(modify_box, bg=LI_CARD_BG)
        conn_row.pack(fill=tk.X, pady=3)
        tk.Label(conn_row, text="Connect:", bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                 width=10, anchor="w", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.conn_user_a = ttk.Combobox(conn_row, values=self.graph_engine.get_users(),
                                        state="readonly", width=14)
        self.conn_user_a.pack(side=tk.LEFT, padx=(0, 2))
        tk.Label(conn_row, text="↔", bg=LI_CARD_BG, fg=LI_BLUE,
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=2)
        self.conn_user_b = ttk.Combobox(conn_row, values=self.graph_engine.get_users(),
                                        state="readonly", width=14)
        self.conn_user_b.pack(side=tk.LEFT, padx=(2, 4))
        ttk.Button(conn_row, text="🔗 Link", style="Primary.TButton",
                   command=self.on_add_connection).pack(side=tk.LEFT, padx=2)
        ttk.Button(conn_row, text="✂ Unlink", style="Danger.TButton",
                   command=self.on_remove_connection).pack(side=tk.LEFT, padx=2)

        # ---- Inspect Mutuals Section ----
        select_box = tk.LabelFrame(card, text=" 🔍 Inspect Mutual Connections ",
                                   bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                                   font=("Segoe UI", 9, "bold"), padx=10, pady=8)
        select_box.pack(fill=tk.X, padx=14, pady=4)

        row_a = tk.Frame(select_box, bg=LI_CARD_BG)
        row_a.pack(fill=tk.X, pady=3)
        tk.Label(row_a, text="Member A:", bg=LI_CARD_BG, fg=LI_TEXT_MAIN, width=12,
                 anchor="w", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.combo_user_a = ttk.Combobox(row_a, values=self.graph_engine.get_users(),
                                         state="readonly", width=28)
        self.combo_user_a.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.combo_user_a.set("Satya Nadella")

        row_b = tk.Frame(select_box, bg=LI_CARD_BG)
        row_b.pack(fill=tk.X, pady=3)
        tk.Label(row_b, text="Member B:", bg=LI_CARD_BG, fg=LI_TEXT_MAIN, width=12,
                 anchor="w", font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.combo_user_b = ttk.Combobox(row_b, values=self.graph_engine.get_users(),
                                         state="readonly", width=28)
        self.combo_user_b.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.combo_user_b.set("Demis Hassabis")

        btn_check = ttk.Button(select_box, text="🔍 Check Mutual Connections",
                               style="Primary.TButton", command=self.on_check_mutuals)
        btn_check.pack(fill=tk.X, pady=(6, 2))

        # Quick pairs
        quick = tk.Frame(card, bg=LI_CARD_BG)
        quick.pack(fill=tk.X, padx=14, pady=2)
        tk.Label(quick, text="Quick Pairs:", bg=LI_CARD_BG, fg=LI_TEXT_MUTED,
                 font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=(0, 4))
        for u1, u2 in [("Satya Nadella", "Demis Hassabis"),
                       ("Sundar Pichai", "Sam Altman"),
                       ("Geoffrey Hinton", "Yann LeCun")]:
            lbl = f"{u1.split()[0]} & {u2.split()[0]}"
            ttk.Button(quick, text=lbl, style="Secondary.TButton",
                       command=lambda a=u1, b=u2: self._quick_pair(a, b)).pack(side=tk.LEFT, padx=2)

        # Results
        res_box = tk.LabelFrame(card, text=" Mutual Connection Results ",
                                bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                                font=("Segoe UI", 9, "bold"), padx=10, pady=6)
        res_box.pack(fill=tk.BOTH, expand=True, padx=14, pady=4)

        self.mutual_result_lbl = tk.Label(res_box,
                                          text="Select members above and click 'Check Mutual Connections'.",
                                          bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                                          font=("Segoe UI", 9), justify=tk.LEFT, wraplength=500)
        self.mutual_result_lbl.pack(anchor="w", pady=2)

        self.mutual_tags_frame = tk.Frame(res_box, bg=LI_CARD_BG)
        self.mutual_tags_frame.pack(fill=tk.X, pady=4)

        # DSA box
        dsa = tk.Frame(card, bg=LI_SECTION_BG, relief=tk.SOLID, bd=1)
        dsa.pack(fill=tk.X, padx=14, pady=(2, 8))
        tk.Label(dsa, text="⚙️  Adjacency List with Hash Sets",
                 bg=LI_SECTION_BG, fg=LI_BLUE,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=8, pady=(4, 1))
        tk.Label(dsa,
                 text="• dict[str, set[str]] → O(1) neighbor lookup\n"
                      "• Mutual: set intersection adj[A] & adj[B]\n"
                      "• Time: O(min(deg(A), deg(B)))  |  Space: O(V + E)",
                 bg=LI_SECTION_BG, fg=LI_TEXT_MUTED,
                 font=("Segoe UI", 8), justify=tk.LEFT).pack(anchor="w", padx=8, pady=(0, 4))

    # ---- Network callbacks ---------------------------------------------------
    def _refresh_user_combos(self):
        users = self.graph_engine.get_users()
        for combo in [self.combo_user_a, self.combo_user_b, self.conn_user_a, self.conn_user_b]:
            combo["values"] = users

    def on_add_user(self):
        name = self.new_user_entry.get().strip()
        role = self.new_role_entry.get().strip() or "LinkedIn Member"
        if not name:
            messagebox.showwarning("Input Required", "Please enter a user name.")
            return
        if self.graph_engine.add_user(name, role):
            self._inc_ops()
            self._refresh_user_combos()
            self.new_user_entry.delete(0, tk.END)
            self.status_lbl.config(text=f"▶  Added user '{name}' ({role}). V={len(self.graph_engine.adj)}")
            self.animate_node_spawn(name)
        else:
            messagebox.showinfo("Duplicate", f"'{name}' already exists in the graph.")

    def on_add_connection(self):
        u = self.conn_user_a.get()
        v = self.conn_user_b.get()
        if not u or not v:
            messagebox.showwarning("Select Users", "Pick two users to connect.")
            return
        if u == v:
            messagebox.showinfo("Self-Loop", "Cannot connect a user to themselves.")
            return
        if self.graph_engine.add_connection(u, v):
            self._inc_ops()
            self.status_lbl.config(
                text=f"▶  Connected '{u.split()[0]}' ↔ '{v.split()[0]}'. E={self.graph_engine.edge_count()}")
            self.animate_edge_link(u, v)
        else:
            messagebox.showinfo("Exists", "Connection already exists or users not found.")

    def on_remove_connection(self):
        u = self.conn_user_a.get()
        v = self.conn_user_b.get()
        if not u or not v:
            messagebox.showwarning("Select Users", "Pick two users to disconnect.")
            return
        if self.graph_engine.remove_connection(u, v):
            self._inc_ops()
            self.status_lbl.config(
                text=f"▶  Removed edge '{u.split()[0]}' ✂ '{v.split()[0]}'. E={self.graph_engine.edge_count()}")
            self.animate_edge_unlink(u, v)
        else:
            messagebox.showinfo("Not Found", "No connection exists between these users.")

    def _quick_pair(self, a, b):
        self.combo_user_a.set(a)
        self.combo_user_b.set(b)
        self.on_check_mutuals()

    def on_check_mutuals(self):
        u1, u2 = self.combo_user_a.get(), self.combo_user_b.get()
        if not u1 or not u2:
            messagebox.showwarning("Selection Required", "Pick both Member A and Member B.")
            return
        for w in self.mutual_tags_frame.winfo_children():
            w.destroy()
        if u1 == u2:
            self.mutual_result_lbl.config(text=f"A and B are identical ({u1}). Pick two distinct members.")
            self.cancel_active_animation()
            self._stop_pulse()
            self.draw_graph(selected_a=u1, selected_b=u2, mutuals=set())
            return
        self._inc_ops()
        mutuals = self.graph_engine.get_mutual_connections(u1, u2)
        if mutuals:
            self.mutual_result_lbl.config(
                text=f"Found {len(mutuals)} mutual connection(s) between {u1} and {u2}:")
            for m in sorted(mutuals):
                pill = tk.Label(self.mutual_tags_frame, text=f" 🤝 {m} ",
                                bg="#DCFCE7", fg="#166534",
                                font=("Segoe UI", 8, "bold"),
                                padx=6, pady=2, relief=tk.SOLID, bd=1)
                pill.pack(side=tk.LEFT, padx=3, pady=2)
            self.status_lbl.config(
                text=f"▶  Intersection: {len(mutuals)} mutual(s) — {', '.join(sorted(mutuals))}")
        else:
            self.mutual_result_lbl.config(
                text=f"No mutual connections between {u1} and {u2} (disjoint neighbor sets).")
            self.status_lbl.config(text="▶  Intersection → ∅  (0 mutuals)")

        self.animate_mutual_discovery(u1, u2, mutuals)

    # ---- Graph Animations ---------------------------------------------------
    def animate_mutual_discovery(self, u1, u2, mutuals):
        """Cinematic multi-stage traversal & set-intersection animation."""
        self.cancel_active_animation()
        self._stop_pulse()
        self.last_mutual_data = (u1, u2, mutuals)

        adj_a = self.graph_engine.adj.get(u1, set())
        adj_b = self.graph_engine.adj.get(u2, set())
        mutual_set = set(mutuals)

        # ----------------------------------------------------------------------
        # Phase 1: Focusing Selected Members A & B (Expanding Scanner Radar Waves)
        # ----------------------------------------------------------------------
        P1_FRAMES = 20

        def phase1(f):
            if self.current_tab != "network":
                return
            t = f / P1_FRAMES
            eased_t = ease_out_quart(t)
            waves = [
                (u1, eased_t, COLOR_BLUE),
                (u2, eased_t, COLOR_CYAN)
            ]
            scale = 1.0 + 0.32 * math.sin(t * math.pi)
            scales = {u1: scale, u2: scale}
            self.status_lbl.config(
                text=f"⚡ [Phase 1/3] Focusing Member A ('{u1.split()[0]}') & Member B ('{u2.split()[0]}') — Initializing Search...")
            banner = f"SCANNING: Querying Neighbors of '{u1.split()[0]}' and '{u2.split()[0]}'"
            self.draw_graph(selected_a=u1, selected_b=u2, mutuals=set(),
                            shockwaves=waves, node_scales=scales,
                            shared_edge_progress=0.0,
                            banner_text=banner)
            if f < P1_FRAMES:
                self.active_animation = self.after(28, lambda: phase1(f + 1))
            else:
                self.active_animation = self.after(50, lambda: phase2(0))

        # ----------------------------------------------------------------------
        # Phase 2: Electric Signals Traveling Outward along Neighbor Edges
        # ----------------------------------------------------------------------
        P2_FRAMES = 26

        def phase2(f):
            if self.current_tab != "network":
                return
            t = f / P2_FRAMES
            eased_t = ease_in_out_cubic(t)

            pulses = []
            for v in adj_a:
                pulses.append((u1, v, eased_t, COLOR_CYAN))
            for w in adj_b:
                pulses.append((u2, w, eased_t, COLOR_BLUE))

            scan_tint = {}
            if t > 0.3:
                strength = (t - 0.3) / 0.7
                for nb in adj_a | adj_b:
                    if nb not in (u1, u2):
                        if nb in mutual_set and t > 0.6:
                            scan_tint[nb] = lerp_color(ENGINE_CARD, "#065F46", strength)
                        else:
                            scan_tint[nb] = lerp_color(ENGINE_CARD, "#1E3A8A", strength * 0.7)

            # When signals reach halfway/destination, show collision sparks
            sparks = []
            if t > 0.65:
                spark_prog = (t - 0.65) / 0.35
                for m in mutual_set:
                    sparks.append((m, spark_prog, COLOR_GREEN))

            self.status_lbl.config(
                text=f"⚡ [Phase 2/3] Traversing Adjacency Sets: |adj[{u1.split()[0]}]|={len(adj_a)}, |adj[{u2.split()[0]}]|={len(adj_b)}...")
            banner = f"SEARCHING: Comparing Edge Sets (adj[{u1.split()[0]}] ∩ adj[{u2.split()[0]}])"
            self.draw_graph(selected_a=u1, selected_b=u2, mutuals=set(),
                            active_pulses=pulses, highlight_tint=scan_tint,
                            shockwaves=sparks,
                            shared_edge_progress=0.0,
                            banner_text=banner)
            if f < P2_FRAMES:
                self.active_animation = self.after(28, lambda: phase2(f + 1))
            else:
                self.active_animation = self.after(60, lambda: phase3(0))

        # ----------------------------------------------------------------------
        # Phase 3: Golden Bridge Laser Edges Unfurl & Celebrate Mutuals
        # ----------------------------------------------------------------------
        P3_FRAMES = 30

        def phase3(f):
            if self.current_tab != "network":
                return
            t = f / P3_FRAMES
            eased_t = ease_out_quart(t)

            waves = []
            scales = {u1: 1.0, u2: 1.0}
            if mutual_set:
                for m in mutual_set:
                    wave_prog = (t * 1.5) % 1.0
                    waves.append((m, wave_prog, COLOR_GREEN))
                    scales[m] = 1.0 + 0.38 * (1.0 - eased_t)
                banner = f"✓ MUTUAL DISCOVERY: Found {len(mutual_set)} Mutual(s) in O(min(deg(A), deg(B)))!"
                self.status_lbl.config(
                    text=f"✓ [Phase 3/3] Found {len(mutual_set)} mutual connection(s): {', '.join(sorted(mutual_set))}")
            else:
                waves.append((u1, t, COLOR_RED))
                waves.append((u2, t, COLOR_RED))
                banner = f"EMPTY SET: adj[{u1.split()[0]}] ∩ adj[{u2.split()[0]}] = ∅ (0 Mutuals)"
                self.status_lbl.config(
                    text=f"▶  Intersection → ∅ (Disjoint neighbor sets between '{u1.split()[0]}' and '{u2.split()[0]}').")

            self.draw_graph(selected_a=u1, selected_b=u2, mutuals=mutual_set,
                            shockwaves=waves, node_scales=scales,
                            shared_edge_progress=eased_t,
                            revealed_mutuals=mutual_set if t > 0.1 else set(),
                            banner_text=banner)

            if f < P3_FRAMES:
                self.active_animation = self.after(28, lambda: phase3(f + 1))
            else:
                self._start_graph_pulse(u1, u2, mutual_set)

        phase1(0)

    def _start_graph_pulse(self, u1, u2, mutuals):
        """Ambient breathing pulse loop for active mutual discovery state."""
        self._stop_pulse()
        if self.current_tab != "network":
            return

        def pulse():
            if self.current_tab != "network" or self.last_mutual_data != (u1, u2, mutuals):
                return
            self.pulse_tick += 1
            t_wave = (math.sin(self.pulse_tick * 0.12) + 1.0) / 2.0

            scales = {}
            for m in mutuals:
                scales[m] = 1.0 + 0.10 * t_wave
            scales[u1] = 1.0 + 0.06 * math.cos(self.pulse_tick * 0.12)
            scales[u2] = 1.0 + 0.06 * math.cos(self.pulse_tick * 0.12)

            self.draw_graph(selected_a=u1, selected_b=u2, mutuals=mutuals,
                            node_scales=scales, shared_edge_progress=1.0,
                            pulse_offset=self.pulse_tick * 3)
            self.pulse_job = self.after(45, pulse)

        pulse()

    def animate_node_spawn(self, user):
        """Animated pop-in scale & burst when a new user is added."""
        self.cancel_active_animation()
        self._stop_pulse()
        FRAMES = 14

        def step(f):
            if self.current_tab != "network":
                return
            t = f / FRAMES
            scale = ease_out_back(t)
            waves = [(user, t, COLOR_CYAN)]
            scales = {user: scale}
            self.draw_graph(shockwaves=waves, node_scales=scales)
            if f < FRAMES:
                self.active_animation = self.after(22, lambda: step(f + 1))
            else:
                self.draw_graph()

        step(0)

    def animate_edge_link(self, u, v):
        """Animated laser beam shooting between nodes on connection."""
        self.cancel_active_animation()
        self._stop_pulse()
        FRAMES = 16

        def step(f):
            if self.current_tab != "network":
                return
            t = ease_out_quart(f / FRAMES)
            pulses = [(u, v, t, COLOR_CYAN), (v, u, t, COLOR_BLUE)]
            waves = [(u, t, COLOR_BLUE), (v, t, COLOR_BLUE)] if f == FRAMES - 1 else []
            self.draw_graph(active_pulses=pulses, shockwaves=waves)
            if f < FRAMES:
                self.active_animation = self.after(22, lambda: step(f + 1))
            else:
                self.draw_graph()

        step(0)

    def animate_edge_unlink(self, u, v):
        """Animated red disconnect ripple on unlinking an edge."""
        self.cancel_active_animation()
        self._stop_pulse()
        FRAMES = 12

        def step(f):
            if self.current_tab != "network":
                return
            t = f / FRAMES
            waves = [(u, t, COLOR_RED), (v, t, COLOR_RED)]
            self.draw_graph(shockwaves=waves)
            if f < FRAMES:
                self.active_animation = self.after(22, lambda: step(f + 1))
            else:
                self.draw_graph()

        step(0)

    # ---- Graph Drawing -------------------------------------------------------
    def draw_graph(self, selected_a=None, selected_b=None, mutuals=None,
                   active_pulses=None, shockwaves=None, node_scales=None,
                   shared_edge_progress=1.0, revealed_mutuals=None,
                   highlight_tint=None, pulse_offset=0, banner_text=None):
        if self.current_tab != "network":
            return
        mutuals = mutuals or set()
        active_mutuals = revealed_mutuals if revealed_mutuals is not None else mutuals
        node_scales = node_scales or {}
        highlight_tint = highlight_tint or {}

        self.canvas.delete("all")
        self._draw_grid_bg()

        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 540

        users = self.graph_engine.get_users()
        n = len(users)
        if n == 0:
            self.canvas.create_text(w / 2, h / 2, text="[ Graph is empty — add users above ]",
                                    fill=TEXT_DIM, font=("Segoe UI", 12))
            return

        cx, cy = w / 2, h / 2
        rx = min(w * 0.38, 250)
        ry = min(h * 0.38, 200)

        coords = {}
        for i, user in enumerate(users):
            angle = 2 * math.pi * i / n - math.pi / 2
            coords[user] = (cx + rx * math.cos(angle), cy + ry * math.sin(angle))

        # Base Edges
        drawn = set()
        for u in users:
            for v in self.graph_engine.adj.get(u, set()):
                key = tuple(sorted([u, v]))
                if key in drawn:
                    continue
                drawn.add(key)
                if u not in coords or v not in coords:
                    continue
                x1, y1 = coords[u]
                x2, y2 = coords[v]

                is_shared = False
                if selected_a and selected_b and active_mutuals:
                    if ((u == selected_a or u == selected_b) and v in active_mutuals) or \
                       ((v == selected_a or v == selected_b) and u in active_mutuals):
                        is_shared = True
                is_direct = (selected_a and selected_b and
                             key == tuple(sorted([selected_a, selected_b])))

                if is_shared:
                    # Shared edge will be drawn on the overlay pass for clean glow
                    pass
                elif is_direct:
                    self.canvas.create_line(x1, y1, x2, y2, fill=COLOR_BLUE, width=2.5, dash=(6, 3))
                else:
                    dim = "#1E293B" if (selected_a and selected_b) else "#334155"
                    self.canvas.create_line(x1, y1, x2, y2, fill=dim, width=1.5)

        # Active Signal Pulses Traveling along Edges
        if active_pulses:
            for from_u, to_u, prog, p_col in active_pulses:
                if from_u in coords and to_u in coords:
                    x1, y1 = coords[from_u]
                    x2, y2 = coords[to_u]
                    px = lerp(x1, x2, prog)
                    py = lerp(y1, y2, prog)
                    # Luminous laser beam
                    self.canvas.create_line(x1, y1, px, py, fill=p_col, width=3.0)
                    # Leading glowing particle head with halo
                    self._draw_particle(px, py, 5.0, p_col, halo=True)

        # Overlay: Shared Golden Laser Edges with unfurling progress & spark
        if selected_a and selected_b and active_mutuals and shared_edge_progress > 0:
            for m in active_mutuals:
                for src in (selected_a, selected_b):
                    if src in coords and m in coords and self.graph_engine.has_connection(src, m):
                        x1, y1 = coords[src]
                        x2, y2 = coords[m]
                        ex = lerp(x1, x2, shared_edge_progress)
                        ey = lerp(y1, y2, shared_edge_progress)
                        # Outer wide glow line
                        self.canvas.create_line(x1, y1, ex, ey, fill=GLOW_YELLOW, width=8.0)
                        # Core bright golden laser line
                        self.canvas.create_line(x1, y1, ex, ey, fill=COLOR_YELLOW, width=3.5)
                        # Spark particle at leading edge or shimmering
                        if shared_edge_progress < 1.0:
                            self._draw_particle(ex, ey, 6.0, "#FFFFFF", halo=True)
                        elif pulse_offset > 0:
                            spark_t = ((pulse_offset + (hash(src + m) % 50)) % 100) / 100.0
                            sx = lerp(x1, x2, spark_t)
                            sy = lerp(y1, y2, spark_t)
                            self._draw_particle(sx, sy, 4.0, "#FFFFFF", halo=True)

        # Draw Expanding Shockwaves
        self._draw_shockwaves(coords, shockwaves)

        # Draw Nodes
        base_radius = 25
        for user, (x, y) in coords.items():
            is_sel = user in (selected_a, selected_b)
            is_mut = user in active_mutuals
            sc = node_scales.get(user, 1.0)
            radius = base_radius * sc

            if is_sel:
                self._draw_glow(x, y, radius, COLOR_BLUE, 3)
                fill, outline, ow = "#0C4A6E", COLOR_BLUE, 3.5
            elif is_mut:
                self._draw_glow(x, y, radius, COLOR_GREEN, 3)
                fill, outline, ow = "#14532D", COLOR_GREEN, 3.5
                # Floating badge marking mutual connection
                self._draw_floating_badge(x, y - radius - 14, "🤝 MUTUAL", bg_col="#064E3B", fg_col=COLOR_GREEN, border_col=COLOR_GREEN)
            elif user in highlight_tint:
                fill, outline, ow = highlight_tint[user], COLOR_CYAN, 2.5
            else:
                fill, outline, ow = ENGINE_CARD, ENGINE_BORDER, 1.5

            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                    fill=fill, outline=outline, width=ow)
            initials = "".join(p[0] for p in user.split()[:2])
            fs = max(8, int(10 * sc))
            self.canvas.create_text(x, y, text=initials, fill="#FFFFFF",
                                    font=("Segoe UI", fs, "bold"))
            name_col = TEXT_BRIGHT if (is_sel or is_mut) else TEXT_DIM
            self.canvas.create_text(x, y + radius + 14, text=user,
                                    fill=name_col, font=("Segoe UI", 7, "bold"))

        # Floating Animation Banner at Canvas Top
        if banner_text:
            self._draw_floating_badge(w / 2, 28, banner_text, bg_col="#0F172A", fg_col=COLOR_CYAN, border_col=COLOR_BLUE)

        # Update HUD
        v_cnt = len(self.graph_engine.adj)
        e_cnt = self.graph_engine.edge_count()
        self.hud_stats_lbl.config(text=f"V={v_cnt} | E={e_cnt} | ops={self.op_counter}")

        self._draw_legend([
            (COLOR_BLUE,   "Selected Members (A & B)"),
            (COLOR_GREEN,  "Mutual Connection(s)"),
            (COLOR_YELLOW, "Shared Edges"),
        ])

    # ==========================================================================
    # 2. FEED TAB — BUILD & LOGIC
    # ==========================================================================
    def _build_feed_tab(self):
        parent = self.tab_feed
        card = tk.Frame(parent, bg=LI_CARD_BG, relief=tk.SOLID, bd=1)
        card.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        tk.Label(card, text="LinkedIn Feed Ranking & Priority Queue",
                 bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(10, 2))
        tk.Label(card, text="Posts ranked dynamically by engagement score using a Max-Heap.",
                 bg=LI_CARD_BG, fg=LI_TEXT_MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=14, pady=(0, 8))

        # Submit form
        form = tk.LabelFrame(card, text=" ✚ Submit New Post ",
                             bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                             font=("Segoe UI", 9, "bold"), padx=10, pady=6)
        form.pack(fill=tk.X, padx=14, pady=4)

        r1 = tk.Frame(form, bg=LI_CARD_BG); r1.pack(fill=tk.X, pady=2)
        tk.Label(r1, text="Author:", bg=LI_CARD_BG, width=10, anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.feed_author = ttk.Combobox(r1, values=[
            "Alex Morgan", "Sarah Connor", "Indrajit (Student)", "Sundar Pichai",
            "Satya Nadella", "Mira Murati"
        ], width=28)
        self.feed_author.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.feed_author.set("Alex Morgan")

        r2 = tk.Frame(form, bg=LI_CARD_BG); r2.pack(fill=tk.X, pady=2)
        tk.Label(r2, text="Content:", bg=LI_CARD_BG, width=10, anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.feed_content = ttk.Entry(r2, width=28)
        self.feed_content.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.feed_content.insert(0, "Excited to share our breakthrough in distributed graphs!")

        r3 = tk.Frame(form, bg=LI_CARD_BG); r3.pack(fill=tk.X, pady=2)
        tk.Label(r3, text="Score:", bg=LI_CARD_BG, width=10, anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.feed_score = ttk.Spinbox(r3, from_=50, to=1500, increment=25, width=10)
        self.feed_score.pack(side=tk.LEFT)
        self.feed_score.set("880")
        tk.Label(r3, text="  (Likes + Reposts)", bg=LI_CARD_BG, fg=LI_TEXT_MUTED,
                 font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=4)

        btn_row = tk.Frame(form, bg=LI_CARD_BG); btn_row.pack(fill=tk.X, pady=(4, 2))
        ttk.Button(btn_row, text="🚀 Publish & Heapify-Up", style="Primary.TButton",
                   command=self.on_publish_post).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        ttk.Button(btn_row, text="🎲 Viral Post", style="Accent.TButton",
                   command=self.on_random_post).pack(side=tk.LEFT, padx=2)

        # Serve controls
        serve = tk.LabelFrame(card, text=" Feed Engine Controls ",
                              bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                              font=("Segoe UI", 9, "bold"), padx=10, pady=6)
        serve.pack(fill=tk.X, padx=14, pady=4)

        sb = tk.Frame(serve, bg=LI_CARD_BG); sb.pack(fill=tk.X)
        ttk.Button(sb, text="⭐ Extract Top Post (Pop Max)", style="Primary.TButton",
                   command=self.on_extract_top).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))

        # Currently served
        top_card = tk.Frame(card, bg="#F0FDF4", relief=tk.SOLID, bd=1)
        top_card.pack(fill=tk.BOTH, expand=True, padx=14, pady=4)
        tk.Label(top_card, text="CURRENTLY SERVED TOP POST", bg="#F0FDF4", fg="#166534",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=8, pady=(4, 1))
        self.served_lbl = tk.Label(top_card,
                                   text="Root: Demis Hassabis | Score: 950\n"
                                        "'Excited to share our breakthrough in protein folding & AI!'",
                                   bg="#F0FDF4", fg=LI_TEXT_MAIN,
                                   font=("Segoe UI", 9), justify=tk.LEFT, wraplength=500)
        self.served_lbl.pack(anchor="w", padx=8, pady=(0, 4))

        # DSA box
        dsa = tk.Frame(card, bg=LI_SECTION_BG, relief=tk.SOLID, bd=1)
        dsa.pack(fill=tk.X, padx=14, pady=(2, 8))
        tk.Label(dsa, text="⚙️  Max-Heap Priority Queue (Complete Binary Tree)",
                 bg=LI_SECTION_BG, fg=LI_BLUE,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=8, pady=(4, 1))
        tk.Label(dsa,
                 text="• Parent(i)=(i-1)//2  Left=2i+1  Right=2i+2\n"
                      "• Heapify-Up: leaf bubbles up via O(log N) swaps\n"
                      "• Heapify-Down: root sifts down to restore invariant",
                 bg=LI_SECTION_BG, fg=LI_TEXT_MUTED,
                 font=("Segoe UI", 8), justify=tk.LEFT).pack(anchor="w", padx=8, pady=(0, 4))

    # ---- Feed callbacks ------------------------------------------------------
    def on_publish_post(self):
        author  = self.feed_author.get().strip() or "Anonymous"
        content = self.feed_content.get().strip() or "Update."
        try:
            score = int(self.feed_score.get())
        except ValueError:
            messagebox.showerror("Invalid", "Score must be an integer.")
            return
        self._inc_ops()
        post, swaps = self.feed_engine.prepare_insert(author, content, score)
        self.status_lbl.config(
            text=f"▶  New post at leaf (score={score}). Heapify-Up: {len(swaps)} swap(s)…")
        self.animate_heapify_up(post, swaps)

    def on_random_post(self):
        authors = ["Satya Nadella", "Sundar Pichai", "Sam Altman",
                    "Yann LeCun", "Demis Hassabis", "Mira Murati"]
        topics = [
            "Announcing our next-gen neural architecture!",
            "Honored to meet our brilliant engineering community.",
            "Scaling laws continue to hold with remarkable consistency.",
            "Excited to open-source our machine learning framework.",
        ]
        self.feed_author.set(random.choice(authors))
        self.feed_content.delete(0, tk.END)
        self.feed_content.insert(0, random.choice(topics))
        self.feed_score.set(str(random.randint(200, 1200)))
        self.on_publish_post()

    def on_extract_top(self):
        top, swaps = self.feed_engine.prepare_extract()
        if not top:
            messagebox.showinfo("Empty", "Feed priority queue is empty.")
            return
        self._inc_ops()
        new_top = self.feed_engine.tree_nodes[0] if self.feed_engine.tree_nodes else None
        if new_top:
            self.served_lbl.config(
                text=f"Popped: {top.author} (Score: {top.score})\n"
                     f"New Root: {new_top.author} (Score: {new_top.score})")
        else:
            self.served_lbl.config(text=f"Popped: {top.author} (Score: {top.score})\nFeed now empty.")
        self.status_lbl.config(
            text=f"▶  Extracted max: {top.author} (score={top.score}). Heapify-down: {len(swaps)} swap(s)…")
        self.animate_heapify_down(top, swaps)

    # ---- Heap Drawing --------------------------------------------------------
    def _heap_positions(self, n, w, h):
        if n == 0:
            return []
        d_max = math.floor(math.log2(n)) if n > 0 else 0
        v_gap = min(80, (h - 110) / (d_max + 1.5))
        positions = []
        for i in range(n):
            depth = math.floor(math.log2(i + 1))
            level_idx = i - ((1 << depth) - 1)
            num_in_lvl = 1 << depth
            slot_w = w / num_in_lvl
            x = (level_idx + 0.5) * slot_w
            y = 60 + depth * v_gap
            positions.append((x, y))
        return positions

    def draw_heap_tree(self, highlight_idx=None, highlight_color=COLOR_PURPLE,
                       swap_pair=None, t_anim=1.0, arc_dir=1,
                       comparison_pair=None, popped_post=None,
                       popped_y_offset=0, popped_alpha=1.0,
                       node_scales=None, shockwaves=None, banner_text=None):
        if self.current_tab != "feed":
            return
        self.canvas.delete("all")
        self._draw_grid_bg()

        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 540
        nodes = self.feed_engine.tree_nodes
        n = len(nodes)
        node_scales = node_scales or {}

        # Update HUD
        self.hud_stats_lbl.config(
            text=f"N={n} | depth={self.feed_engine.depth()} | ops={self.op_counter}")

        if n == 0 and not popped_post:
            self.canvas.create_text(w / 2, h / 2, text="[ Feed Priority Queue is Empty ]",
                                    fill=TEXT_DIM, font=("Segoe UI", 12))
            return

        pos = self._heap_positions(n, w, h)
        radius = 24

        # Edges between parent and children
        for i in range(1, n):
            parent = (i - 1) // 2
            px, py = pos[parent]
            cx, cy = pos[i]
            is_comp = comparison_pair and ((parent, i) == comparison_pair or (i, parent) == comparison_pair)
            if is_comp:
                self.canvas.create_line(px, py, cx, cy, fill=COLOR_YELLOW, width=3.5)
            else:
                self.canvas.create_line(px, py, cx, cy, fill="#334155", width=2)

        # Dissolving / Floating Popped Post (Extract Root Animation)
        if popped_post and pos:
            rx, ry = pos[0][0], pos[0][1] - popped_y_offset
            r_col = lerp_color(COLOR_YELLOW, ENGINE_BG, 1.0 - popped_alpha)
            self._draw_glow(rx, ry, radius, r_col, 3)
            self.canvas.create_oval(rx - radius, ry - radius, rx + radius, ry + radius,
                                    fill="#78350F", outline=r_col, width=3.0)
            self.canvas.create_text(rx, ry, text=str(popped_post.score), fill="#FFFFFF",
                                    font=("Consolas", 10, "bold"))
            self.canvas.create_text(rx, ry - radius - 10, text="⭐ POPPED MAX ROOT",
                                    fill=COLOR_YELLOW, font=("Segoe UI", 8, "bold"))

        # Comparison Beam Indicator
        if comparison_pair and len(pos) > max(comparison_pair):
            p1, p2 = pos[comparison_pair[0]], pos[comparison_pair[1]]
            mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=COLOR_YELLOW, width=3, dash=(4, 2))
            self._draw_floating_badge(mx, my - 14, "COMPARE", bg_col="#854D0E", fg_col=COLOR_YELLOW)

        # Draw Expanding Shockwaves
        self._draw_shockwaves(pos, shockwaves)

        # Draw Nodes
        for i, post in enumerate(nodes):
            x, y = pos[i]

            # Orbital Arced Trajectory during Swaps
            if swap_pair and (i == swap_pair[0] or i == swap_pair[1]):
                a_idx, b_idx = swap_pair
                ax, ay = pos[a_idx]
                bx, by = pos[b_idx]
                t = ease_in_out_cubic(t_anim)
                dx, dy = bx - ax, by - ay
                dist = math.hypot(dx, dy) or 1.0
                nx, ny = -dy / dist, dx / dist
                arc_h = min(40, dist * 0.35) * math.sin(t * math.pi) * arc_dir

                if i == a_idx:
                    x = lerp(ax, bx, t) + nx * arc_h
                    y = lerp(ay, by, t) + ny * arc_h
                else:
                    x = lerp(bx, ax, t) - nx * arc_h
                    y = lerp(by, ay, t) - ny * arc_h

                # Motion blur trailing ghost
                for trail_t in (0.3, 0.6):
                    sub_t = max(0.0, t - trail_t * 0.25)
                    sub_arch = min(40, dist * 0.35) * math.sin(sub_t * math.pi) * arc_dir
                    if i == a_idx:
                        tx = lerp(ax, bx, sub_t) + nx * sub_arch
                        ty = lerp(ay, by, sub_t) + ny * sub_arch
                    else:
                        tx = lerp(bx, ax, sub_t) - nx * sub_arch
                        ty = lerp(by, ay, sub_t) - ny * sub_arch
                    tr_r = radius * 0.75
                    self.canvas.create_oval(tx - tr_r, ty - tr_r, tx + tr_r, ty + tr_r,
                                            fill="", outline=COLOR_YELLOW, width=1.0)

            sc = node_scales.get(i, 1.0)
            r = radius * sc
            is_swapping = swap_pair and (i in swap_pair)

            if is_swapping:
                self._draw_glow(x, y, r, COLOR_YELLOW, 3)
                fill, outline, ow = "#7C2D12", COLOR_YELLOW, 3.0
            elif i == highlight_idx:
                self._draw_glow(x, y, r, highlight_color, 3)
                fill = "#3B0764" if highlight_color == COLOR_PURPLE else "#14532D"
                outline, ow = highlight_color, 3.0
            elif i == 0:
                self._draw_glow(x, y, r, COLOR_GREEN, 2)
                fill, outline, ow = "#1E293B", COLOR_GREEN, 2.5
            else:
                fill, outline, ow = ENGINE_CARD, ENGINE_BORDER, 1.5

            self.canvas.create_oval(x - r, y - r, x + r, y + r,
                                    fill=fill, outline=outline, width=ow)
            self.canvas.create_text(x, y, text=str(post.score), fill="#FFFFFF",
                                    font=("Consolas", max(8, int(10 * sc)), "bold"))
            self.canvas.create_text(x, y + r + 12, text=post.author.split()[0],
                                    fill=TEXT_BRIGHT, font=("Segoe UI", 7))

        if banner_text:
            self._draw_floating_badge(w / 2, 28, banner_text, bg_col="#1E293B", fg_col=COLOR_CYAN)

        self._draw_legend([
            (COLOR_GREEN,  "Root (Max Score Post)"),
            (COLOR_YELLOW, "Heapify Swapping Nodes"),
            (COLOR_PURPLE, "Newly Inserted (Leaf)"),
        ])

    # ---- Heap Animations (Orbital Arcs, Pop-in & Comparisons) ----------------
    def animate_heapify_up(self, post, swaps):
        """Cinematic 3-phase heapify-up: leaf spawn, comparison, and arced swaps."""
        self.cancel_active_animation()
        self._stop_pulse()
        leaf = len(self.feed_engine.tree_nodes) - 1

        # Phase 1: Leaf Pop-in Scale & Double Shockwave
        SPAWN_FRAMES = 18

        def spawn_step(f):
            if self.current_tab != "feed":
                return
            t = f / SPAWN_FRAMES
            scale = ease_out_back(t)
            waves = [(leaf, t, COLOR_PURPLE)]
            scales = {leaf: scale}
            self.draw_heap_tree(highlight_idx=leaf, highlight_color=COLOR_PURPLE,
                                node_scales=scales, shockwaves=waves,
                                banner_text=f"NEW POST ADDED: Author '{post.author.split()[0]}' (Score: {post.score}) enters bottom leaf")
            if f < SPAWN_FRAMES:
                self.active_animation = self.after(26, lambda: spawn_step(f + 1))
            else:
                if not swaps:
                    self.status_lbl.config(text=f"▶  Heapify-Up done. Node at index {leaf} satisfies max-heap invariant.")
                    self._start_feed_pulse()
                    return
                self.active_animation = self.after(45, lambda: run_compare(0))

        # Phase 2: Sequential Comparisons and Arced Orbital Swaps
        def run_compare(si):
            if si >= len(swaps):
                final = swaps[-1][1]
                waves = [(final, 0.5, COLOR_GREEN)]
                self.draw_heap_tree(highlight_idx=final, highlight_color=COLOR_GREEN,
                                    shockwaves=waves, banner_text="✓ MAX-HEAP INVARIANT RESTORED (Child <= Parent)")
                self.status_lbl.config(text=f"▶  Heapify-Up settled at index {final}. Heap restored.")
                self._start_feed_pulse()
                return

            c_idx, p_idx = swaps[si]
            COMPARE_FRAMES = 15

            def comp_step(cf):
                if self.current_tab != "feed":
                    return
                c_post = self.feed_engine.tree_nodes[c_idx]
                p_post = self.feed_engine.tree_nodes[p_idx]
                banner = f"⚡ COMPARISON: Child score ({c_post.score}) > Parent score ({p_post.score}) → SWAP REQUIRED!"
                self.status_lbl.config(
                    text=f"⚡ Invariant Check: Child score ({c_post.score}) > Parent score ({p_post.score}) → Performing Heapify-Up Swap!")
                self.draw_heap_tree(comparison_pair=(c_idx, p_idx),
                                    highlight_idx=c_idx, highlight_color=COLOR_YELLOW,
                                    banner_text=banner)
                if cf < COMPARE_FRAMES:
                    self.active_animation = self.after(28, lambda: comp_step(cf + 1))
                else:
                    self.active_animation = self.after(30, lambda: run_swap_orbit(si, 0))

            comp_step(0)

        def run_swap_orbit(si, f):
            if self.current_tab != "feed":
                return
            c_idx, p_idx = swaps[si]
            SWAP_FRAMES = 22
            t = f / SWAP_FRAMES
            banner = f"SWAPPING: Sifting node up from index {c_idx} ➔ {p_idx}"
            self.draw_heap_tree(swap_pair=(c_idx, p_idx), t_anim=t, arc_dir=1, banner_text=banner)
            if f < SWAP_FRAMES:
                self.active_animation = self.after(26, lambda: run_swap_orbit(si, f + 1))
            else:
                self.feed_engine.execute_single_swap(c_idx, p_idx)
                waves = [(p_idx, 0.4, COLOR_YELLOW)]
                self.draw_heap_tree(highlight_idx=p_idx, highlight_color=COLOR_YELLOW, shockwaves=waves)
                self.active_animation = self.after(55, lambda: run_compare(si + 1))

        spawn_step(0)

    def animate_heapify_down(self, popped, swaps):
        """Cinematic heapify-down: popped root elevates & dissolves, followed by arced sift-downs."""
        self.cancel_active_animation()
        self._stop_pulse()

        # Phase 1: Popped Root Elevation & Golden Dissipation
        POP_FRAMES = 18

        def pop_step(f):
            if self.current_tab != "feed":
                return
            t = f / POP_FRAMES
            y_off = ease_out_quart(t) * 54
            alpha = max(0.0, 1.0 - t)
            waves = [((self.canvas.winfo_width() / 2 if self.canvas.winfo_width() else 300, 60 - y_off), t, COLOR_YELLOW)]
            banner = f"⭐ POPPED MAXIMUM: Extracting top post '{popped.author}' (Score: {popped.score})"
            self.draw_heap_tree(popped_post=popped, popped_y_offset=y_off,
                                popped_alpha=alpha, shockwaves=waves,
                                banner_text=banner)
            if f < POP_FRAMES:
                self.active_animation = self.after(26, lambda: pop_step(f + 1))
            else:
                if not swaps:
                    self.draw_heap_tree(highlight_idx=0, highlight_color=COLOR_GREEN)
                    self._start_feed_pulse()
                    return
                self.active_animation = self.after(45, lambda: run_compare(0))

        # Phase 2: Comparisons and Sift-down Arced Swaps
        def run_compare(si):
            if si >= len(swaps):
                waves = [(0, 0.5, COLOR_GREEN)]
                self.draw_heap_tree(highlight_idx=0, highlight_color=COLOR_GREEN,
                                    shockwaves=waves, banner_text="✓ HEAP PROPERTY RESTORED: New Max Root Established")
                self.status_lbl.config(text="▶  Heapify-Down complete. New max root established.")
                self._start_feed_pulse()
                return

            p_idx, c_idx = swaps[si]
            COMPARE_FRAMES = 15

            def comp_step(cf):
                if self.current_tab != "feed":
                    return
                p_post = self.feed_engine.tree_nodes[p_idx]
                c_post = self.feed_engine.tree_nodes[c_idx]
                banner = f"⚡ SIFT-DOWN CHECK: Parent score ({p_post.score}) < Largest child ({c_post.score}) → SWAP!"
                self.status_lbl.config(
                    text=f"⚡ Invariant Check: Parent score ({p_post.score}) < Child score ({c_post.score}) → Sifting Down!")
                self.draw_heap_tree(comparison_pair=(p_idx, c_idx),
                                    highlight_idx=p_idx, highlight_color=COLOR_YELLOW,
                                    banner_text=banner)
                if cf < COMPARE_FRAMES:
                    self.active_animation = self.after(28, lambda: comp_step(cf + 1))
                else:
                    self.active_animation = self.after(30, lambda: run_swap_orbit(si, 0))

            comp_step(0)

        def run_swap_orbit(si, f):
            if self.current_tab != "feed":
                return
            p_idx, c_idx = swaps[si]
            SWAP_FRAMES = 22
            t = f / SWAP_FRAMES
            banner = f"SIFTING DOWN: Swapping root element with child (index {p_idx} ➔ {c_idx})"
            self.draw_heap_tree(swap_pair=(p_idx, c_idx), t_anim=t, arc_dir=-1, banner_text=banner)
            if f < SWAP_FRAMES:
                self.active_animation = self.after(26, lambda: run_swap_orbit(si, f + 1))
            else:
                self.feed_engine.execute_single_swap(p_idx, c_idx)
                waves = [(c_idx, 0.4, COLOR_YELLOW)]
                self.draw_heap_tree(highlight_idx=c_idx, highlight_color=COLOR_YELLOW, shockwaves=waves)
                self.active_animation = self.after(55, lambda: run_compare(si + 1))

        pop_step(0)

    def _start_feed_pulse(self):
        """Ambient breathing pulse on max root post."""
        self._stop_pulse()
        if self.current_tab != "feed":
            return

        def pulse():
            if self.current_tab != "feed" or not self.feed_engine.tree_nodes:
                return
            self.pulse_tick += 1
            t_wave = (math.sin(self.pulse_tick * 0.12) + 1.0) / 2.0
            scales = {0: 1.0 + 0.10 * t_wave}
            self.draw_heap_tree(node_scales=scales)
            self.pulse_job = self.after(45, pulse)

        pulse()

    # ==========================================================================
    # 3. MESSAGING TAB — BUILD & LOGIC
    # ==========================================================================
    def _build_messaging_tab(self):
        parent = self.tab_messaging
        card = tk.Frame(parent, bg=LI_CARD_BG, relief=tk.SOLID, bd=1)
        card.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        tk.Label(card, text="Direct Messaging & FIFO Transmission",
                 bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(10, 2))
        tk.Label(card, text="Messages buffered in a FIFO double-ended queue (collections.deque).",
                 bg=LI_CARD_BG, fg=LI_TEXT_MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=14, pady=(0, 8))

        # Send form
        send = tk.LabelFrame(card, text=" ✉ Send New Direct Message ",
                             bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                             font=("Segoe UI", 9, "bold"), padx=10, pady=6)
        send.pack(fill=tk.X, padx=14, pady=4)

        r1 = tk.Frame(send, bg=LI_CARD_BG); r1.pack(fill=tk.X, pady=2)
        tk.Label(r1, text="To:", bg=LI_CARD_BG, width=10, anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.msg_partner = ttk.Combobox(r1, values=[
            "Satya Nadella", "Sundar Pichai", "Sam Altman",
            "Mira Murati", "Google Recruiter"
        ], width=28)
        self.msg_partner.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.msg_partner.set("Satya Nadella")

        r2 = tk.Frame(send, bg=LI_CARD_BG); r2.pack(fill=tk.X, pady=2)
        tk.Label(r2, text="Message:", bg=LI_CARD_BG, width=10, anchor="w",
                 font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT)
        self.msg_text = ttk.Entry(r2, width=28)
        self.msg_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.msg_text.insert(0, "Hi Satya, excited about the latest Azure AI integration!")
        self.msg_text.bind("<Return>", lambda e: self.on_send_msg())

        btn_row = tk.Frame(send, bg=LI_CARD_BG); btn_row.pack(fill=tk.X, pady=(4, 2))
        ttk.Button(btn_row, text="📤 Send (Enqueue Tail)", style="Primary.TButton",
                   command=self.on_send_msg).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 4))
        ttk.Button(btn_row, text="📬 Open Chat (Dequeue Head)", style="Success.TButton",
                   command=self.on_dequeue_msg).pack(side=tk.LEFT)

        # Chat history
        chat = tk.LabelFrame(card, text=" Delivered Conversation (FIFO Processed) ",
                             bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                             font=("Segoe UI", 9, "bold"), padx=8, pady=4)
        chat.pack(fill=tk.BOTH, expand=True, padx=14, pady=4)

        self.chat_list = tk.Listbox(chat, bg="#F8FAFC", fg=LI_TEXT_MAIN,
                                    font=("Segoe UI", 9), relief=tk.FLAT)
        self.chat_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll = ttk.Scrollbar(chat, orient=tk.VERTICAL, command=self.chat_list.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_list.config(yscrollcommand=scroll.set)
        self.chat_list.insert(tk.END, "✓ [10:20:00] Indrajit: Initialized handshake with server.")

        self.queue_lbl = tk.Label(card,
                                  text=f"Pipeline Buffer: {len(self.messaging_engine.queue)} messages pending.",
                                  bg=LI_CARD_BG, fg=LI_BLUE,
                                  font=("Segoe UI", 9, "bold"))
        self.queue_lbl.pack(anchor="w", padx=14, pady=2)

        # DSA box
        dsa = tk.Frame(card, bg=LI_SECTION_BG, relief=tk.SOLID, bd=1)
        dsa.pack(fill=tk.X, padx=14, pady=(2, 8))
        tk.Label(dsa, text="⚙️  FIFO Queue (collections.deque — Doubly Linked List)",
                 bg=LI_SECTION_BG, fg=LI_BLUE,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=8, pady=(4, 1))
        tk.Label(dsa,
                 text="• Enqueue: deque.append(packet) → strict O(1) tail push\n"
                      "• Dequeue: deque.popleft() → strict O(1) head pop\n"
                      "• Guarantees in-order FIFO delivery across the pipeline",
                 bg=LI_SECTION_BG, fg=LI_TEXT_MUTED,
                 font=("Segoe UI", 8), justify=tk.LEFT).pack(anchor="w", padx=8, pady=(0, 4))

    # ---- Messaging callbacks -------------------------------------------------
    def on_send_msg(self):
        sender = self.msg_partner.get().strip() or "Member"
        text = self.msg_text.get().strip()
        if not text:
            return
        self._inc_ops()
        msg = self.messaging_engine.enqueue(sender, text)
        self.queue_lbl.config(text=f"Pipeline Buffer: {len(self.messaging_engine.queue)} messages pending.")
        self.status_lbl.config(text=f"▶  Enqueued Msg #{msg.msg_id} to tail. Sliding in…")
        self.animate_enqueue(msg)

    def on_dequeue_msg(self):
        popped = self.messaging_engine.dequeue()
        if not popped:
            messagebox.showinfo("Empty", "No messages in the FIFO pipeline.")
            return
        self._inc_ops()
        self.queue_lbl.config(text=f"Pipeline Buffer: {len(self.messaging_engine.queue)} messages pending.")
        self.chat_list.insert(tk.END, f"✓ [{popped.timestamp}] {popped.sender}: {popped.text}")
        self.chat_list.see(tk.END)
        self.status_lbl.config(text=f"▶  Dequeued Msg #{popped.msg_id} from head. Sliding out…")
        self.animate_dequeue(popped)

    # ---- Messaging Drawing ---------------------------------------------------
    def draw_messaging_pipeline(self, incoming=None, in_off=0, in_scale=1.0,
                                dequeued=None, out_off=0, out_scale=1.0,
                                queue_shift=0.0, shockwaves=None, floating_tag=None,
                                head_glow=False, new_tail_docked=False):
        if self.current_tab != "messaging":
            return
        self.canvas.delete("all")
        self._draw_grid_bg()

        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 540
        py = h / 2
        pipe_h = 120
        pipe_top, pipe_bot = py - pipe_h / 2, py + pipe_h / 2

        # Outer guide rail glow
        self.canvas.create_line(36, pipe_top - 1, w - 36, pipe_top - 1, fill="#0369A1", width=5)
        self.canvas.create_line(36, pipe_bot + 1, w - 36, pipe_bot + 1, fill="#0369A1", width=5)
        # Guide rails
        self.canvas.create_line(40, pipe_top, w - 40, pipe_top, fill="#38BDF8", width=3)
        self.canvas.create_line(40, pipe_bot, w - 40, pipe_bot, fill="#38BDF8", width=3)

        # Directional markers
        self.canvas.create_text(50, pipe_top - 18, text="◀ DEQUEUE [HEAD / EXIT]",
                                fill=COLOR_GREEN, font=("Consolas", 9, "bold"), anchor="w")
        self.canvas.create_text(w - 50, pipe_top - 18, text="[TAIL / ENQUEUE] ◀",
                                fill=COLOR_BLUE, font=("Consolas", 9, "bold"), anchor="e")

        # Dynamic Conveyor Chevrons inside pipeline
        offset = (self.pulse_tick * 4) % 80
        for ax in range(int(40 - offset), int(w + 80), 80):
            if 45 <= ax <= w - 45:
                self.canvas.create_text(ax, pipe_bot + 14, text="◀", fill="#1E3A8A",
                                        font=("Consolas", 10, "bold"))

        bw, bh, sp = 80, 76, 16
        sx = 90
        items = list(self.messaging_engine.queue)

        # Update HUD
        self.hud_stats_lbl.config(
            text=f"buffered={len(items)} | delivered={len(self.messaging_engine.delivered_history)} | ops={self.op_counter}")

        # Dequeued card sliding out through exit chute
        if dequeued:
            dx = sx - out_off
            self._draw_msg_card(dx, py, bw, bh, dequeued, highlighted=True, scale=out_scale)
            self._draw_floating_badge(dx, py - bh / 2 - 12, "POPPED O(1)",
                                      bg_col="#166534", fg_col=COLOR_GREEN)

        # Active queue cards
        tail_idx = len(items) - 1
        for i, msg in enumerate(items):
            cx = sx + i * (bw + sp) - queue_shift
            cy = py
            card_scale = 1.0

            if incoming and msg.msg_id == incoming.msg_id:
                cx = (w + 40) - in_off
                card_scale = in_scale

            is_head = (i == 0 and not dequeued)
            is_tail = (i == tail_idx and not dequeued)

            if is_head and head_glow:
                self._draw_glow(cx, cy, 38, COLOR_GREEN, 3)

            if is_tail and new_tail_docked:
                self._draw_glow(cx, cy, 38, COLOR_BLUE, 2)

            self._draw_msg_card(cx, cy, bw, bh, msg, highlighted=(is_head and head_glow), scale=card_scale)

            # Doubly-Linked List Pointers (◀──▶)
            if i > 0 and not dequeued:
                prev_x = (sx + (i - 1) * (bw + sp)) - queue_shift
                if not (incoming and msg.msg_id == incoming.msg_id):
                    self.canvas.create_line(prev_x + (bw * 0.5) + 2, py,
                                            cx - (bw * 0.5) - 2, py,
                                            fill=COLOR_YELLOW, width=2.5, arrow=tk.BOTH)
                    self._draw_particle((prev_x + cx) / 2, py, 2.5, COLOR_YELLOW, halo=False)

        # Draw Expanding Shockwaves
        if shockwaves:
            for sx_pos, s_t, s_col in shockwaves:
                r = 20 + s_t * 40
                self.canvas.create_oval(sx_pos[0] - r, sx_pos[1] - r,
                                        sx_pos[0] + r, sx_pos[1] + r,
                                        outline=s_col, width=max(1, int(3 * (1 - s_t))))

        # Floating Animation Badges
        if floating_tag:
            fx, fy, f_text, f_col = floating_tag
            self._draw_floating_badge(fx, fy, f_text, bg_col="#0F172A", fg_col=f_col, border_col=f_col)

        self._draw_legend([
            (COLOR_GREEN,  "Head (Oldest — First Out)"),
            (COLOR_BLUE,   "Tail (Newest — Enqueued)"),
            (COLOR_YELLOW, "Doubly-Linked Pointers (◀──▶)"),
        ])

    def _draw_msg_card(self, x, y, w, h, msg, highlighted=False, scale=1.0):
        cw, ch = w * scale, h * scale
        x1, y1, x2, y2 = x - cw / 2, y - ch / 2, x + cw / 2, y + ch / 2
        bc = COLOR_YELLOW if highlighted else msg.color
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=ENGINE_CARD, outline=bc, width=2.5)
        self.canvas.create_rectangle(x1, y1, x2, y1 + 20 * scale, fill=msg.color, outline=bc, width=1)
        self.canvas.create_text(x, y1 + 10 * scale, text=f"#{msg.msg_id}",
                                fill="#FFFFFF", font=("Consolas", max(7, int(8 * scale)), "bold"))
        short = msg.text[:14] + ("…" if len(msg.text) > 14 else "")
        self.canvas.create_text(x, y + 4 * scale, text=short, fill=TEXT_BRIGHT,
                                font=("Segoe UI", max(6, int(7 * scale))), width=cw - 8)
        self.canvas.create_text(x, y2 - 10 * scale, text=msg.timestamp,
                                fill=TEXT_DIM, font=("Consolas", max(5, int(6 * scale))))

    # ---- Messaging Animations (Elastic Docking & Conveyor Slides) ------------
    def animate_enqueue(self, msg):
        """Cinematic enqueue: packet flies into pipeline with tracer particles and spring docks."""
        self.cancel_active_animation()
        self._stop_pulse()
        w = self.canvas.winfo_width() or 600
        py = (self.canvas.winfo_height() or 540) / 2
        tail = len(self.messaging_engine.queue) - 1
        bw, sp, sx = 80, 16, 90
        target = sx + tail * (bw + sp)
        total = (w + 60) - target
        FRAMES = 24

        def step(f):
            if self.current_tab != "messaging":
                return
            t = f / FRAMES
            eased_t = ease_out_back(t)
            eased_scale = 1.0 + 0.18 * math.sin(t * math.pi)

            # Traveling in
            in_pos = total * (1.0 - eased_t)
            tag_y = py - 52 - t * 12
            tag = (target, tag_y, f"📥 ENQUEUED #{msg.msg_id} [TAIL: O(1)]", COLOR_CYAN)

            waves = []
            if f > FRAMES - 6:
                prog = (f - (FRAMES - 6)) / 6.0
                waves = [((target, py), prog, COLOR_BLUE)]

            self.draw_messaging_pipeline(incoming=msg, in_off=total - in_pos,
                                         in_scale=eased_scale, shockwaves=waves,
                                         floating_tag=tag if f > 6 else None,
                                         new_tail_docked=(f == FRAMES))

            if f < FRAMES:
                self.active_animation = self.after(26, lambda: step(f + 1))
            else:
                self.draw_messaging_pipeline(new_tail_docked=True)
                self.status_lbl.config(text=f"▶  Msg #{msg.msg_id} docked at slot {tail}. FIFO Tail pointer updated in O(1).")
                self._start_messaging_pulse()

        step(0)

    def animate_dequeue(self, popped):
        """Cinematic dequeue: head packet illuminates, laser beam discharges, queue shifts forward."""
        self.cancel_active_animation()
        self._stop_pulse()
        py = (self.canvas.winfo_height() or 540) / 2
        bw, sp, sx = 80, 16, 90
        total_shift = bw + sp

        # Phase 1: Head Pulse & Golden Laser Beam Discharge
        HEAD_FRAMES = 12

        def head_step(hf):
            if self.current_tab != "messaging":
                return
            t = hf / HEAD_FRAMES
            eased_t = ease_out_quart(t)
            waves = [((sx, py), eased_t, COLOR_GREEN)]
            tag = (sx, py - 54, f"📬 DEQUEUEING #{popped.msg_id} [HEAD: O(1)]", COLOR_GREEN)
            self.draw_messaging_pipeline(head_glow=True, shockwaves=waves, floating_tag=tag)
            if hf < HEAD_FRAMES:
                self.active_animation = self.after(26, lambda: head_step(hf + 1))
            else:
                slide_step(0)

        # Phase 2: Slide Out to Chat & Conveyor Shift
        SLIDE_FRAMES = 24

        def slide_step(f):
            if self.current_tab != "messaging":
                return
            t = f / SLIDE_FRAMES
            eased_t = ease_in_out_cubic(t)
            eased_out = ease_out_quart(t)

            out_offset = (total_shift + 60) * eased_out
            out_scale = max(0.4, 1.0 - t * 0.5)
            shift = total_shift * (1.0 - eased_t)

            tag_y = py - 54 - t * 12
            tag = (sx - out_offset * 0.5, tag_y, f"DELIVERED #{popped.msg_id} ➔ CHAT", COLOR_GREEN)

            self.draw_messaging_pipeline(dequeued=popped, out_off=out_offset,
                                         out_scale=out_scale, queue_shift=shift,
                                         floating_tag=tag)

            if f < SLIDE_FRAMES:
                self.active_animation = self.after(26, lambda: slide_step(f + 1))
            else:
                self.draw_messaging_pipeline()
                self.status_lbl.config(text=f"▶  Msg #{popped.msg_id} delivered to chat transcript. FIFO Head advanced in strict O(1).")
                self._start_messaging_pulse()

        head_step(0)

    def _start_messaging_pulse(self):
        """Ambient conveyor animation for messaging pipeline."""
        self._stop_pulse()
        if self.current_tab != "messaging":
            return

        def pulse():
            if self.current_tab != "messaging":
                return
            self.pulse_tick += 1
            self.draw_messaging_pipeline()
            self.pulse_job = self.after(60, pulse)

        pulse()

    # ==========================================================================
    # 4. SEARCH TAB — BUILD & LOGIC (RECURSIVE TRIE VISUALIZATION)
    # ==========================================================================
    def _build_search_tab(self):
        parent = self.tab_search
        card = tk.Frame(parent, bg=LI_CARD_BG, relief=tk.SOLID, bd=1)
        card.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        tk.Label(card, text="Search Typeahead & Prefix Tree",
                 bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=14, pady=(10, 2))
        tk.Label(card, text="Instant auto-complete powered by a Trie with O(L) traversal.",
                 bg=LI_CARD_BG, fg=LI_TEXT_MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=14, pady=(0, 8))

        # Search bar
        sbox = tk.LabelFrame(card, text=" 🔍 Type to Search LinkedIn ",
                             bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                             font=("Segoe UI", 9, "bold"), padx=10, pady=6)
        sbox.pack(fill=tk.X, padx=14, pady=4)

        sr = tk.Frame(sbox, bg=LI_CARD_BG); sr.pack(fill=tk.X, pady=3)
        tk.Label(sr, text="🔍", bg=LI_CARD_BG, font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=(0, 4))
        self.search_entry = ttk.Entry(sr, font=("Segoe UI", 11))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.search_entry.bind("<KeyRelease>", self.on_search_key)
        ttk.Button(sr, text="Clear", style="Secondary.TButton",
                   command=self.on_clear_search).pack(side=tk.LEFT, padx=(6, 0))

        # Quick test tags
        qt = tk.Frame(sbox, bg=LI_CARD_BG); qt.pack(fill=tk.X, pady=(4, 2))
        tk.Label(qt, text="Quick Tests:", bg=LI_CARD_BG, fg=LI_TEXT_MUTED,
                 font=("Segoe UI", 8)).pack(side=tk.LEFT, padx=(0, 4))
        for s in ["soft", "data", "prod", "py", "mach", "satya", "dev"]:
            ttk.Button(qt, text=s, style="Secondary.TButton",
                       command=lambda q=s: self._set_search(q)).pack(side=tk.LEFT, padx=2)

        # Suggestions
        sugg = tk.LabelFrame(card, text=" Live Suggestions (Trie Matches) ",
                             bg=LI_CARD_BG, fg=LI_TEXT_MAIN,
                             font=("Segoe UI", 9, "bold"), padx=8, pady=4)
        sugg.pack(fill=tk.BOTH, expand=True, padx=14, pady=4)

        self.sugg_list = tk.Listbox(sugg, bg="#F8FAFC", fg=LI_TEXT_MAIN,
                                    font=("Segoe UI", 9), relief=tk.FLAT)
        self.sugg_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.sugg_list.bind("<<ListboxSelect>>", self.on_sugg_select)
        ss = ttk.Scrollbar(sugg, orient=tk.VERTICAL, command=self.sugg_list.yview)
        ss.pack(side=tk.RIGHT, fill=tk.Y)
        self.sugg_list.config(yscrollcommand=ss.set)

        self.trie_metrics = tk.Label(card,
                                     text="L=0 | Traversed: 1 (Root) | Matches: All",
                                     bg=LI_CARD_BG, fg=LI_BLUE,
                                     font=("Consolas", 9, "bold"))
        self.trie_metrics.pack(anchor="w", padx=14, pady=2)

        # DSA box
        dsa = tk.Frame(card, bg=LI_SECTION_BG, relief=tk.SOLID, bd=1)
        dsa.pack(fill=tk.X, padx=14, pady=(2, 8))
        tk.Label(dsa, text="⚙️  Trie / Prefix Tree Traversal",
                 bg=LI_SECTION_BG, fg=LI_BLUE,
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=8, pady=(4, 1))
        tk.Label(dsa,
                 text="• O(L) node lookups — completely independent of N\n"
                      "• Real-time outline highlights show exact traversal path\n"
                      "• Recursive layout supports arbitrary query depth",
                 bg=LI_SECTION_BG, fg=LI_TEXT_MUTED,
                 font=("Segoe UI", 8), justify=tk.LEFT).pack(anchor="w", padx=8, pady=(0, 4))

    # ---- Search callbacks ----------------------------------------------------
    def _set_search(self, q):
        self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, q)
        self.on_search_key(None)

    def on_clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.on_search_key(None)

    def on_search_key(self, event):
        query = self.search_entry.get()
        traversed, suggestions, is_valid = self.trie_engine.search_prefix(query)
        self.sugg_list.delete(0, tk.END)
        for s in suggestions:
            self.sugg_list.insert(tk.END, f"  🔍  {s}")

        path_str = " → ".join(f"'{n.char}'" for n in traversed)
        status = "✓ Valid" if is_valid else "✗ Miss"
        self.trie_metrics.config(
            text=f"L={len(query)} | Path: {path_str} | {status} | {len(suggestions)} matches")
        self.status_lbl.config(
            text=f"▶  Trie traversed {len(traversed)} nodes in O(L). {len(suggestions)} suggestions.")
        self.animate_trie_search(query, traversed, is_valid, suggestions)

    def on_sugg_select(self, event):
        sel = self.sugg_list.curselection()
        if sel:
            word = self.sugg_list.get(sel[0]).replace("🔍", "").strip()
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, word)
            self.on_search_key(None)

    # ---- Trie Animations (Cascade Laser & Tip Radiant Bursts) ----------------
    def animate_trie_search(self, query, traversed, is_valid, suggestions):
        """Sequential laser cascade down Trie branches with arrival shockwaves."""
        self.cancel_active_animation()
        self._stop_pulse()
        self.last_trie_data = (query, traversed, is_valid, suggestions)

        if not query:
            self.draw_trie_tree(query="", traversed_nodes=[self.trie_engine.root], is_valid=True)
            return

        n_steps = len(traversed)

        def run_step(step_idx):
            if self.current_tab != "search":
                return
            if step_idx < n_steps:
                curr_traversed = traversed[:step_idx + 1]
                active_tip = curr_traversed[-1]
                waves = [(active_tip, 0.45, COLOR_CYAN)]
                banner = f"⚡ TRAVERSING TRIE: Inspecting character '{active_tip.char.upper()}' (Depth: {step_idx}/{len(query)})"
                self.draw_trie_tree(query=query, traversed_nodes=curr_traversed,
                                    is_valid=True, shockwaves=waves,
                                    active_tip=active_tip,
                                    banner_tag=(banner, COLOR_CYAN))
                self.active_animation = self.after(55, lambda: run_step(step_idx + 1))
            else:
                tip_burst(0)

        def tip_burst(f):
            if self.current_tab != "search":
                return
            BURST_FRAMES = 20
            t = f / BURST_FRAMES
            tip_node = traversed[-1]

            if is_valid:
                waves = [(tip_node, t, COLOR_YELLOW)]
                scale = 1.0 + 0.35 * math.sin(t * math.pi)
                scales = {tip_node: scale}
                self.draw_trie_tree(query=query, traversed_nodes=traversed,
                                    is_valid=True, shockwaves=waves,
                                    node_scales=scales, shimmer_children=True,
                                    active_tip=tip_node,
                                    banner_tag=(f"✓ PREFIX MATCH: '{query}' ➔ Found {len(suggestions)} suggestion(s) in O(L) time!", COLOR_YELLOW))
            else:
                waves = [(tip_node, t, COLOR_RED)]
                shake_x = math.sin(f * math.pi * 0.9) * 6 * (1.0 - t)
                self.draw_trie_tree(query=query, traversed_nodes=traversed,
                                    is_valid=False, shockwaves=waves,
                                    shake_offset=shake_x, active_tip=tip_node,
                                    banner_tag=(f"✗ NO MATCH: Branch for '{query[-1]}' not found in Trie!", COLOR_RED))

            if f < BURST_FRAMES:
                self.active_animation = self.after(28, lambda: tip_burst(f + 1))
            else:
                self._start_trie_pulse(query, traversed, is_valid)

        run_step(0)

    def _start_trie_pulse(self, query, traversed, is_valid):
        """Ambient breathing pulse for active Trie query path."""
        self._stop_pulse()
        if self.current_tab != "search" or not traversed:
            return

        def pulse():
            if self.current_tab != "search" or self.last_trie_data is None:
                return
            self.pulse_tick += 1
            tip_node = traversed[-1]
            t_wave = (math.sin(self.pulse_tick * 0.14) + 1.0) / 2.0
            scales = {tip_node: 1.0 + 0.12 * t_wave}
            self.draw_trie_tree(query=query, traversed_nodes=traversed,
                                is_valid=is_valid, node_scales=scales,
                                shimmer_children=is_valid,
                                active_tip=tip_node)
            self.pulse_job = self.after(50, pulse)

        pulse()

    # ---- Trie Drawing (RECURSIVE LAYOUT WITH ANIMATION OVERLAYS) -------------
    def draw_trie_tree(self, query="", traversed_nodes=None, is_valid=True,
                       shockwaves=None, node_scales=None, shake_offset=0,
                       shimmer_children=False, active_tip=None, banner_tag=None):
        if self.current_tab != "search":
            return
        self.canvas.delete("all")
        self._draw_grid_bg()

        w = self.canvas.winfo_width() or 600
        h = self.canvas.winfo_height() or 540
        node_scales = node_scales or {}

        if traversed_nodes is None:
            traversed_nodes, _, is_valid = self.trie_engine.search_prefix(query)

        traversed_set = set(traversed_nodes)
        tip_node = active_tip or (traversed_nodes[-1] if traversed_nodes else None)
        root = self.trie_engine.root

        # Update HUD
        self.hud_stats_lbl.config(
            text=f"trie_nodes={self.trie_engine.total_nodes()} | "
                 f"max_depth={self.trie_engine.max_depth()} | ops={self.op_counter}")

        # Recursive layout
        coords: dict = {}
        edges: list = []
        max_vis_depth = max(6, len(query) + 2)
        max_children = 5

        def layout(node, x, y, h_space, depth):
            coords[node] = (x, y)
            if depth >= max_vis_depth:
                return

            kids = list(node.children.keys())
            if len(query) > depth:
                target = query[depth].lower()
                if target in kids:
                    kids.remove(target)
                    kids.insert(0, target)
            kids = kids[:max_children]

            n_kids = len(kids)
            if n_kids == 0:
                return

            v_gap = min(78, max(50, (h - 80) / (max_vis_depth + 1)))
            child_y = y + v_gap

            total_w = (n_kids - 1) * h_space
            start_x = x - total_w / 2

            for i, ch in enumerate(kids):
                child = node.children[ch]
                cx = start_x + i * h_space
                edges.append((node, child))
                next_h = h_space / max(1.6, n_kids * 0.6)
                layout(child, cx, child_y, next_h, depth + 1)

        initial_h_space = (w - 80) / max(3, min(len(root.children), max_children))
        layout(root, w / 2, 46, initial_h_space, 0)

        # Draw Edges
        for p_node, c_node in edges:
            if p_node in coords and c_node in coords:
                px, py = coords[p_node]
                cx, cy = coords[c_node]
                is_path = p_node in traversed_set and c_node in traversed_set
                is_candidate = shimmer_children and p_node == tip_node and c_node not in traversed_set

                if is_path:
                    # Glowing outer laser line
                    self.canvas.create_line(px, py, cx, cy, fill=GLOW_YELLOW, width=6.0)
                    # Core golden line
                    self.canvas.create_line(px, py, cx, cy, fill=COLOR_YELLOW, width=3.5)
                elif is_candidate:
                    self.canvas.create_line(px, py, cx, cy, fill=COLOR_GREEN, width=2.5, dash=(4, 2))
                else:
                    self.canvas.create_line(px, py, cx, cy, fill="#334155", width=1.5)

        # Draw Shockwaves
        self._draw_shockwaves(coords, shockwaves)

        # Draw Nodes
        base_radius = 18
        for node, (x, y) in coords.items():
            if node == tip_node and shake_offset != 0:
                x += shake_offset

            sc = node_scales.get(node, 1.0)
            radius = base_radius * sc

            is_trav = node in traversed_set
            is_tip = (node == tip_node)
            is_candidate = shimmer_children and tip_node and node in tip_node.children.values()

            if is_tip:
                if is_valid:
                    self._draw_glow(x, y, radius, COLOR_YELLOW, 3)
                    fill, outline, ow = GLOW_YELLOW, COLOR_YELLOW, 3.5
                else:
                    self._draw_glow(x, y, radius, COLOR_RED, 3)
                    fill, outline, ow = "#7F1D1D", COLOR_RED, 3.5
            elif is_trav:
                self._draw_glow(x, y, radius, COLOR_BLUE, 2)
                fill, outline, ow = "#0C4A6E", COLOR_BLUE, 3.0
            elif is_candidate:
                fill, outline, ow = "#064E3B", COLOR_GREEN, 2.0
            else:
                fill, outline, ow = ENGINE_CARD, ENGINE_BORDER, 1.5

            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                    fill=fill, outline=outline, width=ow)
            label = "ROOT" if node is root else node.char.upper()
            fs = max(6, int((7 if node is root else 10) * sc))
            self.canvas.create_text(x, y, text=label, fill="#FFFFFF",
                                    font=("Consolas", fs, "bold"))

        # Floating Banner Tag
        if banner_tag:
            b_text, b_col = banner_tag
            self._draw_floating_badge(w / 2, h - 50, b_text, bg_col="#0F172A", fg_col=b_col, border_col=b_col)
        elif query and not is_valid:
            self.canvas.create_text(w / 2, h - 50,
                                    text=f"⚠ Prefix '{query}' not found in Trie",
                                    fill=COLOR_RED, font=("Segoe UI", 10, "bold"))

        self._draw_legend([
            (COLOR_YELLOW, "Active Traversal Tip"),
            (COLOR_BLUE,   "O(L) Traversed Path"),
            (COLOR_GREEN,  "Candidate Branches"),
            (COLOR_RED,    "Prefix Miss / Dead Branch"),
        ])


# ==============================================================================
# APPLICATION ENTRY POINT
# ==============================================================================
if __name__ == "__main__":
    app = LinkedInDSASimulator()
    app.mainloop()
