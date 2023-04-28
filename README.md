
# Vevox Poll Creator & PDF Generator


Welcome to the Vevox PDF Generator and Poll Creator.

The application allows users to create polls that can be imported and used on the [Vevox](https://vevox.com/) polling platform. It also allows the conversion of zip files from the [Vevox](https://vevox.com/) platform and produces a PDF with the contents of the poll data from the zip file.

This application is built using Python and PyQT.




## Environment Variables

To run this project, you will need to add the following environment variables:

`pdfkit`

`wkhtmltopdf`

Tutorial: https://ourcodeworld.com/articles/read/240/how-to-edit-and-add-environment-variables-in-windows-for-easy-command-line-access

Once wkhtmltopdf is installed, change line 23 in the VevoxPDFGenerator class to to the of the wkhtmltopdf.exe file. For Windows, the current path should be the defualt path, however it may be different for Linux. 

Installation of wkhtmltopdf (Linux version) : https://accel-archives.intra-mart.jp/2014-summer/document/forma/public_en/forma_setup_guide/texts/install/linux/pdf.html
## Libraries Used


[PyQT5](https://pypi.org/project/PyQt5/)

[cv2](https://pypi.org/project/opencv-python/)

pip is the package installer for Python. You can use pip to install packages from the Python Package Index and other indexes.

[pip](https://pypi.org/project/pip/)

