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
    def __init__(self, cart):
        super().__init__()

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

        self.cart = cart

        self.title("Smart Cart Display")
        self.geometry("1100x600")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)

        self._build_layout()
        self.refresh()

    # ---------------- LAYOUT ----------------
    def _build_layout(self):
        # Header
        header = tk.Frame(self, bg="#020617")
        header.pack(fill="x", padx=20, pady=10)

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

        # Body
        body = tk.Frame(self, bg=BG_COLOR)
        body.pack(fill="both", expand=True, padx=20)

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

        self.cam_label = tk.Label(
            right,
            bg="black",
            width=320,
            height=240
        )
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

        # Footer
        footer = tk.Frame(self, bg="#020617")
        footer.pack(fill="x", padx=20, pady=10)

        self.total_label = tk.Label(
            footer,
            text="TOTAL: ₹0.00",
            font=FONT_L,
            fg=ACCENT,
            bg="#020617"
        )
        self.total_label.pack(side="right")

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
        tk.Button(
            container,
            text="END",
            command=self.destroy,
            width=10
        ).pack(pady=10)
