#!/bin/env python
import unittest
from unittest.mock import Mock

from pyats.topology import Device
from pyats.topology import loader

from genie.metaparser.util.exceptions import SchemaEmptyParserError,\
                                             SchemaMissingKeyError

from genie.libs.parser.iosxe.show_platform_resources \
                        import ShowPlatformResources


# ============================================
# unit test for 'show platform resources'
# =============================================
class test_show_platform_resources(unittest.TestCase):
    '''
       unit test show platform resources
    '''
    empty_output = {'execute.return_value': ''}

    # Expected Parsed output
    golden_parsed_output1 = {'processor': {'ESP0(ok, active)': {'CPU Utilization': {'critical': '95%',
                                                        'max': '100%',
                                                        'state': 'H',
                                                        'usage': '0.00%',
                                                        'warning': '90%'},
                                    'DRAM': {'critical': '90%',
                                             'max': '262144KB',
                                             'state': 'H',
                                             'usage': '27467KB(10%)',
                                             'warning': '80%'},
                                    'IRAM': {'critical': '90%',
                                             'max': '2048KB',
                                             'state': 'H',
                                             'usage': '213KB(10%)',
                                             'warning': '80%'}},
               'RP0 (ok, active)': {'Control Processor': {'critical': '90%',
                                                          'max': '100%',
                                                          'state': 'H',
                                                          'usage': '8.20%',
                                                          'warning': '80%'},
                                    'DRAM': {'critical': '93%',
                                             'max': '3942MB',
                                             'state': 'H',
                                             'usage': '2578MB(65%)',
                                             'warning': '88%'}}}}

    # Expected unparsed output
    golden_output1 = {'execute.return_value': '''
cEdge# show platform resources
**State Acronym: H - Healthy, W - Warning, C - Critical
Resource                 Usage                 Max             Warning         Critical        State
----------------------------------------------------------------------------------------------------
RP0 (ok, active)                                                                               H
 Control Processor       8.20%                 100%            80%             90%             H
  DRAM                   2578MB(65%)           3942MB          88%             93%             H
ESP0(ok, active)                                                                               H
 QFP                                                                                           H
  DRAM                   27467KB(10%)          262144KB        80%             90%             H
  IRAM                   213KB(10%)            2048KB          80%             90%             H
  CPU Utilization        0.00%                 100%            90%             95%             H
  '''}

    def test_show_platform_resources_full1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output1)
        obj = ShowPlatformResources(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output1)

    def test_show_platform_resources_empty(self):
            self.maxDiff = None
            self.device = Mock(**self.empty_output)
            obj = ShowPlatformResources(device=self.device)
            with self.assertRaises(SchemaEmptyParserError):
                parsed_output = obj.parse()

if __name__ == '__main__':
    unittest.main()