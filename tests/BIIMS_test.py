import os
import sys
import traceback
import subprocess
import re
import shutil

unit_test_folder = './unitary_tests/'
all_tests = sorted(os.listdir(unit_test_folder), reverse=True)
all_tests.reverse()
unit_test_results = './unitary_tests/figures/'

###################################
## clean the test/figures folder ##
###################################
#old_results = os.listdir(unit_test_results)
#for old_file in old_results:
#	os.remove(unit_test_results+old_file)
if os.path.exists(unit_test_results):
	shutil.rmtree(unit_test_results)

if not os.path.exists(unit_test_results):
	os.makedirs(unit_test_results)


################
## TEST BIMS ##
################
	
python_cmd = 'python3 '
success_flag = True
test_nb = 0
failed_test = []

for test in all_tests:
	if '.py' in test:
		test_nb += 1
		print(test)
		test_out = os.system(python_cmd+unit_test_folder+test)
		if test_out != 0:
			success_flag = False
			failed_test.append(test)

if success_flag == True:
	print('--- All tests passed without errors, check that all tests are true')
else:
	print('--- Error in tests, please consider reported errors before measurements')
	print('--- list of failed tests : ',failed_test)
