# == imports
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import *
# from tkinter.ttk import *   # Style (unsure if going to use)
from tkinter import messagebox as mb

# == Project Packages
from Py_PDF.PDF import pdf


# GUI Class
class PDFGUI:
    selected_PDF = ''

    def __init__(self, master):     # master is the parent widget
        self.master = master        # form
        master.title('IceQuinn\'s PDFReader')   # Window's Title
        scrollBar = Scrollbar(self.master)      # Unsure of what to put in

        # ============= Parent Tab =================
        self.tab_parent = ttk.Notebook(self.master)
        # =========== Tabs (Tab control) ===========
        self.editorTab = ttk.Frame(self.tab_parent)
        self.mergeTab = ttk.Frame(self.tab_parent)
        self.splitTab = ttk.Frame(self.tab_parent)
        self.encryptTab = ttk.Frame(self.tab_parent)
        self.decryptTab = ttk.Frame(self.tab_parent)
        self.conversionTab = ttk.Frame(self.tab_parent)

        # =================================
        #  Editor Tab
        # =================================
        # Need more time for this feature
        self.editor_note = ttk.Label(self.editorTab, text="Work In Progress")
        selection_btn = ttk.Button(self.editorTab, text="SELECT PDF")
        selection_btn.place(x=500, y=40)

        # =================================
        #  Merge Tab
        # =================================
        ttk.Entry(self.mergeTab).place(x=10, y=10)
        ttk.Button(self.mergeTab, text="Select PDF",
                   command=lambda: self.browse_multi_pdf()).place(x=50, y=50)           # Select pdf

        ttk.Button(self.mergeTab, text="MERGE TAB").place(x=100, y=100)     # Merge pdf

        # =================================
        # Split Tab
        # =================================
        self.split_infile = StringVar()  # The selected pdf for splitting

        # === Widget for Split Tab
        self.split_canvas = Canvas(self.splitTab, height=300, width=300, highlightthickness=0)  # Canvas without border
        
        # Select PDF
        self.split_select_btn = ttk.Button(self.split_canvas, text="Select PDF",
                                           command=lambda: self.browseOnePDF(self.split_infile))  # Click to select PDF
        self.split_file_label = ttk.Label(self.split_canvas,
                                          textvariable=self.split_infile)    # Show Selected File Name

        # Split Button
        self.split_btn = ttk.Button(self.split_canvas, text="Split PDF",
                                    command=lambda: self.split_pdf(self.split_infile))  # Pass in PDF name

        # === ADD Widget for Split Tab (Row By Row)
        self.split_select_btn.grid(column=0, row=0)
        self.split_file_label.grid(column=0, row=1)
        self.split_canvas.place(relx=0.5, rely=0.3, anchor=CENTER)  # Place the canvas in the center

        # =================================
        # Encryption Tab (Need to Beautify it)
        # =================================
        self.lock_infile = StringVar()      # Chosen Unlock PDF
        self.lock_outfile = StringVar()     # Output locked PDF
        self.lock_password = StringVar()    # Password to lock PDF

        # === Widget for Encryption Tab
        self.encrypt_canvas = Canvas(self.encryptTab, height=300, width=300,
                                     highlightthickness=0)  # Center without border

        # Select PDF
        self.e_select_btn = ttk.Button(self.encrypt_canvas, text="Select PDF",
                                       command=lambda: self.browse_pdf(self.lock_infile))   # Click to select PDF
        self.e_file_label = ttk.Label(self.encrypt_canvas, textvariable=self.lock_infile)   # Show Selected File Name

        # Encryption File Name
        self.lock_pdf_label = ttk.Label(self.encrypt_canvas, text='Encrypted File Name: ')      # Encryption File Label
        self.lock_pdf_field = ttk.Entry(self.encrypt_canvas, textvariable=self.lock_outfile)    # Entry Widget Name

        # Password
        self.e_password_label = ttk.Label(self.encrypt_canvas, text='Password')     # Password label
        self.e_password_field = ttk.Entry(self.encrypt_canvas, show="*",
                                          textvariable=self.lock_password)  # Password Widget Name

        # Encryption Button
        self.encrypt_btn = ttk.Button(self.encrypt_canvas, text="Encrypt PDF",
                                      command=lambda: self.lock_file())  # Validate and Encrypt

        # === ADD Widget for Encryption Tab (Row By Row)
        self.e_select_btn.grid(column=0, row=1, padx=20, pady=20, columnspan=2)
        self.e_file_label.grid(column=0, row=2, padx=20, pady=20, columnspan=2)
        self.lock_pdf_label.grid(column=0, row=4, padx=20, pady=20)
        self.lock_pdf_field.grid(column=1, row=4, padx=20, pady=20)
        self.e_password_label.grid(column=0, row=5, padx=20, pady=20)
        self.e_password_field.grid(column=1, row=5, padx=20, pady=20)

        self.encrypt_btn.grid(column=0, row=6, padx=20, pady=20, columnspan=2)

        self.encrypt_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)  # Place the canvas in the center

        # =================================
        # Decryption Tab
        # =================================
        self.unlock_infile = StringVar()    # Chosen locked PDF
        self.unlock_outfile = StringVar()   # Unlocked Output PDF
        self.unlock_password = StringVar()  # Password to unlock PDF

        # Select PDF

        # Output File Name

        # Password

        # Decryption Button

        # =================================
        # Conversion Tab (File Format Convert)
        # =================================

        # == Parent tab configure (Adding tabs)
        self.tab_parent.add(self.editorTab, text="Edit PDF")
        self.tab_parent.add(self.mergeTab, text="Merge PDF")
        self.tab_parent.add(self.splitTab, text="Split PDF")
        self.tab_parent.add(self.encryptTab, text="Encrypt PDF")
        self.tab_parent.add(self.decryptTab, text="Decrypt PDF")
        self.tab_parent.add(self.conversionTab, text="Conversion")
        self.tab_parent.pack(side=TOP, fill=BOTH, expand=Y)  # Add the Parent Tab

    # =================================
    # Methods
    # =================================

    # Encrypt file
    def lock_file(self):
        if not self.lock_infile.get() == '' or self.lock_infile.get() is None:              # PDF selected
            if not self.lock_outfile.get() == '' or self.lock_outfile.get() is None:        # Output file name given
                if not self.lock_password.get() == '' or self.lock_password.get() is None:  # Password not null
                    print('pdf Name: %s\n lock pdf Name: %s\nPassword: %s' %
                          (self.lock_infile.get(), self.lock_outfile.get(), self.lock_password.get()))
                    pdf.pdf_encrypt(self.lock_infile.get(), self.lock_outfile.get(), self.lock_password.get())
                else:
                    print('Password not set')
            else:
                print('Output file not set')
        else:
            print('PDF file not selected')

    # Decrypt file
    # def unlockFile(self):

    # File browser for One PDF
    @staticmethod    # For multiple use case (non "self" methods)
    def browse_pdf(filename):
        file = tk.filedialog.askopenfilename(title="Select PDF", filetypes=[('PDF', '*.pdf')])
        filename.set(file.split('/')[-1])  # Set File name not full path

    # File Browser for Multiple PDF
    @staticmethod    # For multiple use case (non "self" methods)
    def browse_multi_pdf(multi_pdf):
        file_list = tk.filedialog.askopenfilenames(title="Select Multiple PDF", filetypes=[('PDF', '*.pdf')])
        multi_pdf.set(file_list.split('/')[-1])

    # Closing Prompt for Window
    def on_closing(self):
        if self:
            if mb.askokcancel("QUIT", "Do you want to quit?"):
                self.master.destroy()


# Calling GUI Program
def gui_main():
    main = tk.Tk()              # Main window object
    main.configure(bg='black')  # parent widget bg color

    # == Window Size Configuration
    width_val = main.winfo_screenwidth()
    height_val = main.winfo_screenheight()
    main.geometry("%dx%d+0+0" % (width_val, height_val))

    gui = PDFGUI(main)  # Initialising GUI class
    main.protocol("WM_DELETE_WINDOW", gui.on_closing)  # Delete on closing method
    main.mainloop()     # Call to Execute GUI
