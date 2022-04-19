from tkinter import ttk, constants, StringVar
from service.budgetapp_service import budgetapp_service, NegativeInputError

class CreateBudgetView:
    def __init__(self,root,handle_logout, handle_show_budget_view):
        self._root = root
        self._handle_logout = handle_logout
        self._handle_show_budget_view = handle_show_budget_view
        self._user = budgetapp_service.current_user()

        self._budgetname_input = None
        self._amount_input = None

        self._error_variable = None
        self._error_label = None
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()
    
    def _logout_handler(self):
        budgetapp_service.logout()
        self._handle_logout()
    
    def _initialize_budgetname_field(self):
        label = ttk.Label(master=self._frame, text='Name of Budget')
        self._budgetname_input = ttk.Entry(master=self._frame)

        label.grid(padx=5, pady=5, sticky=constants.W)
        self._budgetname_input.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize_amount_field(self):
        label = ttk.Label(master=self._frame, text='Budget amount (€)')
        self._amount_input = ttk.Entry(master=self._frame)

        label.grid(padx=10, pady=10, sticky=constants.W)
        self._amount_input.grid(padx=5, pady=5, sticky=constants.EW)

    def _create_budget_handler(self):
        budgetname = self._budgetname_input.get()
        amount = self._amount_input.get()

        if len(budgetname) == 0:
            self._show_error('A name for the budget is required')
            return

    # must create error for negative stuff

        budgetapp_service.create_budget(budgetname, amount)
        self._handle_show_budget_view()
        
    def _show_error(self, text):
        self._error_variable.set(text)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()

    def _initialize_header(self):
        label = ttk.Label(
            master=self._frame,
            text=f'Logged in as {self._user.username}'
        )
        logout_button = ttk.Button(
            master=self._frame,
            text='Logout',
            command=self._logout_handler
        )
        label.grid(row=1, column=0, padx=5, pady=5, sticky=constants.W)
        logout_button.grid(
            row=2,
            column=0,
            padx=5,
            pady=5,
            sticky=constants.W
        )

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)
        self._error_label = ttk.Label(
            master=self._frame,
            text=self._error_variable,
            foreground='yellow'
        )
        self._error_label.grid(padx=5, pady=5)

        self._initialize_header()
        self._initialize_budgetname_field()
        self._initialize_amount_field()

        create_budget_button = ttk.Button(
            master=self._frame,
            text='Create New Budget',
            command=self._create_budget_handler
        )
        create_budget_button.grid(padx=5, pady=5, sticky=constants.EW)
        
        self._frame.grid_columnconfigure(1, weight=1, minsize=500)
        self._hide_error()