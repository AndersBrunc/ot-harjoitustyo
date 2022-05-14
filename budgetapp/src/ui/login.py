from tkinter import ttk, constants, StringVar
from service.budgetapp_service import budgetapp_service, InvalidCredentialsError


class LoginView:
    """Class of the login view
    """
    def __init__(self, root, handle_login, handle_show_create_user_view):
        """Class constructor

            Args:
                root: Tk-object, represents the window
                handle_login: reference to method for switching view to home view
                handle_show_create_user_view: reference to method for switching view to create user view
        """
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
        """Packs the frame
        """
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Destroys the frame
        """
        self._frame.destroy()

    def _initialize_username_field(self):
        """Initializes username input field
        """
        label = ttk.Label(master=self._frame, text='Username')
        self._username_input = ttk.Entry(master=self._frame)

        label.grid(padx=10, pady=10, sticky=constants.W)
        self._username_input.grid(padx=5, pady=10, sticky=constants.EW)

    def _initialize_password_field(self):
        """Initializes password input field
        """
        label = ttk.Label(master=self._frame, text='Password')
        self._password_input = ttk.Entry(master=self._frame)

        label.grid(padx=10, pady=10, sticky=constants.W)
        self._password_input.grid(padx=5, pady=10, sticky=constants.EW)

    def _login_handler(self):
        """If valid credentials, logs user in
        """
        username = self._username_input.get()
        password = self._password_input.get()

        try:
            budgetapp_service.login(username, password)
            self._handle_login()
        except InvalidCredentialsError:
            self._show_error('Invalid username or password')

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
        """Initializes all class-components/window features
        """
        
        self._frame = ttk.Frame(master=self._root)

        self._error_variable = StringVar(self._frame)
        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground='orange'
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
        self._frame.grid_columnconfigure(0, weight=1, minsize=400)
        login_button.grid(padx=4, pady=4, sticky=constants.EW)
        create_user_button.grid(padx=6, pady=6, sticky=constants.EW)

        self._hide_error()
