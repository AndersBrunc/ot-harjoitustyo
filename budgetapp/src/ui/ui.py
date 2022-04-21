from ui.login import LoginView
from ui.create_user import CreateUserView
from ui.budget_view import BudgetView
from ui.view_history import PurchaseView
from ui.create_budget import CreateBudgetView
from ui.add_purchase_view import AddPurchaseView

from tkinter import Tk, ttk


class UI:

    def __init__(self, root):
        self._root = root
        self._current_view = None

    def start(self):
        self._show_login_view()

    def _hide_current_view(self):
        if self._current_view:
            self._current_view.destroy()

        self._current_view = None

    def _show_login_view(self):
        self._hide_current_view()

        self._current_view = LoginView(
            self._root,
            self._show_budget_view,
            self._show_create_user_view
        )
        self._current_view.pack()

    def _show_purchase_history_view(self):
        self._hide_current_view()

        self._current_view = PurchaseView(
            self._root,
            self._show_budget_view
        )
        self._current_view.pack()

    def _show_budget_view(self):
        self._hide_current_view()

        self._current_view = BudgetView(
            self._root,
            self._show_login_view,
            self._show_purchase_history_view,
            self._show_create_budget_view,
            self._show_add_purchase_view
        )
        self._current_view.pack()

    def _show_create_user_view(self):
        self._hide_current_view()

        self._current_view = CreateUserView(
            self._root,
            self._show_budget_view,
            self._show_login_view
        )
        self._current_view.pack()

    def _show_create_budget_view(self):
        self._hide_current_view()

        self._current_view = CreateBudgetView(
            self._root,
            self._show_budget_view
        )
        self._current_view.pack()

    def _show_add_purchase_view(self):
        self._hide_current_view()

        self._current_view = AddPurchaseView(
            self._root,
            self._show_budget_view
        )
