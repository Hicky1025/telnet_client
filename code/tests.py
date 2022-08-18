import unittest
import telnet


class Test_num_double(unittest.TestCase):
    def test(self):
        self.assertEqual(telnet.gen_packet("startup"), "packet")
        

if __name__ == "__main__":
    unittest.main()