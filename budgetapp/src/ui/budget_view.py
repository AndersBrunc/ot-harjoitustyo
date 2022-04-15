from tkinter import ttk, constants
from service.budgetapp_service import budgetapp_service


class BudgetView:
    def __init__(self, root, handle_logout):
        self._root = root
        self._handle_logout = handle_logout
        self._user = budgetapp_service.current_user()
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _logout_handler(self):
        budgetapp_service.logout()
        self._handle_logout()

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
        label.grid(row=1, column=0, padx=10, pady=10, sticky=constants.W)
        logout_button.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
            sticky=constants.EW
        )

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._initialize_header()

        self._frame.grid_configure(0, weight=1, minsize=600)
