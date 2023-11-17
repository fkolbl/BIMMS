#! /usr/bin/env python3
# coding: utf-8

import os
import sys
import traceback
import subprocess
import re
import shutil
import argparse
import cmd

## ARGUMENT PARSER ##
parser = argparse.ArgumentParser(description="NeuRon Virtualizer automated test module")
parser.add_argument("-H", "--Hardware", action="store_true", dest="H_TEST",help="")
parser.add_argument("-t", "--target", dest="TARGET", type=int, nargs="+" ,default=0, help="The number of the tests to simulate")
parser.add_argument("-l", "--list", dest="LIST_TEST",type=int, nargs="?",default=-1, help="Print the name of all unitary tests")

args = parser.parse_args()
if args.H_TEST:
    unit_test_folder = './hardware_unitary_tests/'
else:
    unit_test_folder = './software_unitary_tests/'

all_tests = sorted(os.listdir(unit_test_folder), reverse=True)
all_tests.reverse()
unit_test_results = './unitary_tests/figures/'
digits = [str(k) for k in range(10)]
all_tests [:] = (value for value in all_tests if value[0] in digits)


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
all_test = True

if not args.LIST_TEST == -1:
    if args.LIST_TEST is None:
        N_col = 2
    else:
        N_col = int(args.LIST_TEST)
    tests = []
    tests[:] = all_tests[:]
    i=0
    i_break = 5000
    while i < len(tests) and i_break > 0:
        i_break -= 1
        test = tests[i]
        if ".py" in test:
            tests[i] = test[:3]+ "-" +test[4:-3]
            i += 1
    cli = cmd.Cmd()
    cli.columnize(tests, displaywidth=N_col*47)
    all_test= False


python_cmd = 'python3 '
success_flag = True
test_nb = 0
failed_test = []


if args.TARGET:
    for argt in args.TARGET:
        target_script_key = f"{argt:03}"

        for test in all_tests:
            if str(target_script_key) in test:
                print(test)
                test_out = os.system(python_cmd+unit_test_folder+test)
                print("test exited with value ", test_out)
                break
    all_test = False


if all_test:
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
