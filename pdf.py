import PyPDF2
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

"""
This script converts a PDF file to a text file using Tesseract OCR. 
Good for difficult PDFs that cannot be converted using Google Docs or other online tools.

Make sure to update the `tesseract_cmd`, `poppler_path`, `pdf_path`, and `output_path` variables to match your system's installation paths and the desired input/output file paths.


To find the Tesseract installation path on your system, follow these steps depending on your operating system:

**For Windows:**

1. Press `Win + X` and click on 'Windows PowerShell' or 'Command Prompt'.
2. Type `where tesseract` and press Enter.

If Tesseract is installed and added to the system's PATH, you should see the path to the Tesseract executable. If not, check the default installation location, which is usually `C:\Program Files\Tesseract-OCR\tesseract.exe`.

It seems that Tesseract is not added to your system's PATH or not installed. Please follow these steps to install Tesseract on Windows:

1. Download the Tesseract installer for Windows from the following link: https://github.com/UB-Mannheim/tesseract/wiki

2. Run the downloaded installer and follow the installation steps. Remember the installation location (by default, it should be `C:\Program Files\Tesseract-OCR`).

3. After the installation is complete, you can either add Tesseract to your system's PATH or use the full path to the Tesseract executable in your script.

**To add Tesseract to the system's PATH:**

1. Press `Win + X` and click on 'System'.
2. Click on 'Advanced system settings' on the right side.
3. Click on the 'Environment Variables' button in the 'System Properties' window.
4. Under 'System variables', find and select the 'Path' variable, then click 'Edit'.
5. Click 'New' and add the path to the Tesseract-OCR installation folder (usually `C:\Program Files\Tesseract-OCR`).
6. Click 'OK' to save the changes.

Now, you should be able to find the Tesseract path using the `where tesseract` command in the Command Prompt or PowerShell.

**Alternatively, you can use the full path to the Tesseract executable in your script:**

Update the `tesseract_cmd` line in the Python script to the full path of the Tesseract executable:

```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

Make sure to replace the path with the correct installation location if you installed Tesseract in a different folder.


1. Download the latest version of `poppler-utils` for Windows from this link: http://blog.alivate.com.au/poppler-windows/
2. Extract the downloaded archive to a folder of your choice, for example, `C:\poppler-utils`.
3. Add the `bin` folder inside the extracted `poppler-utils` folder to your system's PATH (similar to how you added Tesseract to the PATH). For example, if you extracted `poppler-utils` to `C:\poppler-utils`, add `C:\poppler-utils\poppler-0.68.0_x86\poppler-0.68.0\bin` (adjust the version number as needed) to your system's PATH.

After adding `poppler-utils` to the system's PATH, close and reopen your Command Prompt, PowerShell, or Visual Studio Code, and try running the Python script again. The error should be resolved, and the script should be able to convert the image-based PDF to text using OCR.

"""

def convert_pdf_to_text(pdf_path, output_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        num_pages = pdf_reader.numPages
        text = ""

        for page in range(num_pages):
            text += pdf_reader.getPage(page).extractText()

    with open(output_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)

def check_pdf_restrictions(pdf_path):
    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        
        if pdf_reader.isEncrypted:
            print(f"The PDF '{pdf_path}' is encrypted.")
        else:
            print(f"The PDF '{pdf_path}' is not encrypted.")
        
        info = pdf_reader.getDocumentInfo()
        if '/EncryptMetadata' in info:
            print("Encryption Metadata: ", info['/EncryptMetadata'])
        
        if pdf_reader.getNumPages() > 0:
            page = pdf_reader.getPage(0)
            if '/Resources' in page:
                resources = page['/Resources']
                if '/Font' in resources:
                    print("Fonts used in the PDF: ", resources['/Font'])
                if '/XObject' in resources:
                    print("External objects used in the PDF: ", resources['/XObject'])

def convert_pdf_to_text_ocr(pdf_path, output_path):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    images = convert_from_path(pdf_path, poppler_path=r'C:\poppler-utils\poppler-0.68.0\bin')
    text = ""

    for image in images:
        text += pytesseract.image_to_string(image)

    with open(output_path, 'w', encoding='utf-8') as text_file:
        text_file.write(text)


if __name__ == "__main__":
    pdf_path = "lease.pdf"  # Replace with your PDF file path
    output_path = "lease.txt"  # Replace with your desired output text file path

    convert_pdf_to_text_ocr(pdf_path, output_path)
    print(f"PDF '{pdf_path}' has been converted to text using OCR and saved as '{output_path}'.")


