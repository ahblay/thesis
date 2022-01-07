\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{sigmasthesis}[2020/01/21 UVic Thesis/Dissertation Template for SIGMAS]

% 	Original class by Ross Churchley, circa 2011 or so
% 	Updated by Joseph Horan, Spring 2020

%   Options
%
%   Passes all class options to the underlying book class
%	This class is based on the "book" class, which comes with a number of pre-set commands and settings.

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{book}}
\ProcessOptions

\LoadClass{book}

%   Margins and spacing
%
%   Sets margins. UVic no longer has margin requirements (it did back when Ross wrote the template). 
%   Also defines commands to allow double- and one-and-a-half-spacing as necessary.

%	Original margins were: [top=1.3in,left=1.5in,bottom=1in,right=1in,headsep=0.5in]

\RequirePackage[top=1in,left=1.2in,bottom=1in,right=1.2in,headsep=0.2in]{geometry}

% 	This changes the line spacing. Most style guides (eg. MLA, APA, Chicago...) recommend double line spacing. On the other hand, currently (Spring 2020) UVic has no guidelines on the matter (adhere to your discipline's style guide; math and stats doesn't really have one). There is research evidence to show that some amount of line spacing is beneficial to reading, but too much is not helpful. Double line spacing facilitates in-line editing and comments.

% 	The \setstretch{factor} command allows for more fine-tuning than \singlespacing (factor = 1), \onehalfspacing (factor = 1.241 for 12pt font), or \doublespacing (factor = 1.655 for 12pt font). Only play with this if you're absolutely sure you don't want to use either \onehalfspacing or \doublespacing.

\RequirePackage{setspace}
%	\newcommand{\defaultspacing}{\onehalfspacing} % Default for the body text is double line spacing: \doublespacing.
    \newcommand{\defaultspacing}{\singlespacing\setstretch{1.12}} % Uncomment this line and comment out the above line for fine-tuned spacing as described above.
    \newcommand{\smallspacing}{\onehalfspacing} % Used for the preliminary pages.

% 	Here's where you can change the format of the Chapter headers. Note that \chaptertitlename defaults to \chaptername (which is generally ``Chapter'' unless you've changed it) except when you're in an appendix, when it changes to \appendixname (which is generally ``Appendix'').

\RequirePackage{titlesec}
    \titleformat{\chapter}[display]{\Huge\bfseries}{\chaptertitlename\ \thechapter}{0pt}{}{}

%	Page numbering is roman for the preliminary pages, arabic for the rest of the document.

\renewcommand{\frontmatter}{%
    \smallspacing
    \pagenumbering{roman}
}

\renewcommand{\mainmatter}{%
    \clearpage
    \defaultspacing
    \pagenumbering{arabic}
}

%   Headers
%
%   UVic has no guidelines on placement of page numbers or use of headers.
%	For the purposes of aligning with a oneside book format (horizontally symmetric pages with equal margins) and allowing for double-siding physical printing if need be, we'll use bottom center page numbers.
%

\usepackage{fancyhdr}
\setlength{\headheight}{15pt}

\fancypagestyle{plain}{%
        \fancyhf{}							% clears all headers/footers, just in case
        \fancyfoot[C]{\thepage}				% places the page number in center of the footer
        \renewcommand{\headrulewidth}{0pt}	% no header lines
        \renewcommand{\footrulewidth}{0pt}	% no footer lines
}
\pagestyle{plain}


%   Title page metadata
%
%   Allows the user to easily set the information displayed on the title page.
%

\renewcommand{\@date}{\the\year}

\newcommand{\type}[1]{\renewcommand\@type{#1}}
\newcommand{\@type}{%
    \ClassError{sigmasthesis}{I need to know whether this is a thesis or a dissertation. Use \protect\type{Thesis} or \protect\type{Dissertation} in the preamble.}{}}
    
\newcommand{\authordetails}[1]{\renewcommand\@authordetails{#1}}
\newcommand{\@authordetails}{}

\newcommand{\degree}[1]{\renewcommand\@degree{#1}}
\newcommand{\@degree}{%
    \ClassError{sigmasthesis}{What degree are you writing this for? Use \protect\degree in the preamble to tell me your expected degree.}{}}

\newcommand{\department}[1]{\renewcommand\@department{#1}}
\newcommand{\@department}{%
    \ClassError{sigmasthesis}{What department are you in? Let me know with  \protect\department in the preamble.}{}
}

\newcommand\panelist[3]{\noindent #1, #2\\\noindent(#3)\tpbreak}
\newcommand{\panel}[1]{\renewcommand\@panel{#1}}
\newcommand{\@panel}{}


%   Title page
%
%   Displays the title page and second page listing the supervisory committee.
%	Takes in a boolean to indicate whether or not the UVic Territory Acknowledgement is included.

\RequirePackage{textcase}
\newcommand{\tpbreak}{\\[\baselineskip]}    % an extra big line break

\newcommand{\maketitlepage}[1]{{\centering
    \@title                                                             \tpbreak
    by                                                                  \tpbreak
    \@author                                                            \\
    \@authordetails                                                     \tpbreak
    A {\@type} Submitted in Partial Fulfillment of the \\
    Requirements for the Degree of                                      \tpbreak
    \MakeUppercase{\@degree}                                            \tpbreak
    in the \@department                     \\ \vfill
    
    \begin{tabular}{cl}
        \copyright  & \@author, \@date\\
                    & University of Victoria
    \end{tabular}                                                       \tpbreak
    \ifbool{#1}
    {All rights reserved. This \MakeLowercase{\@type} may not be reproduced in whole or in part, by photocopying or other means, without the permission of the author. 					\tpbreak
    We acknowledge with respect the Lekwungen peoples on whose traditional territory the university stands, and the Songhees, Esquimalt, and \b{W}S\'{A}NE\'{C} peoples whose historical relationships with the land continue to this day. \tpbreak}
    {All rights reserved. This \MakeLowercase{\@type} may not be reproduced in whole or in part, by photocopying or other means, without the permission of the author. \tpbreak}
}}

\newcommand{\makepanelpage}{
    \addtoToC{Supervisory Committee}
    {\centering
    \@title                                                             \tpbreak
    by                                                                  \tpbreak
    \@author                                                            \\
    \@authordetails                                                     \tpbreak
    }                                                                   \vfill

    \noindent Supervisory Committee                                     \tpbreak
    \@panel                                                             \vfill
}

\renewcommand{\maketitle}[1]{
    \thispagestyle{empty}
    \maketitlepage{#1}             % prints the actual title page (defined above)
    \newpage
    \setcounter{footnote}{0}
}

\newcommand{\makecommittee}{%
    \makepanelpage
    \newpage%
}


%   Abstract
%
%   Displays the abstract page and adds it to the table of contents. "ABSTRACT" could be replaced with "Abstract" if desired.
%	Big change from the old template: Don't need to put the supervisory committee on this page again.
%	Not sure why that was ever a requirement, but it isn't anymore.

\newenvironment{abstract}{
    \newpage\addtoToC{Abstract}

    \begin{center}\textbf{ABSTRACT}\end{center}
    
    }{}


%   Table of Contents
%
%   Fixes some display issues for the table of contents.
%   Provides a command to add sections like the bibliography to the ToC.

\renewcommand{\contentsname}{Table of Contents} % 

\newcommand{\addtoToC}[1]{\addcontentsline{toc}{chapter}{#1}}

\usepackage{tocloft}
\renewcommand{\cftchappresnum}{\chaptertitlename\ } % Prints ``Chapter 1'' or ``Appendix A'' instead of ``1'' or ``A'' in ToC.
\setlength{\cftchapnumwidth}{1.15in} % you could also use the calc package and use \widthof to pick a less arbitrary number.
\renewcommand{\cfttabpresnum}{Table\ }
\renewcommand{\cfttabnumwidth}{0.75in}
\renewcommand{\cftfigpresnum}{Figure\ }
\renewcommand{\cftfignumwidth}{0.90in}

% By default, the Table of Contents does not say ``Chapter'' or ``Appendix''; it just puts the numbering `1' or `A', etc. However, since we specified the pre-section-number (\cftchappresnum) text to be \chaptertitlename, we need to correctly pass it to the .toc file produced by the document. Unfortunately, this macro is what we call ``fragile''; because the .toc file is what is being read when the ToC is being produced, to correctly typeset ``Appendix'' we need to pass that redefinition to the .toc file. We accomplish this redefinition by modifying the \appendix macro; thanks to https://tex.stackexchange.com/questions/56839/chaptername-is-used-even-for-appendix-chapters-in-toc for this. Thus, when the \appendix command is run, it puts a note in the .toc file to correctly typeset the entry.

\g@addto@macro\appendix{
  \addtocontents{toc}{
    \protect\renewcommand{\protect\cftchappresnum}{\appendixname\space}
  }
}

\setcounter{lofdepth}{2}		% displays figure numbering to the depth of section. 1 for chapters, 3 for subsections, etc.

%   Acknowledgements
%
%   Displays the acknowledgements page and adds it to the table of contents.
%	Again, could change the all caps to regular. 

\newenvironment{acknowledgements}{%
    \newpage\addtoToC{Acknowledgements}

    \begin{center}\textbf{ACKNOWLEDGEMENTS}\end{center}
    
    }{}


%   Dedication
%
%   Displays the dedication page and adds it to the table of contents.
%	Again, could change the all caps to regular.

\newenvironment{dedication}{%
    \newpage\addtoToC{Dedication}

    \begin{center}\textbf{DEDICATION}\end{center}
    
    }{}


\endinput