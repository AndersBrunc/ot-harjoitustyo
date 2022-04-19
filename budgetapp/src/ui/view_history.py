from tkinter import ttk, constants
from service.budgetapp_service import budgetapp_service

class PurchaseListView:
    def __init__(self,root, purchases, handle_delete_one):
        self._root = root
        self._purchases = purchases
        self._handle_delete_one = handle_delete_one
        self._frame =None
        
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_purchase_item(self, purchase):
        item_frame = ttk.Frame(master=self._frame)
        label = ttk.Label(master=self._frame, text=purchase.category)

        delete_purchase_button = ttk.Button(
            master=item_frame,
            text='Delete',
            command=lambda: self._handle_delete_one(purchase.id)
        )
        label.grid(row=0 ,column=0,padx=10,pady=10,sticky=constants.W)
        delete_purchase_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.EW
        )
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.pack(fill=constants.X)

    def _initialize(self):
        self._frame=ttk.Frame(master=self._root)

        for purchase in self._purchases:
            self._initialize_purchase_item(purchase)


class PurchaseView:
    def __init__(self, root, handle_logout, handle_show_budget_view):
        self._root = root
        self._handle_logout = handle_logout
        self._handle_show_budget_view = handle_show_budget_view
        self._user = budgetapp_service.current_user()
        
        self._purchase_list_view = None
        self._purchase_list_frame = None
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _logout_handler(self):
        budgetapp_service.logout()
        self._handle_logout

    def _handle_delete_one(self, purchase_id):
        budgetapp_service.delete_purchase(purchase_id)
        self._initialize_purchase_list()

    def _initialize_purchase_list(self):
        if self._purchase_list_view:
            self._purchase_list_view.destroy()
        
        purchases = budgetapp_service.fetch_user_purchases()

        self._purchase_list_view = PurchaseListView(
            self._purchase_list_frame,
            purchases,
            self._handle_delete_one
        )
        self._purchase_list_view.pack()

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
        back_to_budgets_button = ttk.Button(
            master=self._frame,
            text='Back',
            command=self._handle_show_budget_view
        )
        label.grid(row=1, column=0, padx=10, pady=10, sticky=constants.W)
        logout_button.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
            sticky=constants.EW
        )
        back_to_budgets_button.grid(
            row=2,
            column=1,
            padx=10,
            pady=10,
            sticky=constants.EW
        )

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)
        self._purchase_list_frame = ttk.Frame(master=self._frame)

        self._initialize_header()
        self._initialize_purchase_list()

        self._purchase_list_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=constants.EW
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=600)
        self._frame.grid_columnconfigure(1, weight=0)
