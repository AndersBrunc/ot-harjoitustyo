from tkinter import ttk, constants, StringVar
from service.budgetapp_service import budgetapp_service


class BudgetListView:
    """Class of the list of user's budgets
    """
    def __init__(self, root, budgets, handle_delete_one):
        """Class constructor
            Args:
                root: ttk.Frame, represents the window frame
                budgets: list, list of Budget-objects
                handle_delete_one: reference to method that deletes one budget
                
        """
        self._root = root
        self._budgets = budgets
        self._handle_delete_one_budget = handle_delete_one
        self._frame = None

        self._initialize()

    def pack(self):
        """Packs the frame
        """
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Destroys the frame
        """
        self._frame.destroy()

    def _initialize_budget_item(self, budget):
        """Initializes the budget-items witch delete button attached
        """
        item_frame = ttk.Frame(master=self._frame)
        label = ttk.Label(master=item_frame,
                          text=f'{budget.name}: {budget.c_amount} € left')

        delete_budget_button = ttk.Button(
            master=item_frame,
            text='X',
            command=lambda: self._handle_delete_one_budget(budget.id)
        )
        label.grid(row=0, column=1, padx=5, pady=5, sticky=constants.W)
        delete_budget_button.grid(
            row=0,
            column=0,
            padx=1,
            pady=1,
            sticky=constants.W
        )
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.pack(fill=constants.X)

    def _initialize(self):
        """Initializes the list of budget-items
        """
        self._frame = ttk.Frame(master=self._root)

        for budget in self._budgets:
            self._initialize_budget_item(budget)


class EconomyListView:
    """Class of the list of users economic stats
    """
    def __init__(self, root, handle_update_value):
        """Class constructor
            Args:
                root: ttk.Frame, represents the window frame
                handle_update_value: reference to method that updates one of the economic values

        """
        self._root = root
        self._handle_update_value = handle_update_value
        self._user = budgetapp_service.current_user()
        self._frame = None

        self._economy_spinbox_value = None
        self._economy_update_input = None

        self._initialize()

    def pack(self):
        """Packs the frame
        """
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Destroys the frame
        """
        self._frame.destroy()

    def _initialize_list_items(self):
        """Initializes the items in the economic list
        """
        balance_label = ttk.Label(
            master=self._frame,
            text=f'Balance: {self._user.balance} €'
        )
        balance_label.grid(padx=5, pady=5, sticky=constants.EW)
        income_label = ttk.Label(
            master=self._frame,
            text=f'Income: {self._user.income} €'
        )
        income_label.grid(padx=5, pady=5, sticky=constants.EW)
        expenses_label = ttk.Label(
            master=self._frame,
            text=f'Expenses: {self._user.expenses} €'
        )
        expenses_label.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize_footer(self):
        """Initializes list footer
        """
        update_label = ttk.Label(
            master=self._frame, text='Choose Value to update:')
        update_label.grid(padx=5, pady=5, sticky=constants.EW)

        values = ['Balance', 'Income', 'Expenses']
        self._economy_spinbox_value = ttk.Spinbox(
            master=self._frame,
            from_=0,
            to=3,
            increment=1,
            values=values
        )
        self._economy_spinbox_value.grid(padx=5, pady=5, sticky=constants.EW)

        new_amount_label = ttk.Label(
            master=self._frame, text='New amount (€):')
        new_amount_label.grid(padx=5, pady=5, sticky=constants.EW)

        self._economy_update_input = ttk.Entry(master=self._frame)
        self._economy_update_input.grid(padx=5, pady=5, sticky=constants.EW)

        update_button = ttk.Button(
            master=self._frame,
            text='Update Value',
            command=lambda: self._handle_update_value(
                self._economy_spinbox_value.get(),
                self._economy_update_input.get()
            )
        )
        update_button.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize(self):
        """Initializes list of the economic values and the footer
        """
        self._frame = ttk.Frame(master=self._root)
        self._initialize_list_items()
        self._initialize_footer()


class BudgetView:
    """Class of the home screen/ budget view
    """
    def __init__(self, root, handle_logout, handle_show_purchases, handle_create_budget, handle_show_add_purchase):
        """Class constructor
        
            Args:
                root: Tk-object, represents the window
                handle_logout: reference to method that switches the view to the login view
                handle_show_purchases: reference to method that switches the view to the purchase history view
                handle_create_budget: reference to method that switches the view to the create budget view
                handle_show_add_purchase: reference to method that switches the view to the add purchase view
        """
        self._root = root
        self._handle_logout = handle_logout
        self._handle_show_purchases = handle_show_purchases
        self._handle_create_budget = handle_create_budget
        self._handle_show_add_purchase = handle_show_add_purchase
        self._user = budgetapp_service.current_user()

        self._economy_list_view = None
        self._economy_list_frame = None

        self._budget_list_view = None
        self._budget_list_frame = None

        self._error_variable = None
        self._error_label = None
        self._frame = None

        self._initialize()

    def pack(self):
        """Packs the frame
        """
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Destroys the frame
        """
        self._frame.destroy()

    def _logout_handler(self):
        """Logs user out upon button press
        """
        budgetapp_service.logout()
        self._handle_logout()

    def _handle_delete_one_budget(self, budget_id):
        """Deletes a budget upon button press
        """
        budgetapp_service.delete_budget(budget_id)
        self._initialize_budget_list()

    def _handle_update_value(self, value, new_amount):
        """If conditions are met, updates a specified economy value of the user
        """
        try:
            new_amount = float(new_amount)
            if new_amount <= 0:
                self._show_error('Amount must be a positive number')
                return
        except:
            ValueError('Amount must be a positive number')
            self._show_error('Amount must be a positive number')
            return

        budgetapp_service.update_user_economy_value(value, new_amount)
        self._initialize_economy_list()

    def _initialize_economy_list(self):
        """Initializes the list of the user's balance, income and expenses
        """
        if self._economy_list_view:
            self._economy_list_view.destroy()

        self._economy_list_view = EconomyListView(
            self._economy_list_frame,
            self._handle_update_value
        )
        self._economy_list_view.pack()

    def _initialize_budget_list(self):
        """Initializes the list of the user's budgets
        """
        if self._budget_list_view:
            self._budget_list_view.destroy()

        budgets = budgetapp_service.fetch_user_budgets()

        self._budget_list_view = BudgetListView(
            self._budget_list_frame,
            budgets,
            self._handle_delete_one_budget
        )

        self._budget_list_view.pack()

    def _initialize_header(self):
        """Initializes the header of the frame
        """
        user_label = ttk.Label(
            master=self._frame,
            text=f'Logged in as {self._user.username}'
        )
        user_label.grid(row=1, column=0, padx=2, pady=2, sticky=constants.W)
        budgets_label = ttk.Label(
            master=self._frame,
            text='Budgets'
        )
        budgets_label.grid(row=1, column=1, padx=2, pady=2, sticky=constants.W)
        logout_button = ttk.Button(
            master=self._frame,
            text='Logout',
            command=self._logout_handler
        )
        logout_button.grid(
            row=0,
            column=0,
            padx=2,
            pady=2,
            sticky=constants.W
        )

    def _initialize_footer(self):
        """Initializes the footer of the frame
        """
        create_budget_button = ttk.Button(
            master=self._frame,
            text='Create Budget',
            command=self._handle_create_budget
        )
        create_budget_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.EW
        )
        purchase_history_button = ttk.Button(
            master=self._frame,
            text='View Purchase History',
            command=self._handle_show_purchases
        )
        purchase_history_button.grid(
            row=5,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=constants.EW
        )
        add_purchase_button = ttk.Button(
            master=self._frame,
            text='Add Purchase',
            command=self._handle_show_add_purchase
        )
        add_purchase_button.grid(
            row=4,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=constants.EW
        )

    def _show_error(self, text):
        """Shows error message

            Args:
                text: string, the error message

        """
        self._error_variable.set(text)
        self._error_label.grid()

    def _hide_error(self):
        """Hides error message
        """
        self._error_label.grid_remove()

    def _initialize(self):
        """Initializes all class components/window features
        """
        self._frame = ttk.Frame(master=self._root)
        self._budget_list_frame = ttk.Frame(master=self._frame)
        self._economy_list_frame = ttk.Frame(master=self._frame)

        self._initialize_header()
        self._initialize_economy_list()
        self._initialize_budget_list()
        self._initialize_footer()

        self._budget_list_frame.grid(
            row=2,
            column=1,
            columnspan=1,
            sticky=constants.W
        )

        self._economy_list_frame.grid(
            row=2,
            column=0,
            columnspan=1,
            sticky=constants.W
        )

        self._error_variable = StringVar(self._frame)
        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground='orange'
        )

        self._error_label.grid(row=1, column=0, padx=5, pady=5)

        self._frame.grid_columnconfigure(0, weight=1, minsize=200)
        self._frame.grid_columnconfigure(1, weight=0)
