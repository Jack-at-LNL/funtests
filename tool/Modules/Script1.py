	def	test_line_$XX(self):
		status = 0
		strCmdPv='$CMD_PV'
		strRdbkPv='$RDBK_PV'

		# if strCmdPV is not null create the cmdPv Object
		if len(strCmdPv) != 0 : cmdPv= PV(strCmdPv)

		# if strRdbkPv is not null create the rdbkPv Object
		if len(strRdbkPv) != 0 : rdbkPv= PV(strRdbkPv)

		bandWidth = $BANDWIDTH
		Severity = "$SEVERITY"

		# if strCmdPV is not null do caput action
		if len(strCmdPv)!= 0 : self.assertNotEqual(cmdPv.put('$CMD_VAL'),'None')

		# delay
		time.sleep($DELAY)

		# if strRdbkPv is not null do caget action	
		if len(strRdbkPv)!= 0 : self.assertNotEqual(rdbkPv.get(),'None')

		if(len(strRdbkPv) != 0) :
		# Check the threshold
			try :
  				if (rdbkPv.type == 'double' or rdbkPv.type == 'float' or rdbkPv.type == 'long' or rdbkPv.type == 'binary') :
    					self.assertFalse(rdbkPv.value < ($RDBK_VAL - ($RDBK_VAL * bandWidth)) or rdbkPv.value > ($RDBK_VAL + ($RDBK_VAL * bandWidth)))
  				elif rdbkPv.type == 'string' :
					self.assertEqual(rdbkPv.value, '$RDBK_VAL')
				elif rdbkPv.type == 'enum' :
					self.assertEqual(rdbkPv.enum_strs[rdbkPv.value], '$RDBK_VAL')
			except Exception :
				if Severity == 'Critical' :
					results_file.write('\n\nTest '+str($XX)+' => ERROR : '+'$FAIL_MESS')
					results_file.write('\n\n>>>>>>>>>>>>>>>>>>>> TEST FAIL ! .... see the previous error <<<<<<<<<<<<<<<<<<<<<')
					sys.exit("$FAIL_MESS")
				else :
					warnings.warn('$FAIL_MESS')
					results_file.write('\n\nTest '+str($XX)+' => WARNING : '+'$FAIL_MESS\n')
					status=-1
		# Success message
		if status == 0 :
			results_file.write('\n\nTest '+str($XX)+' => success : '+'$SUCC_MESS\n')
		
