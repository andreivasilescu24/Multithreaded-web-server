import json
import unittest
import os
import sys
from deepdiff import DeepDiff

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from data_ingestor import DataIngestor

class TestWebserver(unittest.TestCase):
    def setUp(self):
        self.data_ingestor = DataIngestor("test_table.csv")
        self.question = 'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week'
        self.state1 = 'Indiana'
        self.state2 = 'Washington' 
        self.json_req_question = {'question': self.question}
        self.json_req_question_state1 = {'question': self.question, 'state': self.state1}
        self.json_req_question_state2 = {'question': self.question, 'state': self.state2}

    def read_json(self, filename):
        import json
        with open(filename, "r") as f:
            return json.load(f)

    def test_states_mean(self):
        result = self.data_ingestor.states_mean(self.json_req_question)
        ref_data = self.read_json("my_tests/states_mean_test.json")
       
        d = DeepDiff(result, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_state_mean(self):
        result = self.data_ingestor.state_mean(self.json_req_question_state1)
        ref_data = self.read_json("my_tests/state_mean_test.json")
        d = DeepDiff(result, ref_data, math_epsilon=0.01)

    def test_best5(self):
        result = self.data_ingestor.best5(self.json_req_question)
        ref_data = self.read_json("my_tests/best5_test.json")
        d = DeepDiff(result, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))
    
    def test_worst5(self):
        result = self.data_ingestor.worst5(self.json_req_question)
        ref_data = self.read_json("my_tests/worst5_test.json")
        d = DeepDiff(result, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_global_mean(self):
        result = self.data_ingestor.global_mean(self.json_req_question)
        ref_data = self.read_json("my_tests/global_mean_test.json")
        self.assertSetEqual(set(result.keys()), set(ref_data.keys()))
        self.assertAlmostEqual(result['global_mean'], ref_data['global_mean'], delta=0.01)

    def test_diff_from_mean(self):
        result = self.data_ingestor.diff_from_mean(self.json_req_question)
        ref_data = self.read_json("my_tests/diff_from_mean_test.json")
        self.assertSetEqual(set(result.keys()), set(ref_data.keys()))
        for key in result.keys():
            self.assertAlmostEqual(result[key], ref_data[key], delta=0.01)

    def test_state_diff_from_mean(self):
        result = self.data_ingestor.state_diff_from_mean(self.json_req_question_state2)
        ref_data = self.read_json("my_tests/state_diff_from_mean_test.json")
        self.assertSetEqual(set(result.keys()), set(ref_data.keys()))
        for key in result.keys():
            self.assertAlmostEqual(result[key], ref_data[key], delta=0.01)

    def test_mean_by_category(self):
        result = self.data_ingestor.mean_by_category(self.json_req_question)
        ref_data = self.read_json("my_tests/mean_by_category_test.json")
        d = DeepDiff(result, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    def test_state_mean_by_category(self):
        result = self.data_ingestor.state_mean_by_category(self.json_req_question_state1)
        ref_data = self.read_json("my_tests/state_mean_by_category_test.json")
        d = DeepDiff(result, ref_data, math_epsilon=0.01)
        self.assertTrue(d == {}, str(d))

    
if __name__ == '__main__':
    unittest.main()
