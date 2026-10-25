import os
import tkinter as tk
from tkinter import messagebox, ttk


#  คลาสต้นแบบสินค้า (OOP)
class Product:

    def __init__(self, name, price, type_name, stock):
        self.name = str(name)
        self.price = float(price)
        self.type = str(type_name)
        self.stock = int(stock)


# คลาสหลักสำหรับหน้าต่างโปรแกรม (UI)
class ShopApp:

    def __init__(self, root):
        self.root = root
        self.root.title("ระบบจัดการร้านค้า (Shop Management System)")
        self.root.geometry("750x550")
        self.root.configure(bg="#f5f5f5")

        # จัดเก็บข้อมูลด้วย List และตั้งชื่อไฟล์ข้อความ
        self.items = []
        self.file_path = "products.txt"

        # ดึงข้อมูลจากไฟล์ข้อความมาใส่ในระบบเมื่อเปิดโปรแกรม
        self.load_from_file()

        # สร้างส่วนแสดงผลหน้าจอ
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        # หัวข้อ
        tk.Label(
            self.root,
            text="ระบบจัดการร้านค้า (Shop Management System)",
            font=("Arial", 14, "bold"),
            bg="#f5f5f5",
        ).pack(pady=10)

        # ฟอร์มรับข้อมูล (Grid)
        form = tk.LabelFrame(
            self.root,
            text=" ข้อมูลสินค้า ",
            font=("Arial", 10, "bold"),
            bg="#f5f5f5",
            padx=10,
            pady=10,
        )
        form.pack(fill="x", padx=20, pady=5)

        tk.Label(form, text="ชื่อสินค้า:", bg="#f5f5f5").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.ent_name = tk.Entry(form, width=20)
        self.ent_name.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="ราคาสินค้า:", bg="#f5f5f5").grid(
            row=0, column=2, padx=5, pady=5, sticky="e"
        )
        self.ent_price = tk.Entry(form, width=15)
        self.ent_price.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form, text="ประเภท:", bg="#f5f5f5").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.ent_type = tk.Entry(form, width=20)
        self.ent_type.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="จำนวนในคลัง:", bg="#f5f5f5").grid(
            row=1, column=2, padx=5, pady=5, sticky="e"
        )
        self.ent_stock = tk.Entry(form, width=15)
        self.ent_stock.grid(row=1, column=3, padx=5, pady=5)

        # แผงควบคุมปุ่มกดฟังก์ชัน (Button Panel)
        btn_frame = tk.Frame(self.root, bg="#f5f5f5")
        btn_frame.pack(fill="x", padx=20, pady=10)

        tk.Button(
            btn_frame,
            text="เพิ่มสินค้า",
            bg="#4CAF50",
            fg="white",
            width=10,
            command=self.add_item,
        ).grid(row=0, column=0, padx=5)
        tk.Button(
            btn_frame,
            text="ลบสินค้า",
            bg="#f44336",
            fg="white",
            width=10,
            command=self.delete_item,
        ).grid(row=0, column=1, padx=5)
        tk.Button(
            btn_frame,
            text="แก้ไขสินค้า",
            bg="#FF9800",
            fg="white",
            width=12,
            command=self.edit_item,
        ).grid(row=0, column=2, padx=5)
        tk.Button(
            btn_frame,
            text="ค้นหาสินค้า",
            bg="#2196F3",
            fg="white",
            width=10,
            command=self.search_item,
        ).grid(row=0, column=3, padx=5)
        tk.Button(
            btn_frame,
            text="แสดงทั้งหมด",
            bg="#9E9E9E",
            fg="white",
            width=12,
            command=self.refresh_table,
        ).grid(row=0, column=4, padx=5)

        # ตารางแสดงรายการสินค้า (Treeview)
        t_frame = tk.Frame(self.root)
        t_frame.pack(fill="both", expand=True, padx=20, pady=5)

        cols = ("name", "price", "type", "stock")
        self.tree = ttk.Treeview(t_frame, columns=cols, show="headings")
        self.tree.heading("name", text="ชื่อสินค้า")
        self.tree.heading("price", text="ราคา (บาท)")
        self.tree.heading("type", text="ประเภท")
        self.tree.heading("stock", text="จำนวนคงเหลือ")

        self.tree.column("name", width=180)
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("type", width=120, anchor="center")
        self.tree.column("stock", width=100, anchor="e")

        scroll = ttk.Scrollbar(
            t_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    # ฟังก์ชันเพิ่มสินค้า
    def add_item(self):
        name = self.ent_name.get().strip()
        price = self.ent_price.get().strip()
        type_name = self.ent_type.get().strip()
        stock = self.ent_stock.get().strip()

        if not (name and price and type_name and stock):
            messagebox.showwarning("แจ้งเตือน", "กรุณากรอกข้อมูลให้ครบทุกช่อง")
            return
        try:
            new_item = Product(name, price, type_name, stock)
            self.items.append(new_item)
            self.save_to_file()
            self.refresh_table()
            self.clear_form()
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "ราคาและจำนวนต้องเป็นตัวเลข")

    # ฟังก์ชันลบสินค้า
    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกสินค้าที่จะลบ")
            return
        item_data = self.tree.item(selected)["values"]
        for index, item in enumerate(self.items):
            if item.name == str(item_data[0]):
                self.items.pop(index)
                break
        self.save_to_file()
        self.refresh_table()
        self.clear_form()

    # ฟังก์ชันแก้ไขสินค้า
    def edit_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกสินค้าที่จะแก้ไข")
            return
        item_data = self.tree.item(selected)["values"]
        name = self.ent_name.get().strip()
        price = self.ent_price.get().strip()
        type_name = self.ent_type.get().strip()
        stock = self.ent_stock.get().strip()

        try:
            for item in self.items:
                if item.name == str(item_data[0]):
                    item.name = name
                    item.price = float(price)
                    item.type = type_name
                    item.stock = int(stock)
                    break
            self.save_to_file()
            self.refresh_table()
            self.clear_form()
        except ValueError:
            messagebox.showerror("ข้อผิดพลาด", "ราคาและจำนวนต้องเป็นตัวเลข")

    # ฟังก์ชันค้นหาสินค้า
    def search_item(self):
        keyword = self.ent_name.get().strip()
        if not keyword:
            messagebox.showwarning("แจ้งเตือน", "กรุณาใส่ชื่อสินค้าเพื่อค้นหา")
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.items:
            if keyword.lower() in item.name.lower():
                self.tree.insert(
                    "",
                    "end",
                    values=(item.name, f"{item.price:.2f}", item.type, item.stock),
                )

    # ฟังก์ชันรีเฟรชตารางแสดงผลทั้งหมด
    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in self.items:
            self.tree.insert(
                "",
                "end",
                values=(item.name, f"{item.price:.2f}", item.type, item.stock),
                )

    # บันทึกข้อมูลลง Text File 
    def save_to_file(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            for item in self.items:
                f.write(f"{item.name}||{item.price}||{item.type}||{item.stock}\n")

    # อ่านข้อมูลจาก Text File 
    def load_from_file(self):
        if not os.path.exists(self.file_path):
            return
        try:
            self.items.clear()
            with open(self.file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and "||" in line:
                        p = line.split("||")
                        if len(p) == 4:
                            self.items.append(Product(p[0], p[1], p[2], p[3]))
        except Exception as e:
            print(f"Error: {e}")

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        data = self.tree.item(selected)["values"]
        self.clear_form()
        self.ent_name.insert(0, data[0])
        self.ent_price.insert(0, data[1])
        self.ent_type.insert(0, data[2])
        self.ent_stock.insert(0, data[3])

    def clear_form(self):
        self.ent_name.delete(0, tk.END)
        self.ent_price.delete(0, tk.END)
        self.ent_type.delete(0, tk.END)
        self.ent_stock.delete(0, tk.END)


if __name__ == "__main__":
    root_window = tk.Tk()
    app = ShopApp(root_window)
    root_window.mainloop()
