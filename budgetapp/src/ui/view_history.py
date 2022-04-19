from tkinter import ttk, constants
from service.budgetapp_service import budgetapp_service

class PurchaseView:
    def __init__(self, root, handle_logout, handle_show_budget_view):
        self._root = root
        self._handle_logout = handle_logout
        self._handle_show_budget_view = handle_show_budget_view

        self._frame = None

        