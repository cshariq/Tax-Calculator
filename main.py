import tkinter as tk
from tkinter import messagebox

arg_names = [
    "Last Name", "First Name", "SIN # (9 numeric characters)",
    "Employment Income", "Employee’s CPP Deductions", "Employee's EI Premiums",
    "Income tax deducted", "Union Dues", "Charitable Donations",
    "RRSP Contributions"
]


class UserForm:

  def __init__(self, root):
    self.root = root
    self.root.title("User Information Form")
    self.root.geometry("500x500")
    self.canvas = tk.Canvas(root)
    self.scrollbar = tk.Scrollbar(root,
                                  orient="vertical",
                                  command=self.canvas.yview)
    self.scrollable_frame = tk.Frame(self.canvas)
    self.scrollable_frame.bind(
        "<Configure>",
        lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
    self.canvas.create_window((0, 0),
                              window=self.scrollable_frame,
                              anchor="nw")
    self.canvas.configure(yscrollcommand=self.scrollbar.set)
    self.fields = arg_names
    self.entries = {}
    self.create_input_fields()

  def create_input_fields(self):
    for widget in self.scrollable_frame.winfo_children():
      widget.destroy()
    for i, field in enumerate(self.fields):
      label = tk.Label(self.scrollable_frame, text=field)
      label.grid(row=i, column=0, sticky="w")
      entry = tk.Entry(self.scrollable_frame)
      entry.grid(row=i, column=1)
      self.entries[field] = entry
    self.submit_button = tk.Button(self.scrollable_frame,
                                   text="Submit",
                                   command=self.validate_and_submit)
    self.submit_button.grid(row=len(self.fields), column=1)
    self.canvas.pack(side="left", fill="both", expand=True)
    self.scrollbar.pack(side="right", fill="y")

  def get_form_data(self):
    form_data = {}
    for field in self.fields:
      form_data[field] = self.entries[field].get()
    return form_data

  def validate_and_submit(self):
    form_data = self.get_form_data()
    print(form_data)

    def validate(*args, **kwargs):
      for i, arg in enumerate(args):
        if arg_names[i] == 'Last Name':
          if not arg.strip():
            messagebox.showerror("Error", "Last Name cannot be empty.")
            return False
        elif arg_names[i] == 'First Name':
          pass
        elif arg_names[i] == 'SIN # (9 numeric characters)':
          try:
            sin = int(arg)
            if len(str(sin)) != 9:
              messagebox.showerror("Error",
                                   arg_names[i] + " must be a 9 integer value")
              return False
          except:
            messagebox.showerror("Error",
                                 arg_names[i] + " must be an integer value")
            return False
        elif arg_names[i] == 'Union Dues' or arg_names[
            i] == 'Charitable Donations' or arg_names[
                i] == 'RRSP Contributions':
          try:
            arg = float(arg)
          except:
            messagebox.showerror("Error",
                                 arg_names[i] + " must be a float value")
            return False
        else:
          try:
            arg = float(arg)
            if arg < 0:
              messagebox.showerror(
                  "Error", arg_names[i] + " cannot be empty or less than 0.")
              return False
          except:
            messagebox.showerror("Error",
                                 arg_names[i] + " must be a float value")
            return False
      return True

    if validate(*form_data.values()):

      def step2(line10100):
        # total income = employment income
        line15000 = line10100
        return line15000

      def step3(line15000, line20800, line21200):
        # the net income is total income minus RRSP deductions + union dues
        line23600 = (line15000 - (line20800 + line21200))
        return line23600

      def step4(line23600):
        # taxable income = net income
        line26000 = line23600
        return line26000

      def step5_parta(line26000):
        # Returns the federal tax on taxable income
        if line26000 <= 53359:
          return round(line26000 * 0.15, 2)
        elif line26000 <= 106717:
          return round((line26000 - 53359) * 0.205 + 8003.85, 2)
        elif line26000 <= 165430:
          return round((line26000 - 106717) * 0.26 + 18942.24, 2)
        elif line26000 <= 235675:
          return round((line26000 - 165430) * 0.29 + 34207.62, 2)
        else:
          return round((line26000 - 235675) * 0.33 + 54578.67, 2)

      def step5_partb(line23600, line30800, line10100, line31200,
                      donations_function):
        # Returns the Total federal non-refundable tax credits
        line83 = 0
        if line23600 <= 165430:
          line83 = 15000
        elif line23600 >= 235675:
          line83 = 13520
        else:
          line83 = round(1679 - (line23600 - 155625) / 66083 * 1679, 2)
          if line83 < 0:
            line83 = 0
          line83 = line83 + 12719
        return round((line83 + line30800 + line31200 +
                      (1368 if line10100 > 1368 else line10100)) * 0.15 +
                     donations_function, 2)

      #returns net federal tax (line 42000)
      def step5_partc(line35000, line75):
        #line75 is income tax, line35000 is total federal non-refundable tax credit
        line42000 = round(0 if line75 - line35000 < 0 else line75 - line35000,
                          2)
        #if line75 - line35000 is less than 0, then line42000 (net federal tax) = 0.
        #Otherwise it equals line75 - line35000
        return line42000

      #refund or balance owing (line 167)
      def step6(line26000, line30800, line31200, line42000, line43700, dBox_13,
                dBox_14):
        #ON_line8 is Ontario income tax
        if line26000 <= 49231:
          ON_line8 = round(line26000 * 0.0505, 2)
        elif line26000 <= 98463:
          ON_line8 = round((line26000 - 49231) * 0.0915 + 2486.17, 2)
        elif line26000 <= 150000:
          ON_line8 = round((line26000 - 98463) * 0.1116 + 6990.89, 2)
        elif line26000 <= 220000:
          ON_line8 = round((line26000 - 150000) * 0.1216 + 12742.42, 2)
        else:
          ON_line8 = round((line26000 - 220000) * 0.1316 + 21254.42, 2)

        ON_line25 = 11865 + (line30800 + line31200)

        #Ontario non-refundable tax credits (ON_line50)
        ON_line50 = round(
            (ON_line25 * 0.0505) + (dBox_13 * 0.0505) + (dBox_14 * 0.1116), 2)
        ON_line65 = 0 if ON_line8 - ON_line50 < 0 else ON_line8 - ON_line50

        if ON_line65 < 5315:
          ON_line68 = 0
        else:
          ON_line66 = round(ON_line65 * 0.2, 2)
          ON_line67 = round(0 if ON_line65 - 6802 < 0 else ON_line65 * 0.36, 2)
          ON_line68 = ON_line66 + ON_line67

        #Ontario tax without reductions (ON_line73)
        ON_line73 = ON_line65 + ON_line68

        #Ontario reductions
        ON_line80 = 0 if 548 - ON_line73 < 0 else 548 - ON_line73

        # ON_line89 is Ontario health premium
        if line26000 <= 20000:
          ON_line89 = 0
        elif line26000 <= 25000:
          ON_line89 = round((line26000 - 20000) * 0.06, 2)
        elif line26000 <= 36000:
          ON_line89 = 300
        elif line26000 <= 38500:
          ON_line89 = round((line26000 - 36000) * 0.06 + 300, 2)
        elif line26000 <= 48000:
          ON_line89 = 450
        elif line26000 <= 48600:
          ON_line89 = round((line26000 - 48000) / 4 + 450, 2)
        elif line26000 <= 72000:
          ON_line89 = 600
        elif line26000 <= 72600:
          ON_line89 = round((line26000 - 72000) / 4 + 600, 2)
        elif line26000 <= 200000:
          ON_line89 = 750
        elif line26000 <= 200600:
          ON_line89 = round((line26000 - 200000) / 4 + 750, 2)
        else:
          ON_line89 = 900

        #total ontario tax
        line42800 = (ON_line73 - ON_line80) + ON_line89
        #total payable
        line43500 = line42000 + line42800

        #refund or balance owing
        line167 = round(line43500 - line43700,2)

        line48400 = line167
        return line48400, line43500, line42800 

      # Donations
      def donations(charitable_donations, line32900, line33300, line33400,
                    line26000, line23600, line33700, line33900):
        # total_d = total eligible amount of charitable donations
        total_d = charitable_donations + line32900 + line33300 + line33400  # <-- D for Donations

        # total donations limit is wichever is less between
        # line23600(net income) and line 8 on the Donations and Gifts Form
        total_d_limit = round(
            min(line23600,
                (line23600 * 0.75 + (line33700 + line33900) * 0.25)), 2)

        dBox_13 = min(min(total_d, total_d_limit), 200)
        dBox_14 = min(total_d, total_d_limit) - dBox_13
        dBox_16 = dBox_14
        if dBox_16 < 0:
          dBox_16 = 0

        dBox_19 = line26000 - 235675  # dBox_17 is the taxable income, line 26000, from step 4 on Income Tax and Benefit Return
        if dBox_19 < 0:
          dBox_19 = 0

        dBox_23 = round(
            min(dBox_16, dBox_19) * 0.33 + (dBox_14 - dBox_19) * 0.29 +
            dBox_13 * 0.15, 2)

        return dBox_13, dBox_14, dBox_23  #  <-- this goes into line34900

      def getReturnValues(lastn, firstn, sin, employment_income,
                          cpp_deductions, ei_premiums, income_tax, union_dues,
                          charitable_donations, rrsp_contribution):
        lastName, firstName = lastn, firstn
        SIN = sin
        Total_income = step2(line10100=employment_income)
        Net_income = step3(line15000=Total_income,
                           line20800=rrsp_contribution,
                           line21200=union_dues)
        Taxable_income = step4(line23600=Net_income)
        federal_tax_on_taxable_income = step5_parta(line26000=Taxable_income)
        #TFNRTC = Total Federal Non-Refundable Tax Credits
        TFNRTC = step5_partb(line23600=Net_income,
                             line30800=cpp_deductions,
                             line10100=employment_income,
                             line31200=ei_premiums,
                             donations_function=donations(
                                 charitable_donations=charitable_donations,
                                 line32900=0,
                                 line33300=0,
                                 line33400=0,
                                 line26000=Taxable_income,
                                 line23600=Net_income,
                                 line33700=0,
                                 line33900=0)[2])
        Net_Federal_Tax = step5_partc(
            line35000=TFNRTC, line75=step5_parta(line26000=Taxable_income))
        line48400, line43500, line42800 = step6(
            line26000=Taxable_income,
            line30800=cpp_deductions,
            line31200=ei_premiums,
            line42000=Net_Federal_Tax,
            line43700=income_tax,
            dBox_13=donations(charitable_donations=charitable_donations,
                              line32900=0,
                              line33300=0,
                              line33400=0,
                              line26000=Taxable_income,
                              line23600=Net_income,
                              line33700=0,
                              line33900=0)[0],
            dBox_14=donations(charitable_donations=charitable_donations,
                              line32900=0,
                              line33300=0,
                              line33400=0,
                              line26000=Taxable_income,
                              line23600=Net_income,
                              line33700=0,
                              line33900=0)[1])
        donations_and_gifts = donations(
            charitable_donations=charitable_donations,
            line32900=0,
            line33300=0,
            line33400=0,
            line26000=Taxable_income,
            line23600=Net_income,
            line33700=0,
            line33900=0)[2]
        Ontario_Tax = line42800
        Total_Tax_Payable = line43500
        Total_Tax_Credits = income_tax
        Refund_or_Balace_Owning = line48400

        return [
            lastName, firstName, SIN, Total_income, Net_income, Taxable_income,
            federal_tax_on_taxable_income, TFNRTC, Net_Federal_Tax,
            Ontario_Tax, Total_Tax_Payable, Total_Tax_Credits,
            Refund_or_Balace_Owning, donations_and_gifts
        ]

      for widget in self.scrollable_frame.winfo_children():
        widget.destroy()
      labels = [f"{field}: {value}" for field, value in form_data.items()]
      outputArray = getReturnValues(
          lastn=form_data['Last Name'],
          firstn=form_data['First Name'],
          sin=form_data['SIN # (9 numeric characters)'],
          employment_income=float(form_data['Employment Income']),
          cpp_deductions=float(form_data['Employee’s CPP Deductions']),
          ei_premiums=float(form_data["Employee's EI Premiums"]),
          income_tax=float(form_data['Income tax deducted']),
          union_dues=float(form_data['Union Dues']),
          charitable_donations=float(form_data['Charitable Donations']),
          rrsp_contribution=float(form_data['RRSP Contributions']))
      for i, item in enumerate(outputArray):
        label = tk.Label(self.scrollable_frame, text=item)
        label.grid(row=i, column=0, sticky="w")
      # for i, label_text in enumerate(labels):
      #   label = tk.Label(self.scrollable_frame, text=label_text)
      #   label.grid(row=i, column=0, sticky="w")
      back_button = tk.Button(self.scrollable_frame,
                              text="Back",
                              command=self.create_input_fields)
      back_button.grid(row=len(labels), column=0)

      outputArray = getReturnValues(
          lastn=form_data['Last Name'],
          firstn=form_data['First Name'],
          sin=form_data['SIN # (9 numeric characters)'],
          employment_income=float(form_data['Employment Income']),
          cpp_deductions=float(form_data['Employee’s CPP Deductions']),
          ei_premiums=float(form_data["Employee's EI Premiums"]),
          income_tax=float(form_data['Income tax deducted']),
          union_dues=float(form_data['Union Dues']),
          charitable_donations=float(form_data['Charitable Donations']),
          rrsp_contribution=float(form_data['RRSP Contributions']))
      print(outputArray)


if __name__ == "__main__":
  root = tk.Tk()
  app = UserForm(root)
  root.mainloop()
#72950.49, 3754.45, 1002.45, 13418.45, 1938.69, 52, 2741.89
#198455.79, 3754.45, 1002.45, 63451.10, 0?, 225, 5200
  #issues with TFNRTC for this one