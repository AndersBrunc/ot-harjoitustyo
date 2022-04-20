from tkinter import ttk, constants, StringVar
from service.budgetapp_service import budgetapp_service, NegativeInputError

class AddPurchaseView:
    def __init__(self, root, handle_logout, handle_show_budget_view):
        self._root = root
        self._handle_logout = handle_logout
        self._handle_show_budget_view = handle_show_budget_view
        self._user = budgetapp_service.current_user()
        self._budgets = budgetapp_service.fetch_user_budgets()
        
        self._category_spinbox = None
        self._budget_spinbox = None

        self._amount_input = None
        self._comment_input = None

        self._error_variable = None
        self._error_label = None
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_category_field(self):
        label = ttk.Label(master=self._frame, text='Category')
        self._category_input = ttk.Entry(master=self._frame)

        label.grid(padx=10, pady=10, sticky=constants.W)
        self._category_input.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize_amount_field(self):
        label = ttk.Label(master=self._frame, text='Receipt amount (€)')
        self._amount_input = ttk.Entry(master=self._frame)

        label.grid(padx=5, pady=5, sticky=constants.W)
        self._amount_input.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize_comment_field(self):
        label = ttk.Label(master=self._frame, text='Comment')
        self._comment_input = ttk.Entry(master=self._frame)

        label.grid(padx=5, pady=5, sticky=constants.W)
        self._comment_input.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize_header(self):
        user_label = ttk.Label(
            master=self._frame,
            text=f'Logged in as {self._user.username}'
        )
        user_label.grid(row=0, column=0, padx=2, pady=2, sticky=constants.W)
        user_economy_label = ttk.Label(
            master=self._frame,
            text=(f'Balance: {self._user.balance} €   Income: {self._user.income} €   Expenses: {self._user.expenses} €')
        )
        user_economy_label.grid(row=0, column=1, padx=2, pady=2, sticky=constants.E)
        logout_button = ttk.Button(
            master=self._frame,
            text='Logout',
            command=self._logout_handler
        )
        logout_button.grid(
            row=1,
            column=0,
            padx=2,
            pady=2,
            sticky=constants.W
        )
    
    def _add_purchase_handler(self):
        budget_name = self._budget_spinbox.get()
        budget = filter(lambda budget: budget.name == budget_name,self._budgets)
        budget_id = list(budget)[0].id
        category = self._category_spinbox.get()
        amount = self._amount_input.get()
        comment = self._comment_input.get()

        if len(category) == 0:
            self._show_error('The purchase has to be categorized')
        
        budgetapp_service.add_purchase(budget_id, amount, category, comment)
        self._handle_show_budget_view()

    def _show_error(self, text):
        self._error_variable.set(text)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()

    def _initialize_budget_selection(self):
        label = ttk.Label(master=self._frame, text='Choose Budget that will be affected')
        label.grid(padx=10, pady=10, sticky=constants.W)
        
        values = [budget.name for budget in self._budgets]
        self._budget_spinbox = ttk.Spinbox(
            master=self._frame,
            from_=0,
            to=10,
            increment=1,
            values=values 
        )
        self._budget_spinbox.grid(row=1 ,column=0,padx=5,pady=5,sticky=constants.W)

    def _intitialize_category_selection(self):
        label = ttk.Label(master=self._frame, text='Choose Category')
        label.grid(padx=10, pady=10, sticky=constants.W)

        values = ['Food','Shopping','Transport','Other']
        self._category_spinbox = ttk.Spinbox(
            master=self._frame,
            from_=0,
            to=10,
            increment=1,
            values=values 
        )
        self._category_spinbox.grid(row=0 ,column=0,padx=5,pady=5,sticky=constants.W)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)
        self._error_label = ttk.Label(
            master=self._frame,
            text=self._error_variable,
            foreground='yellow'
        )
    
        self._initialize_header
        self._initialize_budget_selection
        self._intitialize_category_selection
        self._initialize_amount_field
        self._initialize_comment_field

        add_purchase_button = ttk.Button(
            master=self._frame,
            text='Add Purchase',
            command=self._add_purchase_handler
        )
        add_purchase_button.grid(padx=5, pady=5, sticky=constants.EW)
        
        self._frame.grid_columnconfigure(1, weight=1, minsize=500)

        self._hide_error()