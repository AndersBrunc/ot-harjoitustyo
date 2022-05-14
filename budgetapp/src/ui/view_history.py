from tkinter import ttk, constants
from service.budgetapp_service import budgetapp_service


class PurchaseListView:
    """Class of the list of purchases
    """
    def __init__(self, root, purchases, handle_delete_one):
        """Class constructor
        
            Args:
                root: ttk.Frame, represents the frame of the window
                purchases: list, list of users Purchase-objects
                handle_delete_one: reference to method that deletes one purchase

        """
        self._root = root
        self._purchases = purchases
        self._handle_delete_one = handle_delete_one
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

    def _initialize_purchase_item(self, purchase):
        """Inititalizes a purchase item with a delete button attached
        """
        item_frame = ttk.Frame(master=self._frame)
        label = ttk.Label(
            master=item_frame,
            text=f'{purchase.category}: {purchase.amount} € | {purchase.comment}')

        delete_purchase_button = ttk.Button(
            master=item_frame,
            text='X',
            command=lambda: self._handle_delete_one(purchase.id)
        )
        label.grid(row=0, column=0, padx=5, pady=5, sticky=constants.W)
        delete_purchase_button.grid(
            row=0,
            column=1,
            padx=1,
            pady=1,
            sticky=constants.EW
        )
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.pack(fill=constants.X)

    def _initialize(self):
        """Initializes the list of purchase-items
        """
        self._frame = ttk.Frame(master=self._root)

        for purchase in self._purchases:
            self._initialize_purchase_item(purchase)


class PurchaseView:
    """Class of the purchase history view
    """
    def __init__(self, root, handle_show_budget_view):
        """Class constructor
        
            Args:
                root: Tk-object, represents the window
                handle_show_budget_view: reference to method that switches view to the home view
        """
        self._root = root
        self._handle_show_budget_view = handle_show_budget_view
        self._user = budgetapp_service.current_user()

        self._purchase_list_view = None
        self._purchase_list_frame = None
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

    def _handle_delete_one(self, purchase_id):
        """Deletes purchase on button press
        """
        budgetapp_service.delete_purchase(purchase_id)
        self._initialize_purchase_list()

    def _initialize_purchase_list(self):
        """Initializes the list of purchase-items
        """
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
        """Initializes the header of the frame
        """
        label = ttk.Label(
            master=self._frame,
            text=f'Logged in as {self._user.username}'
        )

        purchase_list_label = ttk.Label(
            master=self._frame,
            text='Purchases'
        )

        back_to_budgets_button = ttk.Button(
            master=self._frame,
            text='Back',
            command=self._handle_show_budget_view
        )
        label.grid(row=0, column=0, padx=5, pady=5, sticky=constants.W)
        purchase_list_label.grid(
            row=2, column=0, padx=5, pady=5, sticky=constants.W)

        back_to_budgets_button.grid(
            row=0,
            column=1,
            padx=5,
            pady=5,
            sticky=constants.E
        )

    def _initialize(self):
        """Initializes all class components/window features
        """
        self._frame = ttk.Frame(master=self._root)
        self._purchase_list_frame = ttk.Frame(master=self._frame)

        self._initialize_header()
        self._initialize_purchase_list()

        self._purchase_list_frame.grid(
            row=3,
            column=0,
            columnspan=1,
            sticky=constants.EW
        )

        self._frame.grid_columnconfigure(0, weight=1, minsize=300)
        self._frame.grid_columnconfigure(1, weight=0)
