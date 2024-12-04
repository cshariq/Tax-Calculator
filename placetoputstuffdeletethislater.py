def step5_partb2(line23600, year_born, box18, box55, employment_income,
                 other_employment_income, employment_CPP_deductions):
  line84 = step5_partb1(line23600, year_born)

  line1 = employment_income
  line2 = other_employment_income

  line85 = employment_CPP_deductions

  line85 = box18 + box55
  line86 = 0
  line87 = 0
  line88 = 0
  line89 = 0
  line90 = 0
  line91 = 1368 if line1 + line2 > 1386 else line1 + line2
  line92 = 0
  line93 = 0
  line94 = 0
  line95 = 0

  line96 = line85 + line86 + line87 + line88 + line89 + line90 + line91 + line92 + line93 + line94 + line95

  line96 = 0
  line97 = 0

  line98 = line84 + line96 + line97
  line99 = 0
  line100 = 0

  line101 = line98 + line99 + line100
  line102 = 0
  line103 = 0
  line104 = 0
  line105 = 0

  line106 = line101 + line102 + line103 + line104 + line105

  line107 = medical_expenses

  line108 = line23600 * 0.03

  line109 = line108 if line108 > 2635 else 2635
  line110 = 0 if line107 - line109 > 0 else line107 - line109

  line111 = medical_expenses  #Medical expenses for other dependants use federal worksheet

  line112 = line110 + line111
  line113 = line106 + line112
  line114 = 0.15

  line115 = line113 * line114
  line116 = donations()  #Donations and Gifts Completed in Schedule 9

  line117 = line115  #line116 + line115

  return line117


def output(lastName, firstName, sinNumber, line15000, line20800, line10100,
           line23500, line21200, line26000, line30800, line31200, line35000,
           line73, line42800, line42000, line43700, dBox_13, dBox_14):

  # This function is broken please don't use it

  line23600 = step3(0, line15000, line20800, line21200, line23500)

  Total_income = step2(line15000, line10100)
  Net_income = line23600
  Taxable_income = step4(line26000, line23600)
  TFNRTC = step5_partb(line23600, line30800, line10100, line31200)
  Net_Federal_Tax = step5_partc(line35000, line73)
  Ontario_Tax = line42800
  Total_Tax_Payable = step6(line26000, line30800, line31200, line42000,
                            line43700, dBox_13, dBox_14)



def donations(charitable_donations, line32900, line33300, line33400, line26000, line23600, line33700, line33900):
  # total_d = total eligible amount of charitable donations
  total_d = charitable_donations + line32900 + line33300 + line33400  # <-- D for Donations
  dBox_6 = line23600 * 0.75  # line23600 = net income from step 3 on Income Tax and Benefit Return
  dBox_7 = (line33700 + line33900) * 0.25
  dBox_8 = dBox_6 + dBox_7

  # total donations limit is wichever is less between
  # line23600 and line 8 on the Donations and Gifts Form
  total_d_limit = min(line23600, dBox_8)

  dBox_10 = min(total_d, total_d_limit)  # dBox_10 = line34000
  dBox_12 = dBox_10
  dBox_13 = min(dBox_12, 200)
  dBox_14 = dBox_12 - dBox_13
  dBox_16 = dBox_14
  if dBox_16 < 0:
    dBox_16 = 0

  dBox_19 = line26000 - 235675  # dBox_17 is the taxable income, line 26000, from step 4 on Income Tax and Benefit Return
  if dBox_19 < 0:
    dBox_19 = 0