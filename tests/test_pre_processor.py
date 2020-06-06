import pre_processor
import unittest

class PreProcessorTest(unittest.TestCase):
    def test_whitelist(self):
        pp = pre_processor.PreProcessor(whitelist=['Brazil'])
        data = pp.pre_process()
        len_data = len(data)
        assert len_data == 1
    
    def test_blacklist(self):
        pp = pre_processor.PreProcessor(blacklist=['Brazil'])
        data = pp.pre_process()
        assert 'Brazil' not in data.keys()
    
    def test_data_identifiers(self):
        pp = pre_processor.PreProcessor(whitelist=['Brazil'], data_identifiers=['new_cases'])
        data = pp.pre_process()
        len_data = len(data['Brazil'])
        assert len_data == 1
        pp = pre_processor.PreProcessor(whitelist=['Brazil'])
        data = pp.pre_process(['new_cases'])
        len_data = len(data['Brazil'])
        assert len_data == 1