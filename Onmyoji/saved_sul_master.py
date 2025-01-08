from multiprocessing import Pool
import tkinter as tk
from tkinter import ttk, simpledialog
from PIL import Image, ImageTk
from Onmyoji_SOul import Soul,boost

class SoulMaster:
    def __init__(self, master):
        self.master = master
        self.master.title("Onmyoji Soul Master")
        self.souls = []

        self.master.geometry("750x600")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - 750) // 2
        y = (screen_height - 600) // 2
        self.master.geometry(f"+{x}+{y}")
        self.init_ui()

    def init_ui(self):
        button_frame = ttk.Frame(self.master)
        button_frame.pack(side=tk.BOTTOM, pady=10)
    
        self.help_button = ttk.Button(button_frame, text="Help", command=self.show_help)
        self.help_button.pack(side=tk.LEFT, padx=5)

        self.init_souls_button = ttk.Button(button_frame, text="Initialize Souls", command=self.initialize_souls)
        self.init_souls_button.pack(side=tk.LEFT, padx=5)

        self.warehouse_button = ttk.Button(button_frame, text="Warehouse", command=self.display_souls)
        self.warehouse_button.pack(side=tk.LEFT, padx=5)

        self.hide_souls_button = ttk.Button(button_frame, text="Hide Souls", command=self.hide_souls)
        self.hide_souls_button.pack(side=tk.LEFT, padx=5)
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame)
        self.scroll_y = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scroll_x = ttk.Scrollbar(self.frame, orient="horizontal", command=self.canvas.xview)

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")


    def initialize_souls(self):
        integer = tk.simpledialog.askinteger("Input", "Enter the number of souls to initialize:", parent=self.master)
        if integer is None:
            return
        if integer > 100 or (integer + len(self.souls)) > 100:
            tk.messagebox.showwarning("Warning", "Your warehouse doesn't have enough space!")
            return
        if integer < 0:
            tk.messagebox.showwarning("Warning", "Invalid input!")
            return
        tmp = [Soul() for _ in range(integer)]
        self.souls += tmp
        

    def display_souls(self):
        if not self.souls:
            tk.messagebox.showwarning("Warning", "No souls available. Please initialize some souls first.")
            return
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
       
        # Create a counter for horizontal items
        items_per_row = 6
        item_count = 0

        for soul in self.souls:
            frame = ttk.Frame(self.scrollable_frame, borderwidth=2, relief="groove")
            frame.grid(row=item_count // items_per_row, column=item_count % items_per_row, padx=5, pady=5)
            item_count += 1

            filename = "_".join(soul.name.split(' '))
            img = Image.open(f"./img/{filename}.png")
            img = img.resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)

            label = tk.Label(frame, image=photo)
            label.image = photo
            label.pack()
            
            label.bind("<Button-1>", lambda e, s=soul: self.on_soul_click(e, s))

            label.bind("<Enter>", lambda e, s=soul: self.show_soul_info(e, s))
            label.bind("<Leave>", self.hide_soul_info)
    

    def hide_souls(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def show_soul_info(self, event, soul):
        info = f"Name: {soul.name}\nSlot: {soul.slot}  Level:{soul.level}\nPrime: {soul.prime} ({soul.prime_value})\n"
        info += "\n".join([f"{np}: {nv}" for np, nv in zip(soul.non_prime, soul.non_prime_value)])
        self.info_label = tk.Label(self.master, text=info, justify="left", relief="solid", borderwidth=1)
        self.info_label.place(x=event.widget.winfo_rootx() - self.master.winfo_rootx(), 
                              y=event.widget.winfo_rooty() - self.master.winfo_rooty() + event.widget.winfo_height())

    def hide_soul_info(self, event):
        if hasattr(self, 'info_label'):
            self.info_label.destroy()
    
    def show_help(self):
        help_text = (
            "Welcome to Onmyoji Soul Master application.\n\n"
            "1. Click 'Initialize Souls' to create new souls.\n"
            "2. Click 'Warehouse' to display the initialized souls.\n"
            "3. Hover over a soul to see its details.\n"
            "4. Click 'Hide Souls' to hide the displayed souls."
        )
        tk.messagebox.showinfo("Help", help_text)

    def on_soul_click(self, event, soul):
        action_frame = tk.Toplevel(self.master)
        action_frame.title("Choose Action")
        # action_frame.geometry("300x100")
        action_frame.transient(self.master)
        action_frame.geometry(f"+{self.master.winfo_rootx() + 50}+{self.master.winfo_rooty() + 50}")
        action_frame.grab_set()
        
        delete_button = ttk.Button(action_frame, text="Delete", command=lambda: self.delete_soul(action_frame, soul))
        delete_button.pack(side=tk.LEFT, padx=20, pady=20)
        
        boost_button = ttk.Button(action_frame, text="Boost", command=lambda: self.boost_soul(action_frame, soul))
        boost_button.pack(side=tk.RIGHT, padx=20, pady=20)

    
    def delete_soul(self, action_frame, soul):
        self.hide_souls()
        action_frame.destroy()
        self.souls.remove(soul)
        self.display_souls()
        

    def boost_soul(self, action_frame, soul):
        exp = tk.simpledialog.askinteger("Input", "Enter the amount of EXP:", parent=self.master)
        if exp is None or exp < 0:
            tk.messagebox.showwarning("Warning", "Invalid input!")
            return
        boost(soul, exp)
        self.display_souls()
        action_frame.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SoulMaster(root)
    root.mainloop()