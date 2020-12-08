import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import *
# from tkinter.ttk import *   # Style
from tkinter import messagebox as mb
from Py_PDF import pdf  # import module


# GUI Class
class PDFGUI:


    selected_PDF = ''

    def __init__(self, master):  # master is the parent widget
        self.master = master    # form
        master.title('IceQuinn\'s PDFReader')   # Window's Title
        scrollBar = Scrollbar(self.master)  # Unsure of what to put in


        # ========== Parent Tab =============
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
        selection_btn = ttk.Button(self.editorTab, text="SELECT PDF")
        selection_btn.place(x=500, y=40)

        # =================================
        #  Merge Tab
        # =================================
        ttk.Entry(self.mergeTab).place(x=10, y=10)
        ttk.Button(self.mergeTab, text="Select PDF",
                   command=self.browseMultiPDF).place(x=50, y=50)   # Select pdf

        ttk.Button(self.mergeTab, text="MERGE TAB").place(x=100, y=100) # Merge pdf

        # =================================
        # Split Tab
        # =================================
        self.split_pdf = StringVar()                # The selected pdf for splitting
        self.split_pdf.set('hi')
        self.top=ttk.Frame(self.splitTab)
        self.top.pack(fill=BOTH, expand=TRUE)       # Top Frame
        self.bottom=ttk.Frame(self.splitTab)
        self.bottom.pack(side=BOTTOM, fill=BOTH, expand=TRUE)   # Bottom Frame
        ttk.Button(self.top, text="Select PDF",
                   command=self.browseOnePDF).grid(column=0, row=2, pady=50, padx=20,
                                                          ipady=15, ipadx=25)       # Select PDF
        ttk.Label(self.top, textvariable=self.split_pdf).grid(column=0,row=3)
        ttk.Label(self.bottom, text='Notice').grid(column=0, row=3)

        # =================================
        # Encryption Tab (Need to Beautify it)
        # =================================
        self.lock_infile = StringVar()          # Chosen Unlock PDF
        self.lock_outfile = StringVar()         # Output locked PDF
        self.lock_password = StringVar()        # Password to lock PDF

        # Select PDF
        ttk.Button(self.encryptTab, text="Select PDF",
                   command=self.browseOnePDF).grid(
            column=5, row=1, pady=20, padx=20, ipady=20, ipadx=40)
        ttk.Label(self.encryptTab, textvariable=self.lock_infile).grid(column=0, row=2, pady=20, padx=20)

        # Encryption File Name
        self.lock_pdf_field = ttk.Entry(self.encryptTab, textvariable=self.lock_outfile)    # Entry Widget Name
        self.lock_pdf_field.grid(column=1,row=3,pady=20,padx=20)
        ttk.Label(self.encryptTab, text='Encrypted File Name: ').grid(column=0,row=3,pady=20,padx=20)



        # Password
        self.password_field = ttk.Entry(self.encryptTab, show="**", textvariable=self.lock_password)    # Password Widget Name
        self.password_field.grid(column=0, row=4, pady=20, padx=20)     # Add Password Widget
        ttk.Label(self.encryptTab, text='Password')

        # Encryption Button
        encrypt_btn = ttk.Button(self.encryptTab, text="Encrypt PDF", command=self.lockFile)
        encrypt_btn.grid(column=0, row=5, pady=20, padx=20)

        # =================================
        # Decryption Tab
        # =================================
        self.unlock_infile = StringVar()        # Chosen locked PDF
        self.unlock_outfile = StringVar()       # Unlocked Output PDF
        self.unlock_password = StringVar()      # Password to unlock PDF

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
        self.tab_parent.pack(side=TOP, fill=BOTH, expand=Y)     # Add the Parent Tab


    # =================================
    # Methods
    # =================================

    # Encrypt file
    def lockFile(self):
        if not self.pdf_name.get() == '' or self.pdf_name.get() == None:    # PDF selected
            if not self.lock_pdf.get() == '' or self.lock_pdf.get() == None:    # Output file name given
                if not self.password.get() == ''  or self.password.get() == None:   # Password not null
                    print('pdf Name: %s\n lock pdf Name: %s\nPassword: %s' %
                          (self.pdf_name.get(), self.lock_pdf.get(), self.password.get()))
                    pdf.pdf_encrypt(self.pdf_name.get(), self.lock_pdf.get(), self.password.get())
                else:
                    print('Password not set')
            else:
                print('Output file not set')
        else:
            print('PDF file not selected')

    # Decrypt file
    # def unlockFile(self):



    # File browser (one pdf)
    def browseOnePDF(self):
        pdf_name = tk.filedialog.askopenfilename(title="Select PDF",
                                                      filetypes=[('PDF', '*.pdf')])
        self.pdf_name.set(pdf_name.split('/')[-1])  # Set File name not full path

    # Multiple PDF
    def browseMultiPDF(self):
        self.MultiPDF = tk.filedialog.askopenfilenames(title="Select Multiple PDF",
                                                       filetypes=[('PDF', '*.pdf')])
        self.MultiPDF.set(self.MultiPDF.split('/')[-1])
    
    # Closing Prompt
    def on_closing(self):
        if self:
            if mb.askokcancel("QUIT", "Do you want to quit?"):
                self.master.destroy()


# Calling GUI Program
def gui_main():
    main = tk.Tk()  # Main window object

    main.configure(bg='black')  # parent widget bg color

    # Window Size
    width_val = main.winfo_screenwidth()
    height_val = main.winfo_screenheight()
    main.geometry("%dx%d+0+0" % (width_val, height_val))


    gui = PDFGUI(main)  # Initialising GUI class
    main.protocol("WM_DELETE_WINDOW", gui.on_closing)   # Delete on closing method
    main.mainloop()  # Use to run