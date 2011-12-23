Bracketeer plugin for Sublime Text 2
=====================================

Installation
------------

1. Open the Sublime Text 2 Packages folder

    - OS X: ~/Library/Application Support/Sublime Text 2/Packages/
    - Windows: %APPDATA%/Sublime Text 2/Packages/
    - Linux: ~/.Sublime Text 2/Packages/

2. clone this repo

Commands
--------

`bracketeer`: Surrounds selected text with braces (or quotes - anything, really), and prevents indentation mishaps.

Required args:

`braces`: Two characters.  Default key bindings support:

* `{}`
* `[]`
* `()`
* `<>`
* `«»`
* `‹›`
* `""`
* `''`
* `“”`
* `‘’`
* `\`\``

Select some text and press one of these keys.  The default Sublime Text braces will re-indent the text, and it looks really silly.  This plugin indents sensibly.  Helpful in languages that use curlies, e.g. `C`, `Java`, `PHP`.

In addition, the "super+]" indent command is modified so that the first and last lines are not indented.  Makes it easy to add curly braces.  Select some lines of code, with a blank line above and below.  Or, if you like your braces on the same line as the `if|while|do`, put the start of the selection at the end of that line.

Press `super+]`, then press "{".  The block of code will be indented, leaving the code highlighted, then you can surround it in braces.

    1. if ( a )
    2. echo NULL;

    # add blank lines
    1. if ( a )
    2.
    3. echo NULL;
    4.

    # select text
    1. if ( a )
    2. |
    3. echo NULL;
    4. |

    # press super+]
    1. if ( a )
    2. |
    3.     echo NULL;
    4. |

    # press {
    1. if ( a )
    2. {
    3.     echo NULL;
    4. }|
