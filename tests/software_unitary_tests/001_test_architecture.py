''' 
test to import required librairies
'''
try:
	import andi as ai
	print('- andi package successfully imported')
except :
	raise ValueError('Failed to import andi package.')

try:
	import bimms as bm
	print('- bimms package successfully imported')
except :
	raise ValueError('Failed to import bimms package.')

