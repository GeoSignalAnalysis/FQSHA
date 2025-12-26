import unittest
from unittest.mock import patch, mock_open
import json
import sys
from PyQt5.QtWidgets import QApplication, QFrame, QFileDialog
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
from FQSHA import Ui_Frame
import os


class TestFQSHA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize QApplication once for all tests"""
        cls.app = QApplication(sys.argv)
        # Create a temporary test file
        cls.test_dir = os.path.dirname(os.path.abspath(__file__))
        cls.test_file_path = os.path.join(cls.test_dir, 'Fault_data.json')

        test_data = {
            "fault1": {
                "upperSeismoDepth": 5,
                "lowerSeismoDepth": 15,
                "Dip": 30,
                "fault_trace": [[1.0, 2.0], [3.0, 4.0]]
            }
        }

        with open(cls.test_file_path, 'w') as f:
            json.dump(test_data, f)

    @classmethod
    def tearDownClass(cls):
        """Clean up QApplication and test files"""
        cls.app.quit()
        # Clean up temporary files
        try:
            os.remove(cls.test_file_path)
        except:
            pass

    def setUp(self):
        """Create a fresh UI instance for each test"""
        self.frame = QFrame()
        self.ui = Ui_Frame()
        self.ui.setupUi(self.frame)
        self.frame.show()

    def tearDown(self):
        """Clean up after each test"""
        self.frame.close()

    def test_ui_initialization(self):
        """Test that UI components are properly initialized"""
        self.assertTrue(hasattr(self.ui, 'pushButton'), "Browse button not found")
        self.assertTrue(hasattr(self.ui, 'textEdit_13'), "Output file text edit not found")
        self.assertTrue(hasattr(self.ui, 'comboBox'), "MFD combo box not found")

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    def test_browse_file_dialog(self, mock_dialog):
        """Test that file dialog opens with correct parameters"""
        mock_dialog.return_value = (self.test_file_path, "JSON files (*.json)")

        # Simulate button click
        QTest.mouseClick(self.ui.pushButton, Qt.LeftButton)

        # Verify dialog was called with correct parameters
        mock_dialog.assert_called_once_with(
            None,
            "Select the input file:",
            "Choose one:",
            "JSON files (*.json);;All files (*)",
            options=unittest.mock.ANY
        )

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    @patch('builtins.open', new_callable=mock_open)
    def test_load_valid_json(self, mock_file, mock_dialog):
        """Test loading a valid JSON file (mocked)"""
        test_json = {
            "fault1": {
                "upperSeismoDepth": 5,
                "lowerSeismoDepth": 15,
                "Dip": 30,
                "fault_trace": [[1.0, 2.0], [3.0, 4.0]]
            }
        }
        mock_dialog.return_value = ("valid.json", "JSON files (*.json)")
        mock_file.return_value.read.return_value = json.dumps(test_json)

        # Simulate button click
        QTest.mouseClick(self.ui.pushButton, Qt.LeftButton)

        # Verify file operations
        mock_file.assert_called_once_with("valid.json", 'r')

        # Verify data was loaded correctly
        self.assertIsNotNone(self.ui.faults)
        self.assertEqual(len(self.ui.faults), 1)
        self.assertEqual(self.ui.faults["fault1"]["upperSeismoDepth"], 5)
        self.assertEqual(self.ui.faults["fault1"]["Dip"], 30)

        # Verify input_file_var was set
        self.assertEqual(self.ui.input_file_var, "valid.json")

    @patch('PyQt5.QtWidgets.QFileDialog.getOpenFileName')
    def test_real_file_loading(self, mock_dialog):
        """Test loading from an actual test file"""
        mock_dialog.return_value = (self.test_file_path, "JSON files (*.json)")

        # Simulate button click
        QTest.mouseClick(self.ui.pushButton, Qt.LeftButton)

        # Verify results
        self.assertEqual(self.ui.input_file_var, self.test_file_path)
        self.assertIsNotNone(self.ui.faults)
        self.assertEqual(self.ui.faults["fault1"]["upperSeismoDepth"], 5)
        self.assertEqual(self.ui.faults["fault1"]["Dip"], 30)

    def test_mfd_selection(self):
        """Test MFD combo box functionality"""
        # Test initial state
        self.assertEqual(self.ui.comboBox.currentIndex(), 0)

        # Change selection
        self.ui.comboBox.setCurrentIndex(1)
        self.assertEqual(self.ui.comboBox.currentText(), "Truncated Gutenberg Richter")

        self.ui.comboBox.setCurrentIndex(2)
        self.assertEqual(self.ui.comboBox.currentText(), "Caracteristic gaussian")

    def test_calculation_mode_selection(self):
        """Test calculation mode combo box functionality"""
        # Test initial state
        self.assertEqual(self.ui.comboBox_2.currentIndex(), 0)

        # Change selection
        self.ui.comboBox_2.setCurrentIndex(1)
        self.assertEqual(self.ui.comboBox_2.currentText(), "classical")

        self.ui.comboBox_2.setCurrentIndex(2)
        self.assertEqual(self.ui.comboBox_2.currentText(), "event_based")


if __name__ == '__main__':
    unittest.main()