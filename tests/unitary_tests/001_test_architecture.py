''' 
test to import required librairies
'''


try:
	import dwfconstants
	print('- Waveform SDK detected')
except :
	raise ValueError('Please install Waveform SDK (https://reference.digilentinc.com/software/waveforms/waveforms-sdk/start)')

try:
	import Analysis_Instrument as ai
	print('- Analysis_Instrument Lib successfully imported')
except :
	raise ValueError('Failed to import Analysis_Instrument lib. Make sure it is added to the python path.')

try:
	import BIMMS as bm
	print('- BIMMS Lib successfully imported')
except :
	raise ValueError('Failed to import BIMMS lib. Make sure it is added to the python path.')

try:
	import BIMMS_constants as cst
	print('- BIMMS constants Lib successfully imported')
except :
	raise ValueError('Failed to import BIMMS constants lib. Make sure it is added to the python path.')

