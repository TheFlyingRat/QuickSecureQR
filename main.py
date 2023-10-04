from tkinter import ttk, BooleanVar, Tk, END
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
from PIL.ImageTk import PhotoImage
from PIL.Image import NEAREST, frombytes 

class QuickQRApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title("QuickSecureQR")
        self.root.geometry("388x432")  # Fixed window size to fit gui and no more
        self.root.resizable(False, False)  # Disable window resizing

        # Configure columns to expand horizontally
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        self.hide_qr_var = BooleanVar(value=True)  # Checkbox is checked by default
        self.hide_text_var = BooleanVar(value=False) 

        self.hide_qr_checkbox = ttk.Checkbutton(
            root,
            text="Hide",
            variable=self.hide_qr_var,
            command=self.toggle_qr_preview,
        )
        self.hide_qr_checkbox.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.hide_qr_checkbox.bind("<Return>", self.toggle_qr_preview)  # Bind the enter key to toggle the hide checkbox

        self.text_entry = ttk.Entry(root, width=32) 
        self.text_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")  

        self.clear_button = ttk.Button(root, text="Clear", command=self.clear_text) # clear button clears text in text field
        self.clear_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew") 

        self.qr_label = ttk.Label(root)
        self.qr_label.grid(row=1, column=0, columnspan=3, sticky="ew") 
        self.qr_label.columnconfigure(0, weight=1)  

        self.text_entry.bind("<Escape>", self.clear_text)  # Bind the escape key to clear
        self.text_entry.bind("<KeyRelease>", self.update_qr)  # Bind the key release event to generate, and update qr
        self.text_entry.bind("<Return>", self.toggle_qr_preview)  # Bind the enter key to toggle the hide box

        # Initially hide the QR preview if the checkbox is checked
        self.toggle_qr_preview()

        # Auto highlight the text field when the program starts
        self.text_entry.focus_set()
        self.text_entry.select_range(0, END)
        
        self.countdown_running = False

    def clear_text(self, *a, **kw):
        self.text_entry.delete(0, END)
        self.qr_label.img = None
        
    
    # TODO: merge this with the toggle_qr_preview func
    def hide_after_five(self):
        if self.countdown_running is False:
            self.hide_qr_var.set(True)
            self.qr_label.grid_remove()  # Hide the qr, in fact, delete it from the gui haha
            self.text_entry.config(show="\u2022") # replace password with the dots for over-the-shoulder obfuscation

    def update_checkbox_every_second(self, val):
        # recursion update checkbox to new value every second until 0
        if self.countdown_running is True:
            if val == 0:
                self.hide_qr_checkbox.config(text="Hide")
                self.countdown_running = False
                return None
            self.hide_qr_checkbox.config(text=f"[{val}]")
            self.root.after(1000, self.update_checkbox_every_second, val-1)

    # TODO: Fix the bug where multiple timers can exist if user clicks at a very specific time (within 1 second of previous number changing, e.g clicking at 4.5 seconds when user clicked off at 5 or something like that idk)

    def toggle_qr_preview(self, *a, **kw):
        if self.hide_qr_var.get():
            self.countdown_running = False
            self.hide_qr_checkbox.config(text="Hide")
            self.qr_label.grid_remove()  # hide qr
            self.text_entry.config(show="\u2022") # replace password with dots
        else:
            self.text_entry.config(show="")
            self.qr_label.grid()  # Show the qr
            self.countdown_running = True
            self.update_checkbox_every_second(5)
            self.root.after(5100, self.hide_after_five) # 100ms extra fixes some bug 
            

    def update_qr(self, *a, **kw):  
        text = self.text_entry.get()
        if text:
            qr = QRCode(
                version=1,
                error_correction=ERROR_CORRECT_L,
                box_size=6,
                border=0,
            )
            qr.add_data(text)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="transparent")

            # Upscale the QR code to 384x384 with nearest neighbor interpolation - its kinda broken but its whatever
            qr_img = qr_img.resize((384, 384), NEAREST)

            # convert PIL image to Tkinter PhotoImage with transparency so its compatible with gui
            qr_img = qr_img.convert("RGBA")
            img_data = qr_img.tobytes("raw", "RGBA")
            img_tk = PhotoImage(frombytes("RGBA", qr_img.size, img_data))

            self.qr_label.configure(image=img_tk)
            self.qr_label.img = img_tk
        else:
            self.qr_label.configure(image=None)

def main():
    # run app
    root = Tk()
    QuickQRApp(root)
    root.mainloop()

if __name__ == "__main__":
    # call main if ran as script/app, rather than import
    main()
