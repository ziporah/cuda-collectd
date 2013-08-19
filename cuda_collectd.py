import collectd
import subprocess
import xml.etree.ElementTree as ET

def read(data=None):
        vl = collectd.Values(type='gauge')
        vl.plugin = 'cuda'

	signal.signal(SIGCHLD, signal.SIG_DFL)
        out = subprocess.Popen(['nvidia-smi', '-q', '-x', '-d', 'MEMORY,UTILIZATION,POWER' ], stdout=subprocess.PIPE).communicate()[0]
        root = ET.fromstring(out)

        for gpu in root.getiterator('gpu'):
                vl.plugin_instance = 'cuda-%s' % (gpu.attrib['id'])

#                vl.dispatch(type='fanspeed',
#                            values=[float(gpu.find('fan_speed').text.split()[0])])

#                vl.dispatch(type='temperature',
#                            values=[float(gpu.find('temperature/gpu_temp').text.split()[0])])

                vl.dispatch(type='memory', type_instance='used',
                            values=[1e6 * float(gpu.find('memory_usage/used').text.split()[0])])

                vl.dispatch(type='memory', type_instance='total',
                            values=[1e6 * float(gpu.find('memory_usage/total').text.split()[0])])

                vl.dispatch(type='percent', type_instance='gpu_util',
                            values=[float(gpu.find('utilization/gpu_util').text.split()[0])])
                vl.dispatch(type='power', type_instance='draw',
                            values=[float(gpu.find('power_readings/power_draw').text.split()[0])])

collectd.register_read(read)

