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

    def __init__(self, master):  # master is the parent widget
        self.master = master  # form
        master.title('IceQuinn\'s PDFReader')  # Window's Title
        scrollBar = Scrollbar(self.master)  # Unsure of what to put in
        # ==== Style
        style = ttk.Style()
        style.layout("Tab",
                     [('Notebook.tab', {'sticky': 'nswe', 'children':
                         [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                         # Remove focus on tabs
                         #  [('Notebook.focus', {'side': 'top', 'sticky': 'nswe', 'children':
                             [('Notebook.label', {'side': 'top', 'sticky': ''})],
                                                })],
                                        # })],
                                        })]
                     )

        # Some variable
        self.current_dir = StringVar()
        # self.current_dir.set('C:\\Users')  # Have a default current directory (prevent null)

        # ============= Parent Tab =================
        self.tab_parent = ttk.Notebook(self.master, takefocus=False)
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
        selected_file = StringVar()  # Show selected file name
        # === Widget for Editor Tab
        self.edit_canvas = Canvas(self.editorTab, height=500, width=500, highlightthickness=0,
                                  takefocus=False)  # Canvas without border

        editor_note = ttk.Label(self.edit_canvas, text="Work In Progress")
        selection_btn = ttk.Button(self.edit_canvas, text="SELECT PDF", command=lambda: self.browse_pdf(selected_file),
                                   takefocus=False)
        file_name = ttk.Label(self.edit_canvas, textvariable=selected_file)

        # === ADD Widget for Split Tab (Row By Row)
        editor_note.grid(column=0, row=0, padx=20, pady=20)
        selection_btn.grid(column=0, row=1)
        file_name.grid(column=0, row=2)
        self.edit_canvas.place(relx=0.5, rely=0.3, anchor=CENTER)  # Place the canvas in the center

        # =================================
        #  Merge Tab (Need change to grid)
        # =================================
        file_list = StringVar()  # Store multiple pdfs? (How to store the list of pdfs)

        # == Widget for Merge Tab
        self.merge_canvas = Canvas(self.mergeTab, height=300, width=300, highlightthickness=0,
                                   takefocus=False)  # Canvas without border
        self.merge_select = ttk.Button(self.merge_canvas, text="Select PDF",
                                       command=lambda: self.browse_multi_pdf(file_list), takefocus=False)  # Select pdf

        # == Add widget to Merge Tab
        self.merge_select.grid(column=0, row=0)
        self.merge_canvas.place(relx=0.5, rely=0.2, anchor=CENTER)  # Place the canvas in the center

        # =================================
        # Split Tab
        # =================================
        self.split_infile = StringVar()  # The selected pdf for splitting

        # === Widget for Split Tab
        self.split_canvas = Canvas(self.splitTab, height=300, width=300, highlightthickness=0,
                                   takefocus=False)  # Canvas without border

        # Select PDF
        self.split_select_btn = ttk.Button(self.split_canvas, text="Select PDF",
                                           command=lambda: self.browse_pdf(self.split_infile),
                                           takefocus=False)  # Click to select PDF
        self.split_file_label = ttk.Label(self.split_canvas,
                                          textvariable=self.split_infile)  # Show Selected File Name

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
        self.lock_infile = StringVar()  # Chosen Unlock PDF
        self.lock_outfile = StringVar()  # Output locked PDF
        self.lock_password = StringVar()  # Password to lock PDF
        self.lock_error = StringVar()  # Encrypt error message

        # === Widget for Encryption Tab
        self.encrypt_canvas = Canvas(self.encryptTab, height=300, width=300,
                                     highlightthickness=0, takefocus=False)  # Center without border
        # Instruction Label
        encryption_instruction = ttk.Label(self.encrypt_canvas,
                                           text="1. Choose the PDF to Protect\n\n" +
                                                "2. Provide Password to lock the file")

        # Select PDF
        self.e_select_btn = ttk.Button(self.encrypt_canvas, text="Select PDF",
                                       command=lambda: self.browse_pdf(self.lock_infile),
                                       takefocus=False)  # Click to select PDF
        self.e_file_label = ttk.Label(self.encrypt_canvas, textvariable=self.lock_infile)  # Show Selected File Name

        # Encryption File Name
        self.lock_pdf_label = ttk.Label(self.encrypt_canvas, text='Encrypted File Name: ')  # Encryption File Label
        self.lock_pdf_field = ttk.Entry(self.encrypt_canvas, textvariable=self.lock_outfile,
                                        takefocus=False)  # Entry Widget Name

        # Password
        self.e_password_label = ttk.Label(self.encrypt_canvas, text='Password')  # Password label
        self.e_password_field = ttk.Entry(self.encrypt_canvas, show="*",
                                          textvariable=self.lock_password, takefocus=False)  # Password Widget Name

        # Encryption Button
        self.encrypt_btn = ttk.Button(self.encrypt_canvas, text="Lock PDF",
                                      command=lambda: self.lock_file(), takefocus=False)  # Validate and Encrypt

        # Error Message
        self.encrypt_error = ttk.Label(self.encrypt_canvas, textvariable=self.lock_error)

        # === ADD Widget for Encryption Tab (Row By Row)
        encryption_instruction.grid(column=0, row=1, padx=20, pady=20, columnspan=2)
        self.e_select_btn.grid(column=0, row=2, padx=20, pady=20, columnspan=2, ipadx=30, ipady=15)
        self.e_file_label.grid(column=0, row=3, padx=20, pady=20, columnspan=2)
        self.lock_pdf_label.grid(column=0, row=4, padx=20, pady=20)
        self.lock_pdf_field.grid(column=1, row=4, padx=20, pady=20)
        self.e_password_label.grid(column=0, row=5, padx=20, pady=20)
        self.e_password_field.grid(column=1, row=5, padx=20, pady=20)

        self.encrypt_btn.grid(column=0, row=6, padx=20, pady=20, columnspan=2)
        self.encrypt_error.grid(column=0, row=7, padx=10, pady=10, columnspan=2)

        self.encrypt_canvas.place(relx=0.5, rely=0.5, anchor=CENTER)  # Place the canvas in the center

        # =================================
        # Decryption Tab
        # =================================
        self.unlock_infile = StringVar()  # Chosen locked PDF
        self.unlock_outfile = StringVar()  # Unlocked Output PDF
        self.unlock_password = StringVar()  # Password to unlock PDF
        self.unlock_error = StringVar()  # Display error message
        # === Widget for Decryption Tab
        self.decrypt_canvas = Canvas(self.decryptTab, height=300, width=300, highlightthickness=0,
                                     takefocus=False)  # Center without border
        # Select PDF
        self.d_select_btn = ttk.Button(self.decrypt_canvas, text="Select PDF",
                                       command=lambda: self.browse_pdf(self.unlock_infile),
                                       takefocus=False)  # Click to select PDF
        self.d_file_label = ttk.Label(self.decrypt_canvas, textvariable=self.unlock_infile)  # Show Selected pdf
        # Output File Name
        self.outfile_label = ttk.Label(self.decrypt_canvas, text='Unlocked File Name: ')  # Encryption File Label
        self.outfile_field = ttk.Entry(self.decrypt_canvas,
                                       textvariable=self.unlock_outfile, takefocus=False)  # Entry Widget Name

        # Password
        self.d_password_label = ttk.Label(self.decrypt_canvas, text='Password')  # Password label
        self.d_password_field = ttk.Entry(self.decrypt_canvas, show="*",
                                          textvariable=self.unlock_password, takefocus=False)  # Password Widget Name
        # Decryption Button
        self.decrypt_btn = ttk.Button(self.decrypt_canvas, text="Unlock PDF",
                                      command=lambda: self.unlock_file(), takefocus=False)  # Validate and Encrypt
        # Error Message Label
        self.decrypt_error = ttk.Label(self.decrypt_canvas, textvariable=self.unlock_error)  # Show error message

        # === ADD Widget for Decryption Tab (Row By Row)
        self.d_select_btn.grid(column=0, row=1, padx=20, pady=20, columnspan=2, ipadx=30, ipady=15)
        self.d_file_label.grid(column=0, row=2, padx=20, pady=20, columnspan=2)
        self.outfile_label.grid(column=0, row=4, padx=20, pady=20)
        self.outfile_field.grid(column=1, row=4, padx=20, pady=20)
        self.d_password_label.grid(column=0, row=5, padx=20, pady=20)
        self.d_password_field.grid(column=1, row=5, padx=20, pady=20)

        self.decrypt_btn.grid(column=0, row=6, padx=20, pady=20, columnspan=2)
        self.decrypt_error.grid(column=0, row=7, padx=10, pady=10, columnspan=2)
        self.decrypt_canvas.place(relx=0.5, rely=0.3, anchor=CENTER)  # Place the canvas in the center

        # =================================
        # Conversion Tab (File Format Convert)
        # =================================
        self.file_format = StringVar()  # Selected File Format
        self.convert_infile = StringVar()  # Selected PDF

        self.conversion_canvas = Canvas(self.conversionTab, width=200, height=500, highlightthickness=0,
                                        takefocus=False)
        # == Widgets for Conversion Tab
        self.conversion_instruction = ttk.Label(self.conversion_canvas,
                                                text="1. Select the format you want your PDF to convert to.")
        self.format_label = ttk.Label(self.conversion_canvas, text="File Format")  # Instructions
        self.format_field = ttk.Combobox(self.conversion_canvas, state="readonly", textvariable=self.file_format,
                                         width=50, takefocus=False)  # File Format Selection
        self.format_field.bind("<FocusIn>", self.combobox_deselect)  # Remove the highlight
        default = "Select File Format"  # Placeholder
        default = default.rjust(len(default) + 30, ' ')  # Padding for the text
        # ComboBox Options
        self.format_field['values'] = [
            default,
            "Word (*.docx)",
            "Portable Network Graphics (*.png)",
            "Joint Photographic Expert Group (*.jpeg)"]
        self.format_field.current(0)
        self.conversion_select_btn = ttk.Button(self.conversion_canvas, text="Select PDF",
                                                command=lambda: self.browse_pdf(self.convert_infile),
                                                takefocus=False)  # PDF Selection
        self.conversion_infile_label = ttk.Label(self.conversion_canvas, textvariable=self.convert_infile)

        # == Add the widgets to Conversion Tab
        self.conversion_instruction.grid(column=0, row=0, columnspan=3, padx=10, pady=10)
        self.format_label.grid(column=0, row=1, padx=10, pady=10)
        self.format_field.grid(column=1, row=1, padx=10, pady=10, columnspan=2)
        self.conversion_select_btn.grid(column=0, row=2, padx=10, pady=10, columnspan=3)
        self.conversion_infile_label.grid(column=0, row=3, padx=10, pady=10, columnspan=3)

        self.conversion_canvas.place(relx=0.5, rely=0.15, anchor=CENTER)  # Place the canvas in the center

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

    # Clear Combobox Selection Highlight
    @staticmethod
    def combobox_deselect(event):
        event.widget.master.focus_set()

    # Encrypt file
    def lock_file(self):
        if not self.lock_infile.get() == '' or self.lock_infile.get() is None:  # PDF selected
            if not self.lock_outfile.get() == '' or self.lock_outfile.get() is None:  # Output file name given
                if not self.lock_password.get() == '' or self.lock_password.get() is None:  # Password not null
                    print('pdf Name: %s\nLock pdf Name: %s\nPassword: %s' %
                          (self.current_dir.get() + self.lock_infile.get(),
                           self.lock_outfile.get(), self.lock_password.get()))
                    pdf.pdf_encrypt(self.current_dir.get() + self.lock_infile.get(),
                                    self.lock_outfile.get(), self.lock_password.get())
                    # Message Box
                    mb.showinfo('Success', '%s been successfully generated in \'Download\' folder'
                                % self.lock_outfile.get())
                    # Delete first to the last
                    self.lock_pdf_field.delete(0, 'end')    # Encrypt entry
                    self.e_password_field.delete(0, 'end')  # Password entry

                else:
                    self.lock_error.set('Password not set')
            else:
                self.lock_error.set('Output file not set')
        else:
            self.lock_error.set('PDF file not selected')

    # Decrypt file
    def unlock_file(self):
        if not self.unlock_infile.get() == '' or self.unlock_infile.get() is None:  # PDF selected
            if not self.unlock_outfile.get() == '' or self.unlock_outfile.get() is None:  # Output file name given
                if not self.unlock_password.get() == '' or self.unlock_password.get() is None:  # Password not null
                    print('pdf Name: %s\n Unlocked pdf Name: %s\nPassword: %s' %
                          (self.unlock_infile.get(), self.unlock_outfile.get(), self.unlock_password.get()))
                    pdf.pdf_decrypt(self.unlock_infile.get(), self.unlock_outfile.get(), self.unlock_password.get())
                else:
                    self.unlock_error.set('Password not set')
            else:
                self.unlock_error.set('Output file not set')
        else:
            self.unlock_error.set('PDF file not selected')

    # Split file
    def split_pdf(self, filename):
        pass

    # Merge file    (Select Multiple Files)
    def merge_pdf(self):
        pass

    # Convert file  (File Name and File Format) Default Name is the original name
    def convert_pdf(self):
        pass

    # ==== ERROR MESSAGES  ====

    # File browser for One PDF
    # @staticmethod  # For multiple use case (non "self" methods)
    def browse_pdf(self, filename):
        file = tk.filedialog.askopenfilename(title="Select PDF", filetypes=[('PDF', '*.pdf')])
        filename.set(file.split('/')[-1])  # Set File name not full path
        self.current_dir.set(file[:len(file) - len(filename.get())] + '/')  # Setting the current directory
        print(self.current_dir.get())  # Debugging

    # File Browser for Multiple PDF
    @staticmethod  # For multiple use case (non "self" methods)
    def browse_multi_pdf(multi_pdf):
        file_list = tk.filedialog.askopenfilenames(title="Select Multiple PDF", filetypes=[('PDF', '*.pdf')])
        print('This is filelist:', file_list)
        multi_pdf.set(file_list.split('/')[-1])

    # Closing Prompt for Window
    def on_closing(self):
        if self:
            if mb.askokcancel("QUIT", "Do you want to quit?"):
                self.master.destroy()


# Calling GUI Program
def gui_main():
    main = tk.Tk()  # Main window object
    main.configure(bg='black')  # parent widget bg color

    # == Window Size Configuration
    width_val = main.winfo_screenwidth()
    height_val = main.winfo_screenheight()
    main.geometry("%dx%d+0+0" % (width_val, height_val))

    gui = PDFGUI(main)  # Initialising GUI class
    main.protocol("WM_DELETE_WINDOW", gui.on_closing)  # Delete on closing method
    main.mainloop()  # Call to Execute GUI

# Task
# To Complete Conversion / Split
