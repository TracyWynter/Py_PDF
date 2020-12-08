# import modules
from pathlib import Path
import PyPDF2
from Py_PDF import pdf
from Py_PDF import pdfGUI


# Main (Testing the Methods)
def main():
    # Original PDF
    pdfs = ['TestPDF.pdf', 'ProjSpec.pdf']

    # Output PDF
    output = 'Merged_File.pdf'
    inputPDF = 'ProjSpec.pdf'
    lockPDF = 'Lock_PDF.pdf'
    unlockPDF = 'Unlock_PDF.pdf'
    split_file = 'RevTest.pdf'
    pdfPW = 'keys'

    # Split pages in int list
    split_pages = [3, 6, 11, 17]    # The end page of each split file

    # Calling merge function
    # pdf.pdf_merge(pdfs, output)
    # pdf.pdf_encrypt(inputPDF, lockPDF, pdfPW)
    # pdf.pdf_decrypt(lockPDF, unlockPDF, pdfPW)
    pdf.pdf_split(split_file, split_pages)


# driver
if __name__ == "__main__":
    pdfGUI.gui_main()
