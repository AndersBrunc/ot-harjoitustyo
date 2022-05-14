from tkinter import ttk, constants, StringVar
from service.budgetapp_service import budgetapp_service

class CreateBudgetView:
    """Class of the create budget view
    """
    def __init__(self, root, handle_show_budget_view):
        """Class constructor

            Args:
                root: Tk-object, represents the window
                handle_show_budget_view: reference to a method for switching the view to the home screen

        """
        self._root = root
        self._handle_show_budget_view = handle_show_budget_view
        self._user = budgetapp_service.current_user()

        self._budgetname_input = None
        self._amount_input = None

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

    def _initialize_budgetname_field(self):
        """Initializes input field for budget name
        """

        label = ttk.Label(master=self._frame, text='Name of Budget')
        self._budgetname_input = ttk.Entry(master=self._frame)

        label.grid(padx=5, pady=5, sticky=constants.EW)
        self._budgetname_input.grid(padx=5, pady=5, sticky=constants.EW)

    def _initialize_amount_field(self):
        """Initializes input field for budget amount
        """
        label = ttk.Label(master=self._frame, text='Budget amount (€)')
        self._amount_input = ttk.Entry(master=self._frame)

        label.grid(padx=10, pady=10, sticky=constants.EW)
        self._amount_input.grid(padx=5, pady=5, sticky=constants.EW)

    def _create_budget_handler(self):
        """If the conditions are met, creates Budget after button press
        """
        
        budgetname = self._budgetname_input.get()
        amount = self._amount_input.get()

        try:
            amount = float(amount)
        except:
            ValueError('Amount must be a positive number')
            self._show_error('Amount must be a positive number')
            return

        if len(budgetname) == 0:
            self._show_error('A name for the budget is required')
            return

        if float(amount) <= 0:
            self._show_error('Amount must be a positive number')
            return

        budgetapp_service.create_budget(budgetname, amount)
        self._handle_show_budget_view()

    def _show_error(self, text):
        """Shows error message

            Args:
                text: string, the error message

        """
        self._error_variable.set(text)
        self._error_label.grid()

    def _hide_error(self):
        """Hides the error message
        """
        self._error_label.grid_remove()

    def _initialize_header(self):
        """Inititalizes the header of the window
        """

        label = ttk.Label(
            master=self._frame,
            text=f'Logged in as {self._user.username}'
        )
        label.grid(row=0, column=0, padx=5, pady=5, sticky=constants.EW)

        back_to_budgets_button = ttk.Button(
            master=self._frame,
            text='Back',
            command=self._handle_show_budget_view
        )
        back_to_budgets_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.E
        )

    def _initialize(self):
        """Initializes all class-components/window features
        """

        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)
        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground='orange'
        )
        self._error_label.grid(row=1, column=0, padx=5, pady=5)

        self._initialize_header()
        self._initialize_budgetname_field()
        self._initialize_amount_field()

        create_budget_button = ttk.Button(
            master=self._frame,
            text='Create New Budget',
            command=self._create_budget_handler
        )
        create_budget_button.grid(padx=5, pady=5, sticky=constants.EW)

        self._frame.grid_columnconfigure(0, weight=1, minsize=300)
        self._hide_error()
