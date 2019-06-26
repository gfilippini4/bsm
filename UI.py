from tkinter import ttk
from tkinter import *
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
from sqltest import prepared_statement, filter, prepared_query, tupleBreaker

class Insert(Frame):

	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack()
		self.make_widgets()

	def make_widgets(self):
		NameLab= Label(self, text='Insert Name')
		NameLab.grid(row=0,column=0)

		NickLab= Label(self, text='Insert Nick Name')
		NickLab.grid(row=1,column=0)

		SalLab= Label(self, text='Insert Salary')
		SalLab.grid(row=2,column=0)

		PosLab= Label(self, text='Insert Position')
		PosLab.grid(row=3,column=0)

		AgeLab= Label(self, text='Insert Age')
		AgeLab.grid(row=4,column=0)

		LocLab= Label(self, text='Insert Location')
		LocLab.grid(row=5,column=0)

		self.name = StringVar()
		NameEntry = Entry(self, width=50, textvariable=self.name)
		NameEntry.grid(row=0, column=1)

		self.nickname = StringVar()
		NickEntry = Entry(self, width=50, textvariable=self.nickname)
		NickEntry.grid(row=1,column=1)

		self.salary = StringVar()
		SalEntry = Entry(self, width=50, textvariable=self.salary)
		SalEntry.grid(row=2,column=1)

		self.position = StringVar()
		PosEntry = Entry(self, width=50, textvariable=self.position)
		PosEntry.grid(row=3,column=1)

		self.age = StringVar()
		AgeEntry = Entry(self, width=50, textvariable=self.age)
		AgeEntry.grid(row=4,column=1)

		self.location = StringVar()
		LocEntry = Entry(self, width=50, textvariable=self.location)
		LocEntry.grid(row=5,column=1)

		enterBut = Button(self, text='Insert', command=self.insert)
		enterBut.grid(row=6, columnspan=8)

	def insert(self):
		prepared_statement([self.name.get(),self.nickname.get(),self.salary.get(),self.position.get(),self.age.get(),self.location.get()])


class SelectShow(Frame):

	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack()
		self.make_widgets()
				

	def optMenu(self, kwargs):
		self.textBox.configure(state="normal")
		self.textBox.delete('1.0', END)
		val = ''
		if kwargs == 'All':
			val = tupleBreaker(filter('*'))
		else:
			val = tupleBreaker(filter(kwargs))
		
		self.textBox.insert(END, val)
		self.textBox.configure(state="disabled")
		
	
	def query(self):
		self.textBox.configure(state="normal")
		self.textBox.delete('1.0', END)
		val = prepared_query(self.sql.get())
		if type(val) != type('string'):
			try:
				val = tupleBreaker(val)
			except:
				val = val
		
		self.textBox.insert(END, val)
		self.textBox.configure(state="disabled")
		

	def make_widgets(self):
		sqlLabel = Label(self, text='SQL Query:')
		sqlLabel.grid(row=0,column=0)
		
		self.sql = StringVar()
		sqlEntry = Entry(self, width=50, textvariable=self.sql)
		sqlEntry.grid(row=0, column=1)
		
		sqlQueryButton = Button(self, text='Query', command=self.query)
		sqlQueryButton.grid(row=0,column=2)
		
		self.menuVar = StringVar()
		self.menuVar.set('Quick Filter')		
		menu = OptionMenu(self, self.menuVar, 'All', 'Name', 'Nickname', 'Salary', 'Position', 'Age', 'Location', command=self.optMenu)
		menu.grid(row=0,column=3)

		self.textBox = tkscrolled.ScrolledText(self, width=90, height=11, wrap='word')
		self.textBox.configure(state="disabled")
		self.textBox.grid(row=1,column=0,columnspan=4)
	
		powered = Label(self,text='Powered By Garrett Filippini')
		powered.grid(row=2,column=0)

def main():
	root = tk.Tk()
	root.geometry("750x255")	
	root.resizable(False, False)

	root.title("SQL Injector")
	
	nb = ttk.Notebook(root)

	# adding Frames as pages for the ttk.Notebook
	# first page, which would get widgets gridded into it
	page1 = Insert(nb)
	
	# second page
	page2 = SelectShow(nb)
	
	nb.add(page1, text='Insert')
	nb.add(page2, text='Select')
	
	nb.pack(expand=1, fill="both")

	root.mainloop()

if __name__ == "__main__":
	main()