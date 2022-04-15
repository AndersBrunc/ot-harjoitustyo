from tkinter import ttk, constants, StringVar
from service.budgetapp_service import budgetapp_service, UsernameTakenError


class CreateUserView:

    def __init__(self, root, handle_create_user, handle_show_login_view):
        self._root = root
        self._handle_create_user = handle_create_user
        self._handle_show_login_view = handle_show_login_view
        self._username_input = None
        self._password_input = None
        self._balance_input = None
        self._income_input = None
        self._expenses_input = None
        self._error_variable = None
        self._error_label = None
        self._frame = None

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_username_field(self):
        label = ttk.Label(master=self._frame, text='Username')
        self._username_input = ttk.Entry(master=self._frame)

        label.grid(padx=10, pady=10, sticky=constants.W)
        self._username_input(padx=5, pady=10, sticky=constants.EW)

    def _initialize_password_field(self):
        label = ttk.Label(master=self._frame, text='Password')
        self._password_input = ttk.Entry(master=self._frame)

        label.grid(padx=10, pady=10, sticky=constants.W)
        self._password_input(padx=5, pady=10, sticky=constants.EW)

    def _initialize_balance_field(self):
        label = ttk.Label(master=self._frame, text='Balance (€)')
        self._balance_input = ttk.Entry(master=self._frame)

        label.grid(padx=10, pady=10, sticky=constants.W)
        self._balance_input(padx=5, pady=10, sticky=constants.EW)

    def _initialize_income_field(self):
        label = ttk.Label(master=self._frame, text='Monthly Income (€)')
        self._income_input = ttk.Entry(master=self._frame)

        label.grid(padx=10, pady=10, sticky=constants.W)
        self._income_input(padx=5, pady=10, sticky=constants.EW)

    def _initialize_expenses_field(self):
        label = ttk.Label(master=self._frame,
                          text='Monthly Recurring Expenses (€)')
        self._expenses_input = ttk.Entry(master=self._frame)

        label.grid(padx=10, pady=10, sticky=constants.W)
        self._income_input(padx=5, pady=10, sticky=constants.EW)

    def _create_user_handler(self):
        username = self._username_input.get()
        password = self._password_input.get()
        balance = self._balance_input.get()
        income = self._income_input.get()
        expenses = self._expenses_input.get()

        if len(username) == 0 or len(password) == 0:
            self._show_error('Username and password is required')
            return

        if balance <= 0 or income <= 0 or expenses <= 0:
            self._show_error('Value above 0 required')

        try:
            budgetapp_service.create_user(
                username, password, balance, income, expenses)
            self._handle_create_user()
        except UsernameTakenError:
            self._show_error(f'The username {username} has already been taken')

    def _show_error(self, text):
        self._error_variable.set(text)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()

    def _initalize(self):
        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)
        self._error_lable = ttk.Label(
            master=self._frame,
            text=self._error_variable,
            foreground='yellow'
        )
        self._error_label.grid(padx=10, pady=10)

        self._initialize_username_field()
        self._initialize_password_field()
        self._initialize_balance_field()
        self._initialize_income_field()
        self._initialize_expenses_field()

        login_button = ttk.Button(
            master=self._frame,
            text='Login',
            command=self._handle_show_login_view
        )
        create_user_button = ttk.Button(
            master=self._frame,
            text='Create New User',
            command=self._create_user_handler
        )
        self._frame.grid_columnconfigure(0, weight=1, minsize=600)
        login_button.grid(padx=4, pady=4, sticky=constants.EW)
        create_user_button.grid(padx=6, pady=6, sticky=constants.EW)

        self._hide_error()
