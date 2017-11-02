import re
import json

class MMCLIParser():
    @classmethod
    def save_json(cls, obj, fname):
        with open(fname, 'w') as json_file:
            json.dump(obj, json_file, indent=4)

    @classmethod
    def parse(cls, text):
        res = {}
        cur_sys = None
        cur_subsys = None
        lines = text.split('\n')

        for idx in range(0, len(lines)):
            line = lines[idx]
            if '-------------------------' in line:
                cur_sys = None
                cur_subsys = None
                continue

            if '|' not in line:
                continue

            if len(line.strip()) is 0:
                continue

            first_idx = line.find('|')
            if first_idx >= 10 and first_idx < 15:
                sys = re.search('([\w\d\s]+)', line[:first_idx]).group(1)
                sys = sys.strip()
                if sys is not '':
                    cur_sys = sys
                    res[cur_sys] = {}

                second_idx = line.find(':')
                if second_idx >= 25 and second_idx < 35:
                    subsys = re.search('([\w\d\s]+)', line[first_idx:second_idx]).group(1)
                    subsys = subsys.strip()
                    if subsys is not '':
                        cur_subsys = subsys
                        res[cur_sys][cur_subsys] = ''

                    val = line[second_idx:].strip().strip(':').strip().strip('\'')
                    if val is not '':
                        if res[cur_sys][cur_subsys] == '':
                            res[cur_sys][cur_subsys] += val
                        else:
                            res[cur_sys][cur_subsys] += ', ' + val

        return res

if __name__ == '__main__':
    text = '''
    
  -------------------------
  Hardware |   manufacturer: 'Sierra Wireless, Incorporated'
           |          model: 'MC7354'
           |       revision: 'SWI9X15C_05.05.58.00 r27038 carmd-fwbuild1 2015/03/04 21:30:23'
           |      supported: 'gsm-umts
           |                  cdma-evdo
           |                  lte
           |                  cdma-evdo, gsm-umts
           |                  gsm-umts, lte
           |                  cdma-evdo, lte
           |                  cdma-evdo, gsm-umts, lte'
           |        current: 'gsm-umts, lte'
           |   equipment id: '359225050108901'
  -------------------------
  System   |         device: '/sys/devices/pci0000:00/0000:00:14.0/usb1/1-3'
           |        drivers: 'option1, qmi_wwan'
           |         plugin: 'Sierra'
           |   primary port: 'cdc-wdm0'
           |          ports: 'ttyUSB2 (at), cdc-wdm0 (qmi), cdc-wdm1 (qmi), wwan1 (net), wwan0 (net)'
  -------------------------
  Numbers  |           own : '13035708302'
  -------------------------
  Status   |           lock: 'sim-pin2'
           | unlock retries: 'sim-pin (3), sim-pin2 (3), sim-puk (10), sim-puk2 (10)'
           |          state: 'registered'
           |    power state: 'on'
           |    access tech: 'lte'
           | signal quality: '59' (recent)
  -------------------------
  Modes    |      supported: 'allowed: 2g, 3g, 4g; preferred: none'
           |        current: 'allowed: 2g, 3g, 4g; preferred: none'
  -------------------------
  Bands    |      supported: 'cdma-bc0-cellular-800, cdma-bc1-pcs-1900, cdma-bc10-secondary-800, cdma-bc15-aws, dcs, egsm, pcs, g850, u2100, u1900, u17iv, u850, u900, eutran-ii, eutran-iv, eutran-v, eutran-xiii, eutran-xvii, eutran-xxv'
           |        current: 'cdma-bc15-aws, dcs, egsm, pcs, g850, u2100, u1900, u850, u900, eutran-ii, eutran-iv, eutran-v, eutran-xvii'
  -------------------------
  IP       |      supported: 'ipv4, ipv6, ipv4v6'
  -------------------------
  3GPP     |           imei: '359225050108901'
           |  enabled locks: 'none'
           |    operator id: '310410'
           |  operator name: 'AT&T'
    
    '''

    # Parse text and save as out.json
    res = MMCLIParser.parse(text)
    MMCLIParser.save_json(res, 'out.json')

