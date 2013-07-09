Bracketeer plugin for Sublime Text 2
=====================================

Some bracket manipulation, selection, and insertion commands.


Installation
------------

### Sublime Text 2

1. Using Package Control, install "Bracketeer"

Or:

1. Open the Sublime Text 2 Packages folder

    - OS X: ~/Library/Application Support/Sublime Text 2/Packages/
    - Windows: %APPDATA%/Sublime Text 2/Packages/
    - Linux: ~/.Sublime Text 2/Packages/

2. clone this repo
3. Install keymaps for the commands (see Example.sublime-keymap for my preferred keys)

### Sublime Text 3

1. Open the Sublime Text 2 Packages folder
2. clone this repo, but use the `st3` branch

       git clone -b st3 git@github.com:colinta/SublimeBracketeer

Commands
--------

`bracketeer`: Surrounds selected text with braces (or quotes - anything, really), and prevents indentation mishaps.

`bracketeer_indent`: Indents sensibly - allows a clever use of enter, indent, and '{' to surround code in '{}'.  See example below.

`bracketeer_goto`: Goes to the matching bracket - either opener (ctrl+[), closer (ctrl+]), or *both* (ctrl+alt+[).

`bracketeer_select`: Searches for matching brackets and selects what is inside, or expands the selection to include the brackets.


### bracketeer


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

In addition, the "super+]" indent command is modified (using `bracketeer_indent`) so that the first and last lines are not indented.  Makes it easy to add curly braces.  Select some lines of code, with a blank line above and below.  Or, if you like your braces on the same line as the `if|while|do`, put the start of the selection at the end of that line.

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


### bracketeer_indent


Default key combination is super+]

If the first line of selected text is empty (and keep in mind this *ignores* whatever text is to the left of the selection, so not necessarily an empty line), that line will not be indented.  See example usage above.


### bracketeer_select


Default key combination is ctrl+shift+[

Expands the current region to include text *within* brackets, and if pressed again to include the brackets themselves.

I will use '|' as the caret or selection start and end points:

    1. do_something([1, '[', {'brace':'{', 'test'}])|

    # move caret into the 'test' string
    1. do_something([1, '[', {'brace':'{', 'te|st'}])

    # press ctrl+shift+[
    # the first bracket it finds is the '}', so it will match {}s
    # notice it will ignore the '{', which would otherwise look like the matching brace
    1. do_something([1, '[', {|'brace':'{', 'test'|}])

    # press ctrl+shift+[
    # adds the {} to the selection
    1. do_something([1, '[', |{'brace':'{', 'test'}|])

    # press ctrl+shift+[
    # selects between the []s.
    1. do_something([|1, '[', {'brace':'{', 'test'}|])

    # press ctrl+shift+[
    # selects the []s.
    1. do_something(|[1, '[', {'brace':'{', 'test'}]|)

    # press ctrl+shift+[
    # selects the ()s. It would have expanded to select *between* the (), but that is what the selection already *was to start with*
    1. do_something|([1, '[', {'brace':'{', 'test'}])|

    # press ctrl+shift+[
    # does nothing.  No more brackets to match!
    1. do_something|([1, '[', {'brace':'{', 'test'}])|
