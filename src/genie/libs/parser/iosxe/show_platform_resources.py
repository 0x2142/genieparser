''' show_platform_resources.py
'''

import re
import logging

from genie.metaparser import MetaParser
from genie.libs.parser.utils.common import Common
from genie.metaparser.util.schemaengine import Schema, Any


logger = logging.getLogger(__name__)


# ==============================
# Schema for 'show show platform resources'
# ==============================

class ShowPlatformResourcesSchema(MetaParser):
    # KV pairs
    schema = {
    'processor': {
        Any(): {
            Any(): {
                'usage': str,
                'max': str,
                'warning': str,
                'critical': str,
                'state': str
                }
            }
        }
    }

    
# ==============================
# Parser for 'show platform resources'
# ==============================

# The parser class inherits from the schema class
class ShowPlatformResources(ShowPlatformResourcesSchema):
    ''' Parser for "show platform resources"'''

    cli_command = 'show platform resources'

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output 

        parsed_dict = {}

        #show platform resources
        #**State Acronym: H - Healthy, W - Warning, C - Critical                                             
        #Resource                 Usage                 Max             Warning         Critical        State
        #----------------------------------------------------------------------------------------------------
        #RP0 (ok, active)                                                                               H    
        # Control Processor       9.10%                 100%            80%             90%             H    
        #  DRAM                   2570MB(65%)           3942MB          88%             93%             H    
        #ESP0(ok, active)                                                                               H    
        # QFP                                                                                           H    
        #  DRAM                   27467KB(10%)          262144KB        80%             90%             H    
        #  IRAM                   213KB(10%)            2048KB          80%             90%             H    
        #  CPU Utilization        0.00%                 100%            90%             95%             H    

        p1 = re.compile(r'(?P<processor>\w{1,5}\d\s?\(\w+, \w+\))')
        p2 = re.compile(r'(?P<resource>\w+(\s\w+)?)\s+(?P<usage>\d{1,3}'
                        '(.\d{2})?%|\d{1,6}[K,M]B\(\d{0,2}%\))\s+'
                        '(?P<max>\d{1,3}(.\d{2})?%|\d{1,6}[K,M]B)\s+'
                        '(?P<warning>\d{1,3}(.\d{2})?%)\s+'
                        '(?P<critical>\d{1,3}(.\d{2})?%)\s+'
                        '(?P<state>[H,W,C])')

        for line in out.splitlines():
            line = line.strip()

            # Matches against route processor
            #  RP0 (ok, active)
            #  ESP0(ok, active)
            m = p1.match(line)
            if m:
                group = m.groupdict()
                proc = group['processor']
                parsed_dict.setdefault('processor', {}).\
                                        setdefault(proc,{})
                proc_dict = parsed_dict['processor']

            # Matches each underlying resource (Control Proc, DRAM, etc)
            # and associated statistics
            m2 = p2.match(line)
            if m2:
                group = m2.groupdict()
                resource = group['resource']
                proc_dict[proc].setdefault(resource, {})
                proc_dict[proc][resource]['usage'] = group['usage']
                proc_dict[proc][resource]['max'] = group['max'] 
                proc_dict[proc][resource]['warning'] = group['warning']
                proc_dict[proc][resource]['critical'] = group['critical']
                proc_dict[proc][resource]['state'] = group['state']

                continue

        return(parsed_dict)
