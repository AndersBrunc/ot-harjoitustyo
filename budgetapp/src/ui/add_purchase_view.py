from tkinter import ttk, constants, StringVar
from service.budgetapp_service import budgetapp_service, NegativeInputError

class AddPurchaseView:
    def __init__(self, root, budget_id, handle_logout, handle_show_budget_view):
        self._root = root
        self._budget_id = budget_id
        self._handle_logout = handle_logout
        self._handle_show_budget_view = handle_show_budget_view
        self._user = budgetapp_service.current_user()

        self._category_input = None
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
        category = self._category_input.get()
        amount = self._amount_input.get()
        comment = self._comment_input.get()

        if len(category) == 0:
            self._show_error('The purchase has to be categorized')
        
        budgetapp_service.add_purchase(self._budget_id, amount, category, comment)
        self._handle_show_budget_view()

    def _show_error(self, text):
        self._error_variable.set(text)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()