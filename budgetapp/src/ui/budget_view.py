from tkinter import ttk, constants
from service.budgetapp_service import budgetapp_service


class BudgetListView:
    def __init__(self,root,budgets, handle_delete_one):
        self._root = root
        self._budgets = budgets
        self._handle_delete_one_budget = handle_delete_one
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_budget_item(self, budget):
        item_frame = ttk.Frame(master=self._frame)
        label = ttk.Label(master=item_frame, text = f'{budget.name}: {budget.c_amount} € left')

        delete_budget_button= ttk.Button(
            master=item_frame,
            text='Delete',
            command=lambda: self._handle_delete_one_budget(budget.id)
        )
        label.grid(row=0 ,column=1,padx=5,pady=5,sticky=constants.W)
        delete_budget_button.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky=constants.W
        )
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.pack(fill=constants.X)

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        
        for budget in self._budgets:
            self._initialize_budget_item(budget)
        
class EconomyListView:
    def __init__(self,root, handle_update_value):
        self._root = root
        self._handle_update_value = handle_update_value
        self._user = budgetapp_service.current_user()
        self._frame = None
        
        self._economy_spinbox_value = None
        self._economy_update_input = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_economy_list(self):
        balance_label=ttk.Label(
            master=self._frame,
            text=f'Balance: {self._user.balance} €'
        )
        balance_label.grid(padx=5,pady=5,sticky=constants.EW)
        income_label=ttk.Label(
            master=self._frame,
            text=f'Income: {self._user.income} €'
        )
        income_label.grid(padx=5,pady=5,sticky=constants.EW)
        expenses_label=ttk.Label(
            master=self._frame,
            text=f'Expenses: {self._user.expenses} €'
        )
        expenses_label.grid(padx=5,pady=5,sticky=constants.EW)

    def _initialize_footer(self):

        update_label=ttk.Label(master=self._frame, text='Choose Value to update:')
        update_label.grid(padx=5,pady=5,sticky=constants.EW)

        values=['Balance','Income','Expenses']
        self._economy_spinbox_value = ttk.Spinbox(
            master=self._frame,
            from_=0,
            to=3,
            increment=1,
            values=values 
        )
        self._economy_spinbox_value.grid(padx=5,pady=5,sticky=constants.EW)

        new_amount_label=ttk.Label(master=self._frame, text='New amount (€):')
        new_amount_label.grid(padx=5,pady=5,sticky=constants.EW)

        self._economy_update_input = ttk.Entry(master=self._frame)
        self._economy_update_input.grid(padx=5,pady=5,sticky=constants.EW)

        update_button = ttk.Button(
            master=self._frame,
            text='Update Value',
            command=self._handle_update_value(
                self._economy_spinbox_value.get,
                self._economy_update_input.get
            )
        )
        update_button.grid(padx=5,pady=5,sticky=constants.EW)
        

    def _initialize(self):
        self._frame=ttk.Frame(master=self._root)
        self._initialize_economy_list()
        self._initialize_footer()



class BudgetView:
    def __init__(self, root, handle_logout, handle_show_purchases, handle_create_budget, handle_show_add_purchase):
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

        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _logout_handler(self):
        budgetapp_service.logout()
        self._handle_logout()

    def _handle_delete_one_budget(self, budget_id):
        budgetapp_service.delete_budget(budget_id)
        self._initialize_budget_list()

    def _handle_update_value(self, value, new_amount):

        #error for amount input needs to be added

        budgetapp_service.update_user_economy_value(value,new_amount)
        self._initialize_economy_list()

    def _initialize_economy_list(self):
        if self._economy_list_view:
            self._economy_list_view.destroy()

        self._economy_list_view = EconomyListView(
            self._economy_list_frame,
            self._handle_update_value
        )
        self._economy_list_view.pack()

    def _initialize_budget_list(self):
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
        user_label = ttk.Label(
            master=self._frame,
            text=f'Logged in as {self._user.username}'
        )
        user_label.grid(row=0, column=0, padx=2, pady=2, sticky=constants.W)

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

    def _initialize_footer(self):
        create_budget_button = ttk.Button(
            master=self._frame,
            text='Create Budget',
            command=self._handle_create_budget
        )
        create_budget_button.grid(
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.EW
        )
        purchase_history_button = ttk.Button(
            master=self._frame,
            text = 'View Purchase History',
            command=self._handle_show_purchases
        )
        purchase_history_button.grid(
            row=4,
            column=1,
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
            row=3,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.EW
        )
    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._budget_list_frame = ttk.Frame(master=self._frame)
        self._economy_list_frame = ttk.Frame(master=self._frame)

        self._initialize_header()
        self._initialize_economy_list()
        self._initialize_budget_list()
        self._initialize_footer()

        self._budget_list_frame.grid(
            row=1,
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

        self._frame.grid_columnconfigure(0, weight=1, minsize=100)
        self._frame.grid_columnconfigure(1, weight=0)
