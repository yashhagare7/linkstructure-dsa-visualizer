"""
==============================================================================
UNIT TEST SUITE FOR LINKEDIN DSA SIMULATOR v2.0
Covers all 4 core data structures:
  1. GraphNetwork (Undirected Graph / Adjacency List + Hash Sets)
  2. MaxHeapFeed (Priority Queue / Binary Max-Heap)
  3. MessagingQueue (FIFO Queue / collections.deque)
  4. SearchTrie (Multi-way Prefix Tree)
==============================================================================
"""

import unittest
from linkedin_simulator import GraphNetwork, MaxHeapFeed, MessagingQueue, SearchTrie, FeedPost, MessagePacket, TrieNode


class TestGraphNetwork(unittest.TestCase):
    def setUp(self):
        self.graph = GraphNetwork()

    def test_default_initialization(self):
        users = self.graph.get_users()
        self.assertGreaterEqual(len(users), 8)
        self.assertIn("Satya Nadella", users)
        self.assertIn("Sundar Pichai", users)
        self.assertGreaterEqual(self.graph.edge_count(), 14)

    def test_add_and_remove_user(self):
        # Add User
        added = self.graph.add_user("Alan Turing", "Father of Modern CS")
        self.assertTrue(added)
        self.assertIn("Alan Turing", self.graph.get_users())
        self.assertEqual(self.graph.roles["Alan Turing"], "Father of Modern CS")

        # Duplicate Add Check
        dup = self.graph.add_user("Alan Turing")
        self.assertFalse(dup)

        # Connect Alan Turing to Satya Nadella
        self.graph.add_connection("Alan Turing", "Satya Nadella")
        self.assertTrue(self.graph.has_connection("Alan Turing", "Satya Nadella"))
        self.assertTrue(self.graph.has_connection("Satya Nadella", "Alan Turing"))

        # Remove User & Verify Edge Cleanup
        removed = self.graph.remove_user("Alan Turing")
        self.assertTrue(removed)
        self.assertNotIn("Alan Turing", self.graph.get_users())
        self.assertNotIn("Alan Turing", self.graph.adj["Satya Nadella"])

    def test_add_and_remove_connection(self):
        self.graph.add_user("Alice")
        self.graph.add_user("Bob")

        # Add edge
        linked = self.graph.add_connection("Alice", "Bob")
        self.assertTrue(linked)
        self.assertTrue(self.graph.has_connection("Alice", "Bob"))

        # Duplicate link
        linked_again = self.graph.add_connection("Alice", "Bob")
        self.assertFalse(linked_again)

        # Remove edge
        unlinked = self.graph.remove_connection("Alice", "Bob")
        self.assertTrue(unlinked)
        self.assertFalse(self.graph.has_connection("Alice", "Bob"))

    def test_mutual_connections_set_intersection(self):
        # Satya Nadella and Demis Hassabis share mutuals
        mutuals = self.graph.get_mutual_connections("Satya Nadella", "Demis Hassabis")
        # In default network:
        # Satya connects: Sundar, Sam, Demis
        # Demis connects: Satya, Sundar, Sam, Yann, Geoffrey
        # Mutuals between Satya & Demis: Sundar, Sam
        self.assertIn("Sundar Pichai", mutuals)
        self.assertIn("Sam Altman", mutuals)
        self.assertEqual(len(mutuals), 2)

    def test_disjoint_mutual_connections(self):
        self.graph.add_user("Isolated_A")
        self.graph.add_user("Isolated_B")
        mutuals = self.graph.get_mutual_connections("Isolated_A", "Isolated_B")
        self.assertEqual(len(mutuals), 0)


class TestMaxHeapFeed(unittest.TestCase):
    def setUp(self):
        self.feed = MaxHeapFeed()

    def test_heap_invariant_on_initialization(self):
        # Root must hold the maximum engagement score
        nodes = self.feed.tree_nodes
        self.assertGreater(len(nodes), 0)
        max_score = nodes[0].score

        # Check every child <= parent
        for i in range(1, len(nodes)):
            parent = (i - 1) // 2
            self.assertLessEqual(nodes[i].score, nodes[parent].score)

        self.assertEqual(max_score, 950)  # Demis Hassabis initial breakthrough post

    def test_prepare_insert_heapify_up(self):
        initial_len = len(self.feed.tree_nodes)
        new_post, swaps = self.feed.prepare_insert("Ada Lovelace", "First computer programmer", 2000)

        # It should become the new maximum (root)
        self.assertEqual(len(self.feed.tree_nodes), initial_len + 1)
        self.assertGreater(len(swaps), 0)

        # After applying all swaps
        for child_idx, parent_idx in swaps:
            self.feed.execute_single_swap(child_idx, parent_idx)

        self.assertEqual(self.feed.tree_nodes[0].score, 2000)
        self.assertEqual(self.feed.tree_nodes[0].author, "Ada Lovelace")

    def test_prepare_extract_heapify_down(self):
        initial_len = len(self.feed.tree_nodes)
        top_post, swaps = self.feed.prepare_extract()

        self.assertEqual(top_post.score, 950)
        self.assertEqual(len(self.feed.tree_nodes), initial_len - 1)

        # Apply swaps
        for p_idx, c_idx in swaps:
            self.feed.execute_single_swap(p_idx, c_idx)

        # Root must still maintain heap invariant
        nodes = self.feed.tree_nodes
        for i in range(1, len(nodes)):
            parent = (i - 1) // 2
            self.assertLessEqual(nodes[i].score, nodes[parent].score)

    def test_depth_calculation(self):
        # 7 items -> depth = floor(log2(7)) + 1 = 3
        self.assertEqual(self.feed.depth(), 3)


class TestMessagingQueue(unittest.TestCase):
    def setUp(self):
        self.msg_queue = MessagingQueue()

    def test_fifo_ordering(self):
        # Clear default
        self.msg_queue.queue.clear()

        self.msg_queue.enqueue("User1", "Message 1")
        self.msg_queue.enqueue("User2", "Message 2")
        self.msg_queue.enqueue("User3", "Message 3")

        self.assertEqual(len(self.msg_queue.queue), 3)

        # First in, first out
        m1 = self.msg_queue.dequeue()
        self.assertEqual(m1.text, "Message 1")
        self.assertEqual(m1.sender, "User1")

        m2 = self.msg_queue.dequeue()
        self.assertEqual(m2.text, "Message 2")

        m3 = self.msg_queue.dequeue()
        self.assertEqual(m3.text, "Message 3")

        # Now empty
        self.assertIsNone(self.msg_queue.dequeue())
        self.assertEqual(len(self.msg_queue.delivered_history), 3)

    def test_peek(self):
        self.msg_queue.queue.clear()
        self.assertIsNone(self.msg_queue.peek())
        self.msg_queue.enqueue("Tester", "Test packet")
        self.assertEqual(self.msg_queue.peek().text, "Test packet")
        self.assertEqual(len(self.msg_queue.queue), 1)


class TestSearchTrie(unittest.TestCase):
    def setUp(self):
        self.trie = SearchTrie()

    def test_prefix_search_valid(self):
        # Search for "soft" -> Should return "software engineer", "software architect", etc.
        traversed, suggestions, is_valid = self.trie.search_prefix("soft")
        self.assertTrue(is_valid)
        self.assertEqual(len(traversed), 5)  # [ROOT] -> s -> o -> f -> t
        self.assertIn("software engineer", suggestions)
        self.assertIn("software architect", suggestions)
        self.assertIn("soft skills trainer", suggestions)

    def test_prefix_search_invalid(self):
        traversed, suggestions, is_valid = self.trie.search_prefix("xyznonexistent")
        self.assertFalse(is_valid)
        self.assertEqual(len(suggestions), 0)

    def test_case_insensitivity(self):
        _, sugg_lower, valid_lower = self.trie.search_prefix("satya")
        _, sugg_upper, valid_upper = self.trie.search_prefix("SATYA")
        self.assertTrue(valid_lower)
        self.assertTrue(valid_upper)
        self.assertEqual(sugg_lower, sugg_upper)

    def test_custom_insert_and_retrieval(self):
        self.trie.insert("quantum computer")
        traversed, suggestions, is_valid = self.trie.search_prefix("quant")
        self.assertTrue(is_valid)
        self.assertIn("quantum computer", suggestions)

    def test_node_count_and_depth(self):
        self.assertGreater(self.trie.total_nodes(), 50)
        self.assertGreater(self.trie.max_depth(), 10)


if __name__ == "__main__":
    unittest.main()
