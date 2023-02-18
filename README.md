# LaTeX files for Master's Thesis in Mathematics

This repository contains LaTeX files for a Master's Thesis in Mathematics. Each chapter is kept in a separate directory, and diagrams and figures are stored in subdirectories as PDFs and are automatically inserted into the text.

The repository also includes Python code for automatically rendering LaTeX diagrams from the command line. This can be useful for updating or modifying the figures and diagrams during the writing process.

## Structure
The repository is structured as follows:


Each chapter is stored in a separate directory, which contains the LaTeX source file for that chapter. Figures and diagrams are stored in subdirectories of the chapter directories and are included in the text using the `\includegraphics` command. The `diagrams` directory contains Python code for generating diagrams and figures. These scripts can be run from the command line to update the PDF files in the chapter directories.

## Dependencies
In order to build the PDF file for the thesis, you will need a LaTeX distribution installed on your system, such as TeX Live or MiKTeX.

To run the Python scripts in the `diagrams` directory, you will need to have Python 3.x installed on your system, as well as the `matplotlib` and `numpy` libraries.

## Building
To build the PDF file for the thesis, navigate to the root directory of the repository and run the following command:


This will generate a PDF file named `thesis.pdf`.

To run a Python script in the `diagrams` directory, navigate to that directory and run the script using the following command:


This will generate a PDF file named `figure1.pdf` in the appropriate chapter directory.

## License
This repository is released under the MIT License. Feel free to use this code as a template for your own Master's Thesis or other LaTeX projects.
