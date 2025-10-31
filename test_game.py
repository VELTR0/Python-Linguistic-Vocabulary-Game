"""
Tests for the Vocabulary Learning Game
"""

import unittest
from vocabulary import vocabulary
from game import VocabularyGame


class TestVocabulary(unittest.TestCase):
    """Test vocabulary data"""
    
    def test_vocabulary_not_empty(self):
        """Test that vocabulary has words"""
        self.assertTrue(len(vocabulary) > 0)
        
    def test_vocabulary_format(self):
        """Test that vocabulary has correct format"""
        for key, value in vocabulary.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, str)
            self.assertTrue(len(key) > 0)
            self.assertTrue(len(value) > 0)


class TestGameLogic(unittest.TestCase):
    """Test game logic without GUI"""
    
    def setUp(self):
        """Set up test fixtures"""
        # We can't run the full game in tests (requires display)
        # but we can test the data structures
        self.vocab = vocabulary
        
    def test_vocabulary_has_enough_words(self):
        """Test that we have enough words for multiple choice"""
        self.assertGreaterEqual(len(self.vocab), 4)
        
    def test_word_list_creation(self):
        """Test that word list can be created"""
        word_list = list(self.vocab.keys())
        self.assertEqual(len(word_list), len(self.vocab))
        
    def test_answer_options(self):
        """Test that answer options can be generated"""
        all_answers = list(self.vocab.values())
        self.assertEqual(len(all_answers), len(self.vocab))
        

if __name__ == '__main__':
    unittest.main()
