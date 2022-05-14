from tkinter import ttk, constants, StringVar
from service.budgetapp_service import budgetapp_service


class AddPurchaseView:
    """Class of the add purchase view
    """
    def __init__(self, root, handle_show_budget_view):
        """Class constructor
            Args:
                root: Tk-object, represents the window
                handle_show_budget_view: reference to method that switches view to the home view

        """
        self._root = root
        self._handle_show_budget_view = handle_show_budget_view
        self._frame = None

        self._user = budgetapp_service.current_user()
        self._budgets = budgetapp_service.fetch_user_budgets()

        self._category_spinbox = None
        self._budget_spinbox = None

        self._amount_input = None
        self._comment_input = None

        self._error_variable = None
        self._error_label = None

        self._initialize()

    def pack(self):
        """Packs the frame
        """
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Destroys the frame
        """
        self._frame.destroy()

    def _initialize_header(self):
        """Initializes the header of the frame
        """
        user_label = ttk.Label(
            master=self._frame,
            text=f'Logged in as {self._user.username}'
        )
        user_label.grid(row=1, column=0, padx=2, pady=2, sticky=constants.W)
        user_economy_label = ttk.Label(
            master=self._frame,
            text=(
                f'Balance: {self._user.balance} €   Income: {self._user.income} €   Expenses: {self._user.expenses} €')
        )
        user_economy_label.grid(row=0, column=1, padx=2,
                                pady=2, sticky=constants.E)

    def _initialize_budget_selection(self):
        """Initializes the input field/scrollbar for the budget name
        """
        label = ttk.Label(master=self._frame,
                          text='Choose Budget that will be affected:')
        label.grid(row=3, column=0, padx=5, pady=5, sticky=constants.W)

        values = [budget.name for budget in self._budgets]
        self._budget_spinbox = ttk.Spinbox(
            master=self._frame,
            from_=0,
            to=5,
            increment=1,
            values=values
        )
        self._budget_spinbox.grid(
            row=3, column=1, padx=5, pady=5, sticky=constants.W)

    def _intitialize_category_selection(self):
        """Initializes the input field/scrollbar for the purchase category
        """
        label = ttk.Label(master=self._frame, text='Choose Category:')
        label.grid(padx=5, pady=5, sticky=constants.W)

        values = ['Food', 'Shopping', 'Transport', 'Other']
        self._category_spinbox = ttk.Spinbox(
            master=self._frame,
            from_=0,
            to=5,
            increment=1,
            values=values
        )
        self._category_spinbox.grid(
            row=4, column=1, padx=5, pady=5, sticky=constants.W)

    def _initialize_amount_field(self):
        """Initializes amount input field
        """
        label = ttk.Label(master=self._frame, text='Receipt amount (€):')
        self._amount_input = ttk.Entry(master=self._frame)

        label.grid(padx=5, pady=5, sticky=constants.W)
        self._amount_input.grid(row=5, column=1, padx=5,
                                pady=5, sticky=constants.EW)

    def _initialize_comment_field(self):
        """Initializes comment input field
        """
        label = ttk.Label(master=self._frame, text='Comment:')
        self._comment_input = ttk.Entry(master=self._frame)

        label.grid(padx=5, pady=5, sticky=constants.W)
        self._comment_input.grid(
            row=6, column=1, padx=5, pady=5, sticky=constants.EW)

    def _add_purchase_handler(self):
        """If conditions are met, adds a purchase to the users history
        """
        budget_name = self._budget_spinbox.get()
        budget = filter(lambda budget: budget.name ==
                        budget_name, self._budgets)
        try:
            budget_id = list(budget)[0].id
        except:
            IndexError(f'You do not have a budget named {budget_name}')
            self._show_error(f'You do not have a budget named {budget_name}')
            return

        category = self._category_spinbox.get()
        amount = self._amount_input.get()
        comment = self._comment_input.get()

        if len(category) == 0:
            self._show_error('The purchase has to be categorized')
            return

        try:
            amount = float(amount)
        except:
            ValueError('Amount must be a positive number')
            self._show_error('Amount must be a positive number')
            return

        if float(amount) <= 0:
            self._show_error('Amount must be a positive number')
            return

        if amount > self._user.balance:
            self._show_error('The purchase amount exceeds your balance')
            return

        budgetapp_service.add_purchase(budget_id, amount, category, comment)
        self._handle_show_budget_view()

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

        self._error_variable = StringVar(self._frame)
        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground='orange'
        )
        self._error_label.grid(row=1, column=1, padx=5, pady=5)

        self._initialize_header()
        self._initialize_budget_selection()
        self._intitialize_category_selection()
        self._initialize_amount_field()
        self._initialize_comment_field()

        back_to_budgets_button = ttk.Button(
            master=self._frame,
            text='Back',
            command=self._handle_show_budget_view
        )
        back_to_budgets_button.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky=constants.W
        )
        add_purchase_button = ttk.Button(
            master=self._frame,
            text='Add Purchase',
            command=self._add_purchase_handler
        )
        add_purchase_button.grid(
            row=7, column=0, columnspan=2, padx=5, pady=5, sticky=constants.EW)

        self._frame.pack()

        self._hide_error()
