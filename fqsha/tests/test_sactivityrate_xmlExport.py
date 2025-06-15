import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import json
import unittest
import os
import math
import numpy as np
from fqsha.SeismicActivityRate import sactivityrate, momentbudget
from fqsha.FQSHA_Functions import export_faults_to_xml
from copy import deepcopy


class TestSeismicActivityRate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Prevent blocking from plt.show()
        plt.show = lambda *args, **kwargs: None

        cls.test_dir = os.path.dirname(os.path.abspath(__file__))
        cls.output_dir = os.path.join(cls.test_dir, 'test_output_files')
        os.makedirs(cls.output_dir, exist_ok=True)
        cls.figures_dir = os.path.join(cls.output_dir, 'Figures')
        os.makedirs(cls.figures_dir, exist_ok=True)
        cls.xml_dir = os.path.join(cls.output_dir, 'XML_Exports')
        os.makedirs(cls.xml_dir, exist_ok=True)

        cls.test_data_path = os.path.join(cls.test_dir, 'Faults_test.json')
        with open(cls.test_data_path) as f:
            cls.original_faults = json.load(f)

        cls.prepared_faults = momentbudget(
            faults=deepcopy(cls.original_faults),
            Zeta=0.5,
            Khi=0.2,
            Siggma=0.3,
            ProjFol=cls.output_dir,
            logical_nan=True,
            logical_nan_sdmag=True
        )

        for fault in cls.prepared_faults.values():
            fault.update({
                'CV': fault.get('CV', 0.5),
                'Mmin': fault.get('Mmin', 5.0),
                'b-value': fault.get('b-value', 1.0),
                'Telap': fault.get('Telap', 1000),
                'mag_scale': fault.get('mag_scale', 'WC94'),
                'bin': fault.get('bin', 0.1)
            })

    def setUp(self):
        self.test_faults = deepcopy(self.prepared_faults)
        np.random.seed(42)
        self.result = sactivityrate(
            faults=deepcopy(self.test_faults),
            Fault_behaviour="Truncated Gutenberg Richter",
            w=50,
            bin=0.1,
            ProjFol=self.__class__.figures_dir
        )
        plt.close('all')

    def test_truncated_gr_behaviour(self):
        expected_fields = ['rates', 'b-value']
        for fault_name, fault_data in self.result.items():
            with self.subTest(fault=fault_name):
                for field in expected_fields:
                    self.assertIn(field, fault_data)

    def test_output_consistency(self):
        required_fields = [
            'Mmax', 'sdMmax', 'MomentRate',
            'Tmean', 'L_forTmean', 'Width', 'V',
            'bin', 'rates', 'b-value'
        ]
        for fault_name, fault_data in self.result.items():
            with self.subTest(fault=fault_name):
                for field in required_fields:
                    self.assertIn(field, fault_data)

        try:
            export_faults_to_xml(self.result, self.__class__.xml_dir)
            xml_files = os.listdir(self.__class__.xml_dir)
            self.assertEqual(len(xml_files), len(self.result))
            for file in xml_files:
                self.assertTrue(file.endswith('.xml'))
        except Exception as e:
            self.fail(f"XML export failed: {str(e)}")

    def test_morate_calculation(self):
        valid_morate_count = 0
        for fault_name, fault_data in self.result.items():
            with self.subTest(fault=fault_name):
                self.assertIn('MomentRate', fault_data)
                if math.isnan(fault_data['MomentRate']):
                    continue
                valid_morate_count += 1
                self.assertGreater(fault_data['MomentRate'], 0)
        self.assertGreater(valid_morate_count, 0)


if __name__ == '__main__':
    unittest.main()
