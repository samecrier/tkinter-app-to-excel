import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import openpyxl as op
import csv

path_1 = ''
path_2 = ''


@staticmethod
def keypress(event):
	if event.keycode == 86:
		event.widget.event_generate('<<Paste>>')
	elif event.keycode == 67:
		event.widget.event_generate('<<Copy>>')
	elif event.keycode == 88:
		event.widget.event_generate('<<Cut>>')
	elif event.keycode == 65:
		event.widget.event_generate('<<SelectAll>>')


win = tk.Tk()
win.geometry('1300x700+50+50')
win.title('Программа')
win.bind("<Control-KeyPress>", keypress)


def get_info():
	print(f'Номер лабораторного журнала - {nb_lab_journal.get()}')
	print(f'Регистрационный номер пробы - {rg_nb_sample.get()}')
	print(f'Наименование пробы(образца) - {name_sample.get()}')
	print(f'ФИО специалиста ответственного за пробоподготовку - {nm_sample_executor.get()}')
	print(f'Примечания пробоподготовки - {nt_sample.get()}')
	print(f'Примечания регистрационного журнала - {nt_register.get()}')
	print(f'Укажите перечень показателей через запятую - {ls_indicators.get()}')
	print(f'Укажите реквизиты НД для проведения пробоподготовки - {det_nd_prep_sample.get()}')
	print(f'Укажите реквизиты НД на метод исследования - {det_nd_research_sample.get()}')
	print(f'ФИО специалиста проводившего исследование - {sp_did_research.get()}')
	print(f'ФИО ответственного исполнителя - {rsp_executor.get()}')
	print(f'Дата начала исследования - {dt_st_research.get()}')
	print(f'Дата начала пробоподготовки - {dt_st_sample_prep.get()}')
	print(f'Дата отбора пробы (образца) - {dt_st_sampling.get()}')
	print(f'Дата поступления - {dt_get_receipt.get()}')
	print(f'Дата окончания исследования - {dt_fn_research.get()}')
	print(f'Дата окончания пробоподготовки - {dt_fn_sample_prep.get()}')
	print(f'Дата утилизации пробы/сведения о консервации - {dt_disposal.get()}')
	print(f'Дата выписки листа протокола - {dt_issue_protocol.get()}')
	print(f'Этапы пробоподготовки - {steps_sample.get()}')
	print(f'Этапы исследования - {stp_research.get()}')
	print('_________________________________________________')


def write_history(row):
	with open('datas/query_history.csv', 'a', newline='', encoding='utf-8') as f:
		writer = csv.writer(f, delimiter='&')
		writer.writerow(row)


def excel_func():
	if rg_nb_sample.get() == '':
		messagebox.showerror('Ошибка', 'Введите регистрационный номер пробы для отправки')
		return
	dict_keys = []
	with open('datas/query_history.csv', 'r', encoding='utf-8', newline='') as f:
		csv_reader = csv.reader(f, delimiter='&')
		for row in csv_reader:
			dict_keys.append(row[1])
	if rg_nb_sample.get() in dict_keys:
		messagebox.showerror('Ошибка',
		                     'Данный регистрационный номер уже находится в базе. Удалите запись из базы или попробуйте ввести другой номер.')
		return
	if path_1 == '':
		path_sample_file = 'C:/Users/saycry/PycharmProjects/gui_to_excel/docs/test_file_sample.xlsx'
	else:
		path_sample_file = path_1
	if path_2 == '':
		path_register_file = 'C:/Users/saycry/PycharmProjects/gui_to_excel/docs/test_file_register.xlsx'
	else:
		path_register_file = path_2

	book_1 = op.load_workbook(filename=path_sample_file)
	sheet_1 = book_1.active
	book_2 = op.load_workbook(filename=path_register_file)
	sheet_2 = book_2.active

	print(ls_indicators.get(), type(ls_indicators.get()))
	if ('обнаружена' or 'не обнаружена') in ls_indicators.get():
		ls_indicators_text = ls_indicators.get()
		print('мы тут')
	else:
		ls_indicators_text = ls_indicators.get() + ' ' + default_indicator
		print('мы здеся')

	sample_file = [
		nb_lab_journal.get(),
		rg_nb_sample.get(),
		name_sample.get(),
		det_nd_prep_sample.get(),
		steps_sample.get(),
		dt_st_sample_prep.get(),
		dt_fn_sample_prep.get(),
		nm_sample_executor.get(),
		det_nd_research_sample.get(),
		stp_research.get(),
		dt_st_research.get(),
		dt_fn_research.get(),
		ls_indicators_text,
		sp_did_research.get(),
		nt_sample.get()
	]
	register_file = [
		nb_lab_journal.get(),
		rg_nb_sample.get(),
		name_sample.get(),
		dt_st_sampling.get(),
		dt_get_receipt.get(),
		dt_st_research.get(),
		ls_indicators.get(),
		dt_fn_research.get(),
		dt_disposal.get(),
		dt_issue_protocol.get(),
		rsp_executor.get(),
		nt_register.get()
	]

	sheet_1.append(sample_file)
	book_1.save(filename=path_sample_file)
	path = os.path.realpath(path_sample_file)

	sheet_2.append(register_file)
	book_2.save(filename=path_register_file)
	path = os.path.realpath(path_register_file)

	write_history(
		[
			nb_lab_journal.get(),
			rg_nb_sample.get(),
			name_sample.get(),
			nm_sample_executor.get(),
			nt_sample.get(),
			nt_register.get(),
			ls_indicators_text,
			det_nd_prep_sample.get(),
			det_nd_research_sample.get(),
			sp_did_research.get(),
			rsp_executor.get(),
			dt_st_research.get(),
			dt_st_sample_prep.get(),
			dt_st_sampling.get(),
			dt_get_receipt.get(),
			dt_fn_research.get(),
			dt_fn_sample_prep.get(),
			dt_disposal.get(),
			dt_issue_protocol.get(),
			steps_sample.get(),
			stp_research.get(),
		]
	)

	if op_xl_button_value.get() == 'No':
		print('Сохранение в эксель без открытия')
		return
	os.startfile(path_sample_file)
	os.startfile(path_register_file)
	print('Сохранение в эксель с открытием ')


def read_csv():
	with open('datas/did_research.csv', 'r', encoding='utf-8', newline='') as f:
		csv_reader = csv.reader(f, delimiter=';')
		for row in csv_reader:
			return row


def write_csv(row):
	row = sorted(row)
	with open('datas/did_research.csv', 'w', newline='', encoding='utf-8') as f:
		writer = csv.writer(f, delimiter=';')
		writer.writerow(row)


def get_file_1():
	global path_1
	path_1 = filedialog.askopenfilename()
	tk.Label(win, text=path_1).grid(row=21, column=1)
	print(path_1)


def get_file_2():
	global path_2
	path_2 = filedialog.askopenfilename()
	tk.Label(win, text=path_2).grid(row=22, column=1)
	print(path_2)


def repeat_for_nd():
	if repeat_for_nd_value.get() == 'Yes':
		det_nd_research_sample.insert(0, det_nd_prep_sample.get())
	if repeat_for_nd_value.get() == 'No':
		det_nd_research_sample.delete(0, tk.END)


def repeat_for_sp():
	if repeat_for_sp_value.get() == 'Yes':
		rsp_executor.insert(0, sp_did_research.get())
	if repeat_for_sp_value.get() == 'No':
		rsp_executor.delete(0, tk.END)


def repeat_for_dt_st_1():
	if dt_st_value_1.get() == 'Yes':
		dt_st_sample_prep.insert(0, dt_st_research.get())
	if dt_st_value_1.get() == 'No':
		dt_st_sample_prep.delete(0, tk.END)
print('hello world')

def repeat_for_dt_st_2():
	if dt_st_value_2.get() == 'Yes':
		dt_st_sampling.insert(0, dt_st_research.get())
	if dt_st_value_2.get() == 'No':
		dt_st_sampling.delete(0, tk.END)


def repeat_for_dt_st_3():
	if dt_st_value_3.get() == 'Yes':
		dt_get_receipt.insert(0, dt_st_research.get())
	if dt_st_value_3.get() == 'No':
		dt_get_receipt.delete(0, tk.END)


def repeat_for_dt_fn_1():
	if dt_fn_value_1.get() == 'Yes':
		dt_fn_sample_prep.insert(0, dt_fn_research.get())
	if dt_fn_value_1.get() == 'No':
		dt_fn_sample_prep.delete(0, tk.END)


def repeat_for_dt_fn_2():
	if dt_fn_value_2.get() == 'Yes':
		dt_disposal.insert(0, dt_fn_research.get())
	if dt_fn_value_2.get() == 'No':
		dt_disposal.delete(0, tk.END)


def repeat_for_dt_fn_3():
	if dt_fn_value_3.get() == 'Yes':
		dt_issue_protocol.insert(0, dt_fn_research.get())
	if dt_fn_value_3.get() == 'No':
		dt_issue_protocol.delete(0, tk.END)


def repeat_for_stp():
	if repeat_for_stp_value.get() == 'Yes':
		stp_research.insert(0, steps_sample.get())
	if repeat_for_stp_value.get() == 'No':
		stp_research.delete(0, tk.END)


def find_not_find(eventObject):
	global default_indicator
	default_indicator = eventObject.widget.get()
	print(default_indicator)


def start_window_0():
	def delete():
		selection = employee_listbox.curselection()
		name_of_selection = employee_listbox.get(int(employee_listbox.curselection()[0]))
		if name_of_selection == sp_did_research.get():
			sp_did_research.delete(0, tk.END)
		employees.remove(name_of_selection)
		write_csv(employees)
		# мы можем получить удаляемый элемент по индексу
		# selected_language = employee_listbox.get(selection[0])
		employee_listbox.delete(selection[0])

	# добавление нового элемента
	def add():
		new_employee = employee_entry.get()
		write_csv(employees + [new_employee])
		employee_listbox.insert(0, new_employee)

	def show_print(evt):
		w = evt.widget
		value = w.get(int(w.curselection()[0]))
		print(value)

	def add_to_enter_box():
		sp_did_research.delete(0, tk.END)
		selection = employee_listbox.curselection()
		name_of_selection = employee_listbox.get(int(employee_listbox.curselection()[0]))
		sp_did_research.insert(0, name_of_selection)
		new_window_0.destroy()

	new_window_0 = tk.Toplevel(win)
	new_window_0.grab_set()  # нельзя нажимать в других окнах
	new_window_0.title('Окно 1')
	new_window_0.geometry('400x300+1800+350')
	new_window_0.protocol('WM_DELETE_WINDOW')  # закрытие приложения
	new_window_0.wm_attributes("-topmost", 1)  # чтобы повешать поверх все окон, но работает и без
	# текстовое поле и кнопка для добавления в список
	employee_entry = ttk.Entry(new_window_0)
	employee_entry.grid(column=0, row=0, padx=6, pady=6, sticky='ew')
	ttk.Button(new_window_0, text="Добавить специалиста", command=add).grid(column=1, row=0, padx=6, pady=6)
	employees = read_csv()
	employees_var = tk.Variable(new_window_0, value=employees)
	employee_listbox = tk.Listbox(new_window_0, listvariable=employees_var)
	employee_listbox.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

	ttk.Button(new_window_0, text="Применить", command=add_to_enter_box).grid(row=2, column=0, padx=5, pady=5)
	ttk.Button(new_window_0, text="Удалить", command=delete).grid(row=2, column=1, padx=5, pady=5)


def on_closing_0(this_window):
	if messagebox.askokcancel('Выход из приложения', 'Хотите ли вы выйти из приложения?'):
		this_window.destroy()


def history_window():
	history_window_0 = tk.Toplevel(win)  # нельзя нажимать в других окнах
	history_window_0.title('Окно 1')
	history_window_0.geometry('1000x500+1300+350')
	history_window_0.protocol('WM_DELETE_WINDOW')  # закрытие приложения

	def dict_from_csv():
		csv_dict = {}
		with open('datas/query_history.csv', 'r', encoding='utf-8', newline='') as f:
			csv_reader = csv.reader(f, delimiter='&')
			for row in csv_reader:
				dict_key = row[1]
				dict_values = row
				csv_dict[dict_key] = dict_values
		return csv_dict

	def choose_code(evt):
		t0['state'] = tk.NORMAL
		t0.delete(0.0, tk.END)
		w = evt.widget
		value = w.get(int(w.curselection()[0]))
		counter = 0
		for i, row in enumerate(history_dict[value]):
			t0.insert(tk.INSERT, infos_for_history[i] + ' - ' + row + '\n')
		t0['state'] = tk.DISABLED

	def confirm_to_main():
		variables_for_row = [nb_lab_journal, rg_nb_sample, name_sample, nm_sample_executor, nt_sample, nt_register,
		                     ls_indicators, det_nd_prep_sample, det_nd_research_sample, sp_did_research, rsp_executor,
		                     dt_st_research, dt_st_sample_prep, dt_st_sampling, dt_get_receipt, dt_fn_research,
		                     dt_fn_sample_prep, dt_disposal, dt_issue_protocol, steps_sample, stp_research, ]

		for i in range(len(variables_for_row)):
			variables_for_row[i].delete(0, tk.END)

		selection = l0.curselection()
		value = l0.get(int(l0.curselection()[0]))
		for i in range(len(variables_for_row)):
			variables_for_row[i].insert(0, history_dict[value][i])

	infos_for_history = ['Номер лабораторного журнала', 'Регистрационный номер пробы', 'Наименование пробы(образца)',
	                     'ФИО специалиста ответственного за пробоподготовку', 'Примечания пробоподготовки',
	                     'Примечания регистрационного журнала', 'Укажите перечень показателей через запятую',
	                     'Укажите реквизиты НД для проведения пробоподготовки',
	                     'Укажите реквизиты НД на метод исследования', 'ФИО специалиста проводившего исследование',
	                     'ФИО ответственного исполнителя', 'Дата начала исследования', 'Дата начала пробоподготовки',
	                     'Дата отбора пробы (образца)', 'Дата поступления', 'Дата окончания исследования',
	                     'Дата окончания пробоподготовки', 'Дата утилизации пробы/сведения о консервации',
	                     'Дата выписки листа протокола', 'Этапы пробоподготовки', 'Этапы исследования']

	t0 = tk.Text(history_window_0, width=100, state=tk.DISABLED)
	t0.grid(row=0, column=1, padx=5)

	history_dict = dict_from_csv()

	history_samples = sorted(dict_from_csv(), reverse=False)

	list_var = tk.Variable(value=history_samples)
	l0 = tk.Listbox(history_window_0, listvariable=list_var,
	                exportselection=False)  # exportselection отвечает за то, чтобы при работе с виджетом можно было работать с другим без вреда для первого и второго
	l0.grid(row=0, column=0)
	l0.bind('<<ListboxSelect>>', choose_code)

	b1 = tk.Button(history_window_0, text='Применить', font=('Arial', '14'), command=confirm_to_main)
	b1.grid(row=1, column=1, pady=20)


def clear_all_information():
	variables_for_row = [nb_lab_journal, rg_nb_sample, name_sample, nm_sample_executor, nt_sample, nt_register,
	                     ls_indicators, det_nd_prep_sample, det_nd_research_sample, sp_did_research, rsp_executor,
	                     dt_st_research, dt_st_sample_prep, dt_st_sampling, dt_get_receipt, dt_fn_research,
	                     dt_fn_sample_prep, dt_disposal, dt_issue_protocol, steps_sample, stp_research, ]
	for i in range(len(variables_for_row)):
		variables_for_row[i].delete(0, tk.END)


# двойное
tk.Label(win, text='Номер лабораторного журнала').grid(row=0, column=0)
nb_lab_journal = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
nb_lab_journal.grid(row=0, column=1)

tk.Button(win, text='История', command=history_window).grid(row=0, column=3)

tk.Button(win, text='Очистить все', command=clear_all_information).grid(row=0, column=2, stick='w', padx=25)

# двойное
tk.Label(win, text='Регистрационный номер пробы').grid(row=1, column=0)
rg_nb_sample = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
rg_nb_sample.grid(row=1, column=1)

# двойное
tk.Label(win, text='Наименование пробы(образца)').grid(row=2, column=0)
name_sample = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
name_sample.grid(row=2, column=1)

# уникальное
tk.Label(win, text='ФИО специалиста ответственного за пробоподготовку').grid(row=3, column=0)
nm_sample_executor = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
nm_sample_executor.grid(row=3, column=1)

# уникальное
tk.Label(win, text='Примечания пробоподготовки').grid(row=4, column=0)
nt_sample = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
nt_sample.grid(row=4, column=1)

# уникальное
tk.Label(win, text='Примечания регистрационного журнала').grid(row=5, column=0)
nt_register = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
nt_register.grid(row=5, column=1)

# Перечень показателей
default_indicator = 'не обнаружена'
list_of_indicators = ('не обнаружена', 'обнаружена')
tk.Label(win, text='Укажите перечень показателей через запятую').grid(row=6, column=0)
ls_indicators = tk.Entry(win, font=('Arial', 10), width=25)
ls_indicators.grid(row=6, column=1)
combo_indicators = ttk.Combobox(win, values=list_of_indicators)
combo_indicators.current(0)
combo_indicators.grid(row=6, column=2, stick='w')
combo_indicators.bind("<<ComboboxSelected>>", find_not_find)

# Реквизиты НД для проведения пробоподготовки и на метод исследования
repeat_for_nd_value = tk.StringVar()
repeat_for_nd_value.set('No')
tk.Label(win, text='Укажите реквизиты НД для проведения пробоподготовки').grid(row=7, column=0)
det_nd_prep_sample = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
det_nd_prep_sample.grid(row=7, column=1)
nd_check_button = tk.Checkbutton(win, text='пов. для рекв. методов исследования', command=repeat_for_nd,
                                 variable=repeat_for_nd_value, offvalue='No', onvalue='Yes')
nd_check_button.grid(row=7, column=2)
tk.Label(win, text='Укажите реквизиты НД на метод исследования').grid(row=8, column=0)
det_nd_research_sample = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
det_nd_research_sample.grid(row=8, column=1)

# ФИО специалиста и ответственный исполнитель
repeat_for_sp_value = tk.StringVar()
repeat_for_sp_value.set('No')
tk.Label(win, text='ФИО специалиста проводившего исследование').grid(row=9, column=0)
sp_did_research = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
sp_did_research.grid(row=9, column=1)
tk.Button(win, text='Выбрать специалистиа', command=start_window_0).grid(row=9, column=2)
sp_check_button = tk.Checkbutton(win, text='пов. для ответственного исполнителя', command=repeat_for_sp,
                                 variable=repeat_for_sp_value, offvalue='No', onvalue='Yes')
sp_check_button.grid(row=9, column=3)
tk.Label(win, text='ФИО ответственного исполнителя').grid(row=10, column=0)
rsp_executor = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
rsp_executor.grid(row=10, column=1)

# Даты начала

# двойное
tk.Label(win, text='Дата начала исследования').grid(row=11, column=0)
dt_st_research = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
dt_st_research.grid(row=11, column=1)

dt_st_value_1 = tk.StringVar()
dt_st_value_2 = tk.StringVar()
dt_st_value_3 = tk.StringVar()
dt_st_value_1.set('No')
dt_st_value_2.set('No')
dt_st_value_3.set('No')
dt_st_check_button_1 = tk.Checkbutton(win, text='пов. начало пробоподготовки', command=repeat_for_dt_st_1,
                                      variable=dt_st_value_1, offvalue='No', onvalue='Yes')
dt_st_check_button_1.grid(row=11, column=2, stick='w')
dt_st_check_button_2 = tk.Checkbutton(win, text='пов. дата отбора пробы (образца)', command=repeat_for_dt_st_2,
                                      variable=dt_st_value_2, offvalue='No', onvalue='Yes')
dt_st_check_button_2.grid(row=11, column=3, stick='w')
dt_st_check_button_3 = tk.Checkbutton(win, text='пов. дата поступления', command=repeat_for_dt_st_3,
                                      variable=dt_st_value_3, offvalue='No', onvalue='Yes')
dt_st_check_button_3.grid(row=11, column=4, stick='w')

tk.Label(win, text='Дата начала пробоподготовки').grid(row=12, column=0)
dt_st_sample_prep = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
dt_st_sample_prep.grid(row=12, column=1)

tk.Label(win, text='Дата отбора пробы (образца)').grid(row=13, column=0)
dt_st_sampling = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
dt_st_sampling.grid(row=13, column=1)

tk.Label(win, text='Дата поступления').grid(row=14, column=0)
dt_get_receipt = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
dt_get_receipt.grid(row=14, column=1)

# Даты окончания

tk.Label(win, text='Дата окончания исследования').grid(row=15, column=0)
dt_fn_research = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
dt_fn_research.grid(row=15, column=1)

dt_fn_value_1 = tk.StringVar()
dt_fn_value_2 = tk.StringVar()
dt_fn_value_3 = tk.StringVar()
dt_fn_value_1.set('No')
dt_fn_value_2.set('No')
dt_fn_value_3.set('No')

dt_st_check_button_1 = tk.Checkbutton(win, text='пов. дату окончания пробоподготовки', command=repeat_for_dt_fn_1,
                                      variable=dt_fn_value_1, offvalue='No', onvalue='Yes')
dt_st_check_button_1.grid(row=15, column=2, stick='w')
dt_st_check_button_2 = tk.Checkbutton(win, text='пов. дату утилизации пробы/сведения о консервации',
                                      command=repeat_for_dt_fn_2, variable=dt_fn_value_2, offvalue='No', onvalue='Yes')
dt_st_check_button_2.grid(row=15, column=3, stick='w')
dt_st_check_button_3 = tk.Checkbutton(win, text='пов. дату выписки листа прокола', command=repeat_for_dt_fn_3,
                                      variable=dt_fn_value_3, offvalue='No', onvalue='Yes')
dt_st_check_button_3.grid(row=15, column=4, stick='w')

tk.Label(win, text='Дата окончания пробоподготовки').grid(row=16, column=0)
dt_fn_sample_prep = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
dt_fn_sample_prep.grid(row=16, column=1)

tk.Label(win, text='Дата утилизации пробы/сведения о консервации').grid(row=17, column=0)
dt_disposal = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
dt_disposal.grid(row=17, column=1)

tk.Label(win, text='Дата выписки листа протокола').grid(row=18, column=0)
dt_issue_protocol = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
dt_issue_protocol.grid(row=18, column=1)

# Этапы исследования
repeat_for_stp_value = tk.StringVar()
repeat_for_stp_value.set('No')
tk.Label(win, text='Этапы пробоподготовки').grid(row=19, column=0)
steps_sample = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
steps_sample.grid(row=19, column=1)
stp_check_button = tk.Checkbutton(win, text='автом. этапы исследования', command=repeat_for_stp,
                                  variable=repeat_for_stp_value, offvalue='No', onvalue='Yes')
stp_check_button.grid(row=19, column=2)
tk.Label(win, text='Этапы исследования').grid(row=20, column=0)
stp_research = tk.Entry(win, justify=tk.LEFT, font=('Arial', 10), width=25)
stp_research.grid(row=20, column=1)

# Эксель файл 1
tk.Label(win, text='Выбери эксель пробоподготовки 1').grid(row=21, column=0)
tk.Button(text='Выбери файл', bd=5, font=('Arial', 10), command=get_file_1).grid(row=21, column=2, stick='w', padx=25)

# Эксель файл 2
tk.Label(win, text='Выбери регистрационный эксель файл 2').grid(row=22, column=0)
tk.Button(text='Выбери файл 2', bd=5, font=('Arial', 10), command=get_file_2).grid(row=22, column=2, stick='w', padx=25)
op_xl_button_value = tk.StringVar()
op_xl_button_value.set('Yes')
print(op_xl_button_value.get())
op_xl_button = tk.Checkbutton(win, text='открыть ли эксель', variable=op_xl_button_value, offvalue='No', onvalue='Yes')
op_xl_button.grid(row=22, column=3)

# Кнопка на сервер
tk.Button(text='Пушь на сервак', bd=5, font=('Arial', 10), command=excel_func).grid(row=100, column=0, pady=10)

win.mainloop()
