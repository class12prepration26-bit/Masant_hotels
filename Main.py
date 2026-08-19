from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, RoundedRectangle
from datetime import datetime
import random


class Card(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.12, 0.12, 0.12, 1)

            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[18]
            )

        self.bind(
            pos=self.update_bg,
            size=self.update_bg
        )

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class HomeScreen(Screen):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app

        layout = BoxLayout(
            orientation="vertical",
            padding=30,
            spacing=15
        )

        layout.add_widget(Label(
            text="🍴",
            font_size=55,
            size_hint_y=None,
            height=70
        ))

        layout.add_widget(Label(
            text="MASANT HOTELS",
            font_size=36,
            bold=True
        ))

        layout.add_widget(Label(
            text="Delicious Food • Happy Moments",
            font_size=18
        ))

        menu = Button(
            text="🍕  EXPLORE MENU",
            font_size=21,
            size_hint_y=None,
            height=65
        )

        menu.bind(
            on_press=lambda x:
            self.app.show_menu()
        )

        layout.add_widget(menu)

        history = Button(
            text="📋  ORDER HISTORY",
            font_size=19,
            size_hint_y=None,
            height=60
        )

        history.bind(
            on_press=lambda x:
            self.app.show_history()
        )

        layout.add_widget(history)

        self.add_widget(layout)


class MenuScreen(Screen):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app

        self.layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        header = BoxLayout(
            size_hint_y=None,
            height=60
        )

        header.add_widget(Label(
            text="🍴 MENU",
            font_size=30,
            bold=True
        ))

        self.cart_button = Button(
            text="🛒 0",
            size_hint_x=None,
            width=100
        )

        self.cart_button.bind(
            on_press=lambda x:
            self.app.show_cart()
        )

        header.add_widget(self.cart_button)

        self.layout.add_widget(header)

        self.menu = GridLayout(
            cols=2,
            spacing=12,
            padding=5
        )

        self.layout.add_widget(self.menu)

        home = Button(
            text="🏠 HOME",
            size_hint_y=None,
            height=55
        )

        home.bind(
            on_press=lambda x:
            self.app.show_home()
        )

        self.layout.add_widget(home)

        self.add_widget(self.layout)

        self.build_menu()

    def build_menu(self):

        self.menu.clear_widgets()

        for item, price in self.app.prices.items():

            card = Card(
                orientation="vertical",
                padding=10,
                spacing=5
            )

            card.add_widget(Label(
                text="🍽️",
                font_size=28,
                size_hint_y=None,
                height=40
            ))

            card.add_widget(Label(
                text=item,
                font_size=21,
                bold=True
            ))

            card.add_widget(Label(
                text=f"₹{price}",
                font_size=18
            ))

            add = Button(
                text="ADD +",
                size_hint_y=None,
                height=42
            )

            add.bind(
                on_press=lambda x, i=item:
                self.app.add_item(i)
            )

            card.add_widget(add)

            self.menu.add_widget(card)

    def refresh(self):

        count = sum(
            self.app.cart.values()
        )

        self.cart_button.text = f"🛒 {count}"


class CartScreen(Screen):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app

        self.layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=8
        )

        self.add_widget(self.layout)

    def refresh(self):

        self.layout.clear_widgets()

        self.layout.add_widget(Label(
            text="🛒 YOUR CART",
            font_size=30,
            bold=True,
            size_hint_y=None,
            height=60
        ))

        if not self.app.cart:

            self.layout.add_widget(Label(
                text="Your cart is empty!",
                font_size=22
            ))

        else:

            for item, quantity in list(
                self.app.cart.items()
            ):

                row = BoxLayout(
                    size_hint_y=None,
                    height=65,
                    spacing=5
                )

                price = self.app.prices[item]

                row.add_widget(Label(
                    text=f"{item}\n₹{price}",
                    font_size=17
                ))

                minus = Button(
                    text="−",
                    size_hint_x=None,
                    width=45
                )

                minus.bind(
                    on_press=lambda x, i=item:
                    self.app.remove_one(i)
                )

                row.add_widget(minus)

                row.add_widget(Label(
                    text=str(quantity),
                    font_size=20,
                    size_hint_x=None,
                    width=40
                ))

                plus = Button(
                    text="+",
                    size_hint_x=None,
                    width=45
                )

                plus.bind(
                    on_press=lambda x, i=item:
                    self.app.add_item(i)
                )

                row.add_widget(plus)

                remove = Button(
                    text="REMOVE",
                    size_hint_x=None,
                    width=90
                )

                remove.bind(
                    on_press=lambda x, i=item:
                    self.app.remove_item(i)
                )

                row.add_widget(remove)

                self.layout.add_widget(row)

        self.layout.add_widget(Label(
            text=f"TOTAL: ₹{self.app.get_total()}",
            font_size=27,
            bold=True,
            size_hint_y=None,
            height=60
        ))

        buttons = BoxLayout(
            size_hint_y=None,
            height=58,
            spacing=8
        )

        menu = Button(text="🍕 MENU")
        menu.bind(
            on_press=lambda x:
            self.app.show_menu()
        )

        clear = Button(text="CLEAR")
        clear.bind(
            on_press=lambda x:
            self.app.clear_cart()
        )

        order = Button(text="ORDER")
        order.bind(
            on_press=lambda x:
            self.app.show_customer()
        )

        buttons.add_widget(menu)
        buttons.add_widget(clear)
        buttons.add_widget(order)

        self.layout.add_widget(buttons)


class CustomerScreen(Screen):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app

        layout = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=15
        )

        layout.add_widget(Label(
            text="👤 CUSTOMER DETAILS",
            font_size=29,
            bold=True
        ))

        self.name_input = TextInput(
            hint_text="Customer name",
            multiline=False,
            font_size=18,
            size_hint_y=None,
            height=55
        )

        self.mobile_input = TextInput(
            hint_text="Mobile number",
            multiline=False,
            input_filter="int",
            font_size=18,
            size_hint_y=None,
            height=55
        )

        layout.add_widget(self.name_input)
        layout.add_widget(self.mobile_input)

        self.total = Label(
            text="TOTAL: ₹0",
            font_size=27,
            bold=True
        )

        layout.add_widget(self.total)

        confirm = Button(
            text="✅ CONFIRM ORDER",
            font_size=20,
            size_hint_y=None,
            height=62
        )

        confirm.bind(
            on_press=lambda x:
            self.app.confirm_order()
        )

        layout.add_widget(confirm)

        back = Button(
            text="🔙 CART",
            size_hint_y=None,
            height=50
        )

        back.bind(
            on_press=lambda x:
            self.app.show_cart()
        )

        layout.add_widget(back)

        self.add_widget(layout)

    def refresh(self):

        self.total.text = (
            f"TOTAL: ₹{self.app.get_total()}"
        )


class ReceiptScreen(Screen):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app

    def show_receipt(self, order_id, total):

        self.clear_widgets()

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=8
        )

        layout.add_widget(Label(
            text="🧾 MASANT HOTELS",
            font_size=30,
            bold=True
        ))

        layout.add_widget(Label(
            text="ORDER RECEIPT",
            font_size=21,
            bold=True
        ))

        now = datetime.now().strftime(
            "%d-%m-%Y  %I:%M %p"
        )

        details = (
            f"Order ID: {order_id}\n"
            f"Customer: {self.app.customer_name}\n"
            f"Mobile: {self.app.customer_mobile}\n"
            f"Date: {now}"
        )

        layout.add_widget(Label(
            text=details,
            font_size=16
        ))

        layout.add_widget(Label(
            text="--------------------------"
        ))

        for item, quantity in (
            self.app.last_order.items()
        ):

            price = (
                self.app.prices[item] *
                quantity
            )

            layout.add_widget(Label(
                text=f"{item} × {quantity} = ₹{price}",
                font_size=18
            ))

        layout.add_widget(Label(
            text=f"FINAL BILL: ₹{total}",
            font_size=28,
            bold=True
        ))

        layout.add_widget(Label(
            text="Thank you for visiting Masant Hotels! ❤️",
            font_size=17
        ))

        new_order = Button(
            text="🍕 NEW ORDER",
            size_hint_y=None,
            height=60
        )

        new_order.bind(
            on_press=lambda x:
            self.app.show_menu()
        )

        layout.add_widget(new_order)

        history = Button(
            text="📋 ORDER HISTORY",
            size_hint_y=None,
            height=55
        )

        history.bind(
            on_press=lambda x:
            self.app.show_history()
        )

        layout.add_widget(history)

        home = Button(
            text="🏠 HOME",
            size_hint_y=None,
            height=55
        )

        home.bind(
            on_press=lambda x:
            self.app.show_home()
        )

        layout.add_widget(home)

        self.add_widget(layout)


class HistoryScreen(Screen):

    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.app = app

        self.layout = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        self.add_widget(self.layout)

    def refresh(self):

        self.layout.clear_widgets()

        self.layout.add_widget(Label(
            text="📋 ORDER HISTORY",
            font_size=30,
            bold=True,
            size_hint_y=None,
            height=60
        ))

        if not self.app.order_history:

            self.layout.add_widget(Label(
                text="No orders yet.",
                font_size=22
            ))

        else:

            for order in reversed(
                self.app.order_history
            ):

                items_text = ""

                for item, quantity in (
                    order["items"].items()
                ):

                    items_text += (
                        f"{item} × {quantity}, "
                    )

                card = Card(
                    orientation="vertical",
                    padding=10,
                    spacing=3,
                    size_hint_y=None,
                    height=125
                )

                card.add_widget(Label(
                    text=(
                        f"Order ID: {order['order_id']}\n"
                        f"Customer: {order['name']}\n"
                        f"Items: {items_text}\n"
                        f"Total: ₹{order['total']}"
                    ),
                    font_size=16
                ))

                self.layout.add_widget(card)

        back = Button(
            text="🏠 HOME",
            size_hint_y=None,
            height=55
        )

        back.bind(
            on_press=lambda x:
            self.app.show_home()
        )

        self.layout.add_widget(back)


class MasantHotels(App):

    def build(self):

        self.cart = {}

        self.prices = {
            "Pizza": 200,
            "Burger": 100,
            "Sandwich": 150,
            "Coffee": 100
        }

        self.customer_name = ""
        self.customer_mobile = ""

        self.last_order = {}

        # Order History
        self.order_history = []

        self.sm = ScreenManager()

        self.sm.add_widget(
            HomeScreen(
                self,
                name="home"
            )
        )

        self.sm.add_widget(
            MenuScreen(
                self,
                name="menu"
            )
        )

        self.sm.add_widget(
            CartScreen(
                self,
                name="cart"
            )
        )

        self.sm.add_widget(
            CustomerScreen(
                self,
                name="customer"
            )
        )

        self.sm.add_widget(
            ReceiptScreen(
                self,
                name="receipt"
            )
        )

        self.sm.add_widget(
            HistoryScreen(
                self,
                name="history"
            )
        )

        return self.sm

    def show_home(self):

        self.sm.current = "home"

    def show_menu(self):

        self.sm.get_screen(
            "menu"
        ).refresh()

        self.sm.current = "menu"

    def show_cart(self):

        self.sm.get_screen(
            "cart"
        ).refresh()

        self.sm.current = "cart"

    def show_customer(self):

        if not self.cart:
            return

        self.sm.get_screen(
            "customer"
        ).refresh()

        self.sm.current = "customer"

    def show_history(self):

        self.sm.get_screen(
            "history"
        ).refresh()

        self.sm.current = "history"

    def add_item(self, item):

        if item in self.cart:
            self.cart[item] += 1
        else:
            self.cart[item] = 1

        self.refresh_screens()

    def remove_one(self, item):

        if item not in self.cart:
            return

        self.cart[item] -= 1

        if self.cart[item] <= 0:
            del self.cart[item]

        self.refresh_screens()

    def remove_item(self, item):

        if item in self.cart:
            del self.cart[item]

        self.refresh_screens()

    def clear_cart(self):

        self.cart.clear()

        self.refresh_screens()

    def refresh_screens(self):

        self.sm.get_screen(
            "menu"
        ).refresh()

        self.sm.get_screen(
            "cart"
        ).refresh()

    def get_total(self):

        return sum(
            self.prices[item] * quantity
            for item, quantity
            in self.cart.items()
        )

    def confirm_order(self):

        customer = self.sm.get_screen(
            "customer"
        )

        name = customer.name_input.text.strip()

        mobile = customer.mobile_input.text.strip()

        if not name:
            return

        if not mobile:
            return

        self.customer_name = name
        self.customer_mobile = mobile

        total = self.get_total()

        self.last_order = self.cart.copy()

        order_id = "MH" + str(
            random.randint(10000, 99999)
        )

        # Save order to history
        self.order_history.append({
            "order_id": order_id,
            "name": self.customer_name,
            "mobile": self.customer_mobile,
            "items": self.last_order.copy(),
            "total": total
        })

        self.sm.get_screen(
            "receipt"
        ).show_receipt(
            order_id,
            total
        )

        self.cart.clear()

        self.sm.current = "receipt"


MasantHotels().run()
