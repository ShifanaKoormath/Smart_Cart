"""
Smart Cart – On-Cart UI Screen (FINAL, CORRECT VERSION)
=====================================================

Features:
- Cart item list (authoritative from backend Cart)
- Last action display (ADD / REMOVE / REJECT)
- Confidence display
- Camera frame display (backend-owned camera)
- Final bill screen at demo end

ARCHITECTURE GUARANTEES:
- UI makes NO decisions
- UI does NOT open the camera
- UI only displays data pushed from backend
"""
import qrcode
import random

import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

# ---------------- UI CONFIG ----------------
BG_COLOR = "#0f172a"
FG_COLOR = "#e5e7eb"
ACCENT = "#22c55e"
WARN = "#f59e0b"
ERROR = "#ef4444"

FONT_L = ("Segoe UI", 20, "bold")
FONT_M = ("Segoe UI", 14)
FONT_S = ("Segoe UI", 11)


class SmartCartUI(tk.Tk):
    def __init__(self, cart, on_shutdown=None):
        super().__init__()
        self.cart = cart
        self.on_shutdown = on_shutdown

        # ---------- Treeview styling ----------
        style = ttk.Style(self)
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#020617",
            foreground=FG_COLOR,
            rowheight=32,
            fieldbackground="#020617",
            borderwidth=0,
            font=FONT_S
        )

        style.configure(
            "Treeview.Heading",
            background="#020617",
            foreground=ACCENT,
            font=("Segoe UI", 11, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#1e293b")]
        )

        self.view_mode = "CART"
        self.payment_qr_generated = False
        self.payment_success = False
        self.current_txn_id = None

        self.title("Smart Cart Display")
        self.geometry("1100x600")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        self._build_layout()
        self.refresh()

    def _build_layout(self):
        # Root grid config
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ---------- HEADER (row 0) ----------
        header = tk.Frame(self, bg="#020617")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

        tk.Label(
            header,
            text="🛒 SMART CART",
            font=FONT_L,
            fg=ACCENT,
            bg="#020617"
        ).pack(side="left")

        self.status_label = tk.Label(
            header,
            text="SYSTEM READY",
            font=FONT_S,
            fg=FG_COLOR,
            bg="#020617"
        )
        self.status_label.pack(side="right")

        # ---------- BODY (row 1 – expandable) ----------
        body = tk.Frame(self, bg=BG_COLOR)
        body.grid(row=1, column=0, sticky="nsew", padx=20)

        # LEFT: Cart table
        left = tk.Frame(body, bg=BG_COLOR)
        left.pack(side="left", fill="both", expand=True)

        columns = ("name", "qty_wt", "price")
        self.tree = ttk.Treeview(left, columns=columns, show="headings", height=12)

        self.tree.heading("name", text="Item")
        self.tree.heading("qty_wt", text="Qty / Weight")
        self.tree.heading("price", text="Subtotal (₹)")

        self.tree.column("name", width=260)
        self.tree.column("qty_wt", width=150, anchor="center")
        self.tree.column("price", width=150, anchor="e")

        self.tree.pack(fill="both", expand=True)

        # RIGHT: Status panel
        right = tk.Frame(body, bg="#020617")
        right.pack(side="right", fill="y", padx=15)

        self.cam_label = tk.Label(right, bg="black", width=320, height=240)
        self.cam_label.pack(pady=(12, 8))

        self.action_label = tk.Label(
            right,
            text="Last Action: -",
            font=("Segoe UI", 15, "bold"),
            fg=ACCENT,
            bg="#020617"
        )
        self.action_label.pack(anchor="w", padx=10, pady=(8, 4))

        self.conf_label = tk.Label(
            right,
            text="Confidence: -",
            font=FONT_S,
            fg=FG_COLOR,
            bg="#020617"
        )
        self.conf_label.pack(anchor="w", padx=10)

        # ---------- FOOTER (row 2 – FIXED) ----------
        self.footer = tk.Frame(self, bg="#020617")
        self.footer.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        self.checkout_btn = tk.Button(
            self.footer,
            text="Proceed to Bill",
            font=FONT_M,
            bg=ACCENT,
            fg="black",
            padx=16,
            pady=6,
            command=self.show_final_bill
        )
        self.checkout_btn.pack(side="left")

        self.total_label = tk.Label(
            self.footer,
            text="TOTAL: ₹0.00",
            font=FONT_L,
            fg=ACCENT,
            bg="#020617"
        )
        self.total_label.pack(side="right")

        
    def show_cart_view(self):
        """
        Restore the main cart UI view.
        Cart data is preserved.
        """
        self.view_mode = "CART"

        for widget in self.winfo_children():
            widget.destroy()

        self._build_layout()
        self.refresh()

        
      
    # ---------------- BACKEND → UI HOOKS ----------------
    def update_event(self, action, confidence=None, product_name=None):
        if action == "ADD" and product_name:
            text, color = f"Added {product_name}", ACCENT
        elif action == "REMOVE" and product_name:
            text, color = f"Removed {product_name}", WARN
        elif action == "REJECT":
            text, color = "Rejected (low confidence)", ERROR
        else:
            text, color = action, FG_COLOR

        self.action_label.config(text=f"Last Action: {text}", fg=color)

        if confidence is not None:
            self.conf_label.config(text=f"Confidence: {confidence:.2f}")
        else:
            self.conf_label.config(text="Confidence: -")

    def update_frame(self, frame):
        if frame is None:
            return

        frame = cv2.resize(frame, (320, 240))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        self.cam_label.configure(image=img)
        self.cam_label.image = img

    def refresh(self):
        if self.view_mode != "CART":
            return
        self.tree.delete(*self.tree.get_children())

        if not self.cart.items:
            self.status_label.config(text="Cart empty", fg=WARN)
            self.tree.insert("", "end", values=("— No items in cart —", "", ""))
        else:
            self.status_label.config(text="Cart updated", fg=ACCENT)

            for item in self.cart.items.values():
                qty = (
                    f"{item.quantity} unit(s)"
                    if item.product.price_per_unit is not None
                    else f"{item.weight} g"
                )
                self.tree.insert(
                    "",
                    "end",
                    values=(item.product.name, qty, f"₹{item.subtotal:.2f}")
                )

        self.total_label.config(text=f"TOTAL: ₹{self.cart.total():.2f}")


    # ---------------- FINAL BILL SCREEN ----------------
    def show_final_bill(self):
        self.view_mode = "BILL"

        # Clear existing UI
        for widget in self.winfo_children():
            widget.destroy()

        # Container for centering content
        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(expand=True)

        # Title
        tk.Label(
            container,
            text="FINAL BILL",
            font=FONT_L,
            fg=ACCENT,
            bg=BG_COLOR
        ).pack(pady=(10, 20))

        # Items
        items_frame = tk.Frame(container, bg=BG_COLOR)
        items_frame.pack(pady=10)

        for item in self.cart.items.values():
            if item.product.price_per_unit is not None:
                line = f"{item.product.name:<20}  x{item.quantity:<2}   ₹{item.subtotal:.2f}"
            else:
                line = f"{item.product.name:<20}  {item.weight}g   ₹{item.subtotal:.2f}"

            tk.Label(
                items_frame,
                text=line,
                font=FONT_M,
                fg=FG_COLOR,
                bg=BG_COLOR,
                anchor="w"
            ).pack(anchor="w", padx=20)

        # Divider
        tk.Label(
            container,
            text="—" * 30,
            fg=FG_COLOR,
            bg=BG_COLOR
        ).pack(pady=10)

        # Total
        tk.Label(
            container,
            text=f"TOTAL: ₹{self.cart.total():.2f}",
            font=FONT_L,
            fg=ACCENT,
            bg=BG_COLOR
        ).pack(pady=15)

        # Closing note
        tk.Label(
            container,
            text="Thank you for using Smart Cart",
            font=FONT_S,
            fg=FG_COLOR,
            bg=BG_COLOR
        ).pack(pady=(5, 15))

        # End button
        btns = tk.Frame(container, bg=BG_COLOR)
        btns.pack(pady=10)

        tk.Button(
            btns,
            text="Back to Cart",
            font=FONT_M,
            command=self.show_cart_view,
            width=12
        ).pack(side="left", padx=10)

        tk.Button(
            btns,
            text="Pay Now",
            font=FONT_M,
            bg=ACCENT,
            fg="black",
            command=self.show_payment_view,
            width=10
        ).pack(side="right", padx=10)

    def show_payment_view(self):
        self.view_mode = "PAYMENT"
        self.payment_qr_generated = True
        self.payment_success = False

        # Generate transaction ID
        self.current_txn_id = f"TXN-{random.randint(100000, 999999)}"

        for widget in self.winfo_children():
            widget.destroy()

        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(expand=True)

        tk.Label(
            container,
            text="PAYMENT",
            font=FONT_L,
            fg=ACCENT,
            bg=BG_COLOR
        ).pack(pady=(10, 15))

        tk.Label(
            container,
            text=f"Amount to Pay: ₹{self.cart.total():.2f}",
            font=FONT_M,
            fg=FG_COLOR,
            bg=BG_COLOR
        ).pack(pady=5)

        # ---- Generate QR ----
        qr_data = f"SMARTCART|{self.current_txn_id}|AMT:{self.cart.total():.2f}"
        qr = qrcode.make(qr_data)
        qr = qr.resize((200, 200))

        self.qr_img = ImageTk.PhotoImage(qr)

        qr_label = tk.Label(container, image=self.qr_img, bg=BG_COLOR)
        qr_label.pack(pady=15)

        tk.Label(
            container,
            text=f"Transaction ID: {self.current_txn_id}",
            font=FONT_S,
            fg="#38bdf8",
            bg=BG_COLOR
        ).pack(pady=5)

        tk.Label(
            container,
            text="Scan & Pay using UPI\n(Demo QR – Payment Simulation)",
            font=FONT_S,
            fg="#38bdf8",
            bg=BG_COLOR
        ).pack(pady=10)

        self.payment_status_label = tk.Label(
            container,
            text="Status: Waiting for payment",
            font=FONT_M,
            fg=WARN,
            bg=BG_COLOR
        )
        self.payment_status_label.pack(pady=10)

        btns = tk.Frame(container, bg=BG_COLOR)
        btns.pack(pady=15)

        tk.Button(
            btns,
            text="Confirm Payment (Demo)",
            font=FONT_M,
            bg=ACCENT,
            fg="black",
            command=self.confirm_payment,
            width=18
        ).pack(side="left", padx=10)

        tk.Button(
            btns,
            text="Cancel",
            font=FONT_M,
            command=self.show_cart_view,
            width=10
        ).pack(side="right", padx=10)
        tk.Button(
            container,
            text="Proceed to Exit Gate",
            font=FONT_M,
            bg="#38bdf8",      # INFO blue
            fg="black",
            padx=16,
            pady=6,
            command=self.show_exit_verification
        ).pack(pady=(10, 0))

    def confirm_payment(self):
        self.payment_success = True

        self.payment_status_label.config(
            text="✅ Payment Successful",
            fg=ACCENT
        
        )
        # Immediate transition (no delay, no race conditions)
        self.show_exit_verification()
    def show_exit_verification(self):
        self.view_mode = "EXIT"

        for widget in self.winfo_children():
            widget.destroy()

        container = tk.Frame(self, bg=BG_COLOR)
        container.pack(expand=True)

        tk.Label(
            container,
            text="EXIT GATE VERIFICATION",
            font=FONT_L,
            fg=ACCENT,
            bg=BG_COLOR
        ).pack(pady=(10, 20))

        if self.payment_success:
            tk.Label(
                container,
                text=f"Payment VERIFIED\nTransaction: {self.current_txn_id}",
                font=FONT_M,
                fg=FG_COLOR,
                bg=BG_COLOR
            ).pack(pady=10)

            status = tk.Label(
                container,
                text="🟢 Gate Open\nPlease proceed",
                font=FONT_M,
                fg=ACCENT,
                bg=BG_COLOR
            )
            status.pack(pady=20)

        else:
            tk.Label(
                container,
                text="⚠️ PAYMENT NOT VERIFIED\nUnpaid items detected",
                font=FONT_M,
                fg=ERROR,
                bg=BG_COLOR
            ).pack(pady=15)

            tk.Label(
                container,
                text="🔒 Gate Locked",
                font=FONT_M,
                fg=ERROR,
                bg=BG_COLOR
            ).pack(pady=10)

        btns = tk.Frame(container, bg=BG_COLOR)
        btns.pack(pady=25)

        if not self.payment_success:
            tk.Button(
                btns,
                text="Go to Payment",
                font=FONT_M,
                command=self.show_payment_view,
                width=14
            ).pack(side="left", padx=10)

        tk.Button(
            btns,
            text="New Cart",
            font=FONT_M,
            command=self.start_new_cart,
            width=12
        ).pack(side="left", padx=10)

        tk.Button(
            btns,
            text="End Demo",
            font=FONT_M,
            command=self.end_demo,
            width=10
        ).pack(side="right", padx=10)
    def start_new_cart(self):
        """
        Starts a fresh shopping session.
        """
        self.cart.reset()

        # Reset payment state
        self.payment_qr_generated = False
        self.payment_success = False
        self.current_txn_id = None

        self.show_cart_view()
    def end_demo(self):
        if self.on_shutdown:
            self.on_shutdown()
        self.destroy()

       