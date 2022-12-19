from unittest import TestCase
from assessment import SomeModel, predict_message_mood

class TestAssessment(TestCase):
    def setUp(self) -> None:
       self.model = SomeModel()
       self.bad = "неуд"
       self.norm = "норм"
       self.good = "отл"

    def test_bad(self):
        message = "они и мы"
        expected = self.bad
        result = predict_message_mood(message, self.model)
        self.assertEqual(result, expected)
    
    def test_norm(self):
        message = "это не самое плохое сообщение"
        expected = self.norm
        result = predict_message_mood(message, self.model)
        self.assertEqual(result, expected)
    
    def test_ok(self):
        message = "просто идельное сообщение, подходящее идеальному тесту"
        expected = self.good
        result = predict_message_mood(message, self.model)
        self.assertEqual(result, expected)
    
    def test_empty(self):
        message = ""
        self.assertRaises(ZeroDivisionError, predict_message_mood, message, self.model)

