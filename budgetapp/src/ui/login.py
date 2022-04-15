from tkinter import ttk, constants, StringVar
from service.budgetapp_service import budgetapp_service, InvalidCredentialsError


class LoginView:

    def __init__(self, root, handle_login, handle_show_create_user_view):
        self._root = root
        self._handle_login = handle_login
        self._handle_show_create_user_view = handle_show_create_user_view
        self._username_input = None
        self._password_input = None
        self._error_variable = None
        self._error_label = None
        self._frame = None

        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _initialize_username_field(self):
        label = ttk.Label(master=self._frame, text='Username')
        self._username_input = ttk.Entry(master=self._frame)

        label.grid(padx=10, pady=10, sticky=constants.W)
        self._username_input.grid(padx=5, pady=10, sticky=constants.EW)

    def _initialize_password_field(self):
        label = ttk.Label(master=self._frame, text='Password')
        self._password_input = ttk.Entry(master=self._frame)

        label.grid(padx=10, pady=10, sticky=constants.W)
        self._password_input.grid(padx=5, pady=10, sticky=constants.EW)

    def _login_handler(self):
        username = self._username_input.get()
        password = self._password_input.get()

        try:
            budgetapp_service.login(username, password)
            self._handle_login()
        except InvalidCredentialsError:
            self._show_error('Invalid username or password')

    def _show_error(self, text):
        self._error_variable.set(text)
        self._error_label.grid()

    def _hide_error(self):
        self._error_label.grid_remove()

    def _initialize(self):
        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)
        self._error_label = ttk.Label(
            master=self._frame,
            text=self._error_variable,
            foreground='yellow'
        )
        self._error_label.grid(padx=10, pady=10)

        self._initialize_username_field()
        self._initialize_password_field()

        login_button = ttk.Button(
            master=self._frame,
            text='Login',
            command=self._login_handler
        )
        create_user_button = ttk.Button(
            master=self._frame,
            text='Create User',
            command=self._handle_show_create_user_view
        )
        self._frame.grid_columnconfigure(0, weight=1, minsize=600)
        login_button.grid(padx=4, pady=4, sticky=constants.EW)
        create_user_button.grid(padx=6, pady=6, sticky=constants.EW)

        self._hide_error()
