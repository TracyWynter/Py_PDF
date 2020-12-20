# == imports
# Note: PyPDF2 does not work well with Python 3
import PyPDF4   # For python 3.* and above
import os

# =================================
# PDF Methods
# =================================


# Merge PDFs
def pdf_merge(ori_pdf: list, output_pdf):
    pdfMerger = PyPDF4.PdfFileMerger()  # Create pdf merger object
    # Append PDFs one by one
    for pdf in ori_pdf:
        with open(pdf, 'rb') as in_file:
            pdfMerger.append(in_file)

    # Writing merge pdf to output file
    pdfMerger.write(output_pdf)
    pdfMerger.close()


# Split PDF (Take in end page of each split file)
def pdf_split(ori_pdf, split_pages: list):
    # Create original pdf obj
    pdfFileObj = open(ori_pdf, 'rb')    # Read binary

    # Start to End (Indexes)
    start = 0
    end = split_pages[0]  # Page i+1

    # Looping through the splitting points
    for i in range(len(split_pages)):
        # Create Reader Object
        pdfReader = PyPDF4.PdfFileReader(pdfFileObj)

        # Create writer object
        pdfWriter = PyPDF4.PdfFileWriter()

        # Output file
        outputPDF = ori_pdf.split('.pdf')[0] + str(i+1) + '.pdf'

        # Adding pages to writer (count starts from 0)
        for page in range(start, end):
            pdfWriter.addPage(pdfReader.getPage(page))  # Add pdf object

        # Writing split pdf to file
        with open(outputPDF, 'wb') as file:
            pdfWriter.write(file)

        # Does not execute when its the last split
        if not end == split_pages[len(split_pages)-1]:
            try:
                # Next split point (change start and end points)
                start = end
                # Setting the end position for the next split
                end = split_pages[i+1]
            except IndexError:  # Test if there is out of bound
                print('Page Out Of Bound')

    # Close file obj
    pdfFileObj.close()


# Encrypt PDF
def pdf_encrypt(ori_pdf, lock_pdf, pw):
    pdfWriter = PyPDF4.PdfFileWriter()          # Writer object
    pdfReader = PyPDF4.PdfFileReader(ori_pdf)   # Reader Object
    home = os.path.expanduser('~')
    path_dir = os.path.join(home, 'Downloads\\')    # Output file directory

    # Only encrypt if the file is not encrypted
    if not pdfReader.isEncrypted:   # Check if it is encrypted
        for page in range(pdfReader.getNumPages()):
            pdfWriter.addPage(pdfReader.getPage(page))

        pdfWriter.encrypt(user_pwd=pw, use_128bit=True)     # Encrypt using 128 bits
        # Output to writer object
        with open(path_dir + lock_pdf + '.pdf', 'wb') as file:         # Write binary
            pdfWriter.write(file)
        print("'%s' is generated" % lock_pdf)
    else:
        print("'%s' is already encrypted" % ori_pdf)


# Decrypt PDF
def pdf_decrypt(ori_pdf, unlock_pdf, pw):
    pdf_file = PyPDF4.PdfFileReader(ori_pdf)    # Open PDF with Reader object
    pdfWriter = PyPDF4.PdfFileWriter()
    home = os.path.expanduser('~')
    path_dir = os.path.join(home, 'Downloads\\')    # Output file directory
    if pdf_file.isEncrypted:    # Check if is encrypted
        pdf_file.decrypt(pw)    # Decrypt
        # Iterate through unlock file and add every page to new file
        for page in range(pdf_file.getNumPages()):
            pdfWriter.addPage(pdf_file.getPage(page))

        # Output decrypted pdf to new file
        with open(path_dir + unlock_pdf, 'wb') as file:
            pdfWriter.write(file)
        print("Decrypted PDF File '%s' is generated" % unlock_pdf)
    else:
        print("'%s' is not encrypted" % ori_pdf)


# Edit PDF

    # # Writing to new pdf
    # newFile = open(output_pdf, 'wb')    # Write binary
    # pdfWriter = PyPDF2.PdfFileWriter()  # Writer object
    # pdfWriter.write(newFile)    # Write to new pdf


# Convert PDF
# def pdf_convert:
