Bracketeer
==========

Some bracket manipulation, selection, and insertion commands.

Installation
------------

Using Package Control, install "Bracketeer" or clone this repo in your packages folder.

I recommended you add key bindings for the commands. I've included my preferred bindings below.
Copy them to your key bindings file (⌘⇧,).

Commands
--------

`bracketeer`: Surrounds selected text with braces (or quotes - anything, really), and prevents indentation mishaps.

`bracketeer_indent`: Indents sensibly - allows a clever use of enter, indent, and '{' to surround code in '{}'.  See example below.

`bracketeer_goto`: Goes to the matching bracket - either opener, closer, or *both* (creates two cursors).

`bracketeer_select`: Searches for matching brackets and selects what is inside, or expands the selection to include the brackets.

Key Bindings
------------

Copy these to your user key bindings file.

<!-- keybindings start -->
    { "keys": ["super+]"], "command": "bracketeer_indent" },
    { "keys": ["ctrl+shift+["], "command": "bracketeer_select" },

    { "keys": ["ctrl+["], "command": "bracketeer_goto", "args": { "goto": "left" } },
    { "keys": ["ctrl+]"], "command": "bracketeer_goto", "args": { "goto": "right" } },
    { "keys": ["ctrl+alt+["], "command": "bracketeer_goto", "args": { "goto": "both" } },
    { "keys": ["ctrl+alt+]"], "command": "bracketeer_goto", "args": { "goto": "both" } },
    //|
    //|  BRACKETEER
    //|
    { "keys": ["{"], "command": "bracketeer", "args": { "braces": "{}" } },
    { "keys": ["}"], "command": "bracketeer", "args": { "braces": "{}", "pressed": "}", "unindent": true } },
    { "keys": ["["], "command": "bracketeer", "args": { "braces": "[]" } },
    { "keys": ["]"], "command": "bracketeer", "args": { "braces": "[]", "pressed": "]" } },
    { "keys": ["("], "command": "bracketeer", "args": { "braces": "()" } },
    { "keys": [")"], "command": "bracketeer", "args": { "braces": "()", "pressed": ")" } },

    //|  reStructured Text
    { "keys": ["alt+`"], "command": "bracketeer", "args": { "braces": "````", "pressed": "``" }, "context":
        [
            { "key": "selector", "operator": "equal", "operand": "text.restructuredtext" }
        ]
    },
    { "keys": ["*"], "command": "bracketeer", "args": { "braces": "**", "pressed": "*" }, "context":
        [
            { "key": "selector", "operator": "equal", "operand": "text.restructuredtext" }
        ]
    },

    //|  DJANGO CURLIES
    // For django, liquid, jinja.  All the grammars *I* have list 'source.smarty' as
    // when the cursor is inside "{}"s
    { "keys": ["{"], "command": "bracketeer", "args": { "braces": "{  }" }, "context":
        [{ "key": "selector", "operator": "equal", "operand": "source.smarty" }]
    },
    { "keys": ["{"], "command": "bracketeer", "args": { "braces": "{  }" }, "context":
        [{ "key": "selector", "operator": "equal", "operand": "meta.brace.curly" }]
    },
    { "keys": ["%"], "command": "bracketeer", "args": { "braces": "%  %" }, "context":
        [{ "key": "selector", "operator": "equal", "operand": "source.smarty" }]
    },
    { "keys": ["%"], "command": "bracketeer", "args": { "braces": "%  %" }, "context":
        [
            { "key": "selector", "operator": "equal", "operand": "meta.brace.curly" },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "<$", "match_all": true }
        ]
    },
    { "keys": ["%"], "command": "insert_snippet", "args": { "contents": " $1 %>$0" }, "context":
        [
            { "key": "selector", "operator": "equal", "operand": "source.ruby" },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "<%$", "match_all": true }
        ]
    },
    { "keys": [">"], "command": "insert_snippet", "args": { "contents": ">$1<% $0" }, "context":
        [
            { "key": "selector", "operator": "equal", "operand": "source.ruby" },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "%$", "match_all": true }
        ]
    },
    { "keys": ["="], "command": "insert_snippet", "args": { "contents": "= $1 %>$0" }, "context":
        [
            { "key": "selector", "operator": "equal", "operand": "source.ruby" },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "<%$", "match_all": true }
        ]
    },
    { "keys": ["-"], "command": "insert_snippet", "args": { "contents": "- $1 %>$0" }, "context":
        [
            { "key": "selector", "operator": "equal", "operand": "source.ruby" },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "<%$", "match_all": true }
        ]
    },
    { "keys": ["#"], "command": "bracketeer", "args": { "braces": "#  #" }, "context":
        [{ "key": "selector", "operator": "equal", "operand": "source.smarty" }]
    },

    //|  QUOTES
    { "keys": ["\""], "command": "bracketeer", "args": { "braces": "\"\"", "pressed": "\"" } },
    { "keys": ["ctrl+'","ctrl+'"], "command": "bracketeer", "args": { "braces": "\"\"\"\n\n\"\"\"" } },
    { "keys": ["'"], "command": "bracketeer", "args": { "braces": "''", "pressed": "'" } },
    { "keys": ["ctrl+'","'"], "command": "bracketeer", "args": { "braces": "'''\n\n'''" } },
    { "keys": ["`"], "command": "bracketeer", "args": { "braces": "``", "pressed": "`" } },
    { "keys": ["ctrl+'","`"], "command": "insert_snippet", "args": { "contents": "```${1:syntax}\n$0\n```" } },
    { "keys": ["|"], "command": "bracketeer", "args": { "braces": "||", "pressed": "|" } },
    { "keys": ["«"], "command": "bracketeer", "args": { "braces": "«»" } },
    { "keys": ["»"], "command": "bracketeer", "args": { "braces": "«»", "pressed": "»" } },
    { "keys": ["‹"], "command": "bracketeer", "args": { "braces": "‹›" } },
    { "keys": ["›"], "command": "bracketeer", "args": { "braces": "‹›", "pressed": "›" } },
    { "keys": ["“"], "command": "bracketeer", "args": { "braces": "“”" } },
    { "keys": ["”"], "command": "bracketeer", "args": { "braces": "“”", "pressed": "”" }  },
    { "keys": ["‘"], "command": "bracketeer", "args": { "braces": "‘’" } },
    { "keys": ["’"], "command": "bracketeer", "args": { "braces": "‘’", "pressed": "’" } },

    //|
    //|  AUTO DELETE MATCHING '', "", [], etc.
    //|
    { "keys": ["backspace"], "command": "run_macro_file", "args": {"file": "Packages/Default/Delete Left Right.sublime-macro"}, "context":
        [
            { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
            { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "\"$" },
            { "key": "following_text", "operator": "regex_contains", "operand": "^\"" }
        ]
    },
    { "keys": ["backspace"], "command": "run_macro_file", "args": {"file": "Packages/Default/Delete Left Right.sublime-macro"}, "context":
        [
            { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
            { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "'$" },
            { "key": "following_text", "operator": "regex_contains", "operand": "^'" }
        ]
    },
    { "keys": ["backspace"], "command": "run_macro_file", "args": {"file": "Packages/Default/Delete Left Right.sublime-macro"}, "context":
        [
            { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
            { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "`$" },
            { "key": "following_text", "operator": "regex_contains", "operand": "^`" }
        ]
    },
    { "keys": ["backspace"], "command": "run_macro_file", "args": {"file": "Packages/Default/Delete Left Right.sublime-macro"}, "context":
        [
            { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
            { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "«$" },
            { "key": "following_text", "operator": "regex_contains", "operand": "^»" }
        ]
    },
    { "keys": ["backspace"], "command": "run_macro_file", "args": {"file": "Packages/Default/Delete Left Right.sublime-macro"}, "context":
        [
            { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
            { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "‹$" },
            { "key": "following_text", "operator": "regex_contains", "operand": "^›" }
        ]
    },
    { "keys": ["backspace"], "command": "run_macro_file", "args": {"file": "Packages/Default/Delete Left Right.sublime-macro"}, "context":
        [
            { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
            { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "“$" },
            { "key": "following_text", "operator": "regex_contains", "operand": "^”" }
        ]
    },
    { "keys": ["backspace"], "command": "run_macro_file", "args": {"file": "Packages/Default/Delete Left Right.sublime-macro"}, "context":
        [
            { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
            { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "‘$" },
            { "key": "following_text", "operator": "regex_contains", "operand": "^’" }
        ]
    },
    { "keys": ["backspace"], "command": "run_macro_file", "args": {"file": "Packages/Default/Delete Left Right.sublime-macro"}, "context":
        [
            { "key": "selector", "operator": "equal", "operand": "text.restructuredtext" },
            { "key": "setting.auto_match_enabled", "operator": "equal", "operand": true },
            { "key": "selection_empty", "operator": "equal", "operand": true, "match_all": true },
            { "key": "preceding_text", "operator": "regex_contains", "operand": "\\*$" },
            { "key": "following_text", "operator": "regex_contains", "operand": "^\\*" }
        ]
    },

    //|
    //|  Bracket and select
    //|
    { "keys": ["ctrl+alt+[", "backspace"], "command": "bracketeer", "args": { "braces": "", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "d"], "command": "bracketeer", "args": { "braces": ["do", "end"], "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "d"], "command": "bracketeer", "args": { "braces": ["do", "end"], "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "{"], "command": "bracketeer", "args": { "braces": "{}", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "{"], "command": "bracketeer", "args": { "braces": "{}", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", " "], "command": "bracketeer", "args": { "braces": "  ", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", " "], "command": "bracketeer", "args": { "braces": "  ", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "["], "command": "bracketeer", "args": { "braces": "[]", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "["], "command": "bracketeer", "args": { "braces": "[]", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "("], "command": "bracketeer", "args": { "braces": "()", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "("], "command": "bracketeer", "args": { "braces": "()", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "\""], "command": "bracketeer", "args": { "braces": "\"\"", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "\""], "command": "bracketeer", "args": { "braces": "\"\"", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "ctrl+shift+'"], "command": "bracketeer", "args": { "braces": "\"\"\"\"\"\"", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "ctrl+shift+'"], "command": "bracketeer", "args": { "braces": "\"\"\"\"\"\"", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "'"], "command": "bracketeer", "args": { "braces": "''", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "'"], "command": "bracketeer", "args": { "braces": "''", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "ctrl+'"], "command": "bracketeer", "args": { "braces": "''''''", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "ctrl+'"], "command": "bracketeer", "args": { "braces": "''''''", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "`"], "command": "bracketeer", "args": { "braces": "``", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "`"], "command": "bracketeer", "args": { "braces": "``", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "ctrl+`"], "command": "bracketeer", "args": { "braces": "``````", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "ctrl+`"], "command": "bracketeer", "args": { "braces": "``````", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "«"], "command": "bracketeer", "args": { "braces": "«»", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "«"], "command": "bracketeer", "args": { "braces": "«»", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "‹"], "command": "bracketeer", "args": { "braces": "‹›", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "‹"], "command": "bracketeer", "args": { "braces": "‹›", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "“"], "command": "bracketeer", "args": { "braces": "“”", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "“"], "command": "bracketeer", "args": { "braces": "“”", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "‘"], "command": "bracketeer", "args": { "braces": "‘’", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "‘"], "command": "bracketeer", "args": { "braces": "‘’", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "alt+`"], "command": "bracketeer", "args": { "braces": "````", "select": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+alt+[", "alt+`"], "command": "bracketeer", "args": { "braces": "````", "select": true, "replace": true }, "context":
        [{ "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true }]
    },
    { "keys": ["ctrl+[", "*"], "command": "bracketeer", "args": { "braces": "**", "select": true }, "context":
        [
            { "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true },
            { "key": "selector", "operator": "equal", "operand": "text.restructuredtext" }
        ]
    },
    { "keys": ["ctrl+alt+[", "*"], "command": "bracketeer", "args": { "braces": "**", "select": true, "replace": true }, "context":
        [
            { "key": "selection_empty", "operator": "equal", "operand": false, "match_all": true },
            { "key": "selector", "operator": "equal", "operand": "text.restructuredtext" }
        ]
    },
<!-- keybindings stop -->

In depth
--------

### Command: `bracketeer`

> Default key combination: any opening bracket or quote character, possibly combined with `select` and `replace` options

Options:

`braces`: *Required* String with open/close characters, or list of `[open, close]`.  Default key bindings support:

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

`select`: *Default: false* Whether to select the text after brackets are inserted.  Sublime Text usually *does* keep the text selected, so this command emulates that behavior.  The example keymap file has these mapped to `["ctrl+[", bracket]`

`replace`: If the selection is contained inside bracket characters, they will be replaced with new brackets.  For example, to change curly brackets to square brackets:

1. Use `bracketeer_select` to select inside the curly brackets
2. Press `"ctrl+alt+[", "["` (from Example.sublime-keymap) and '(text)' changes to '[text]'

The default Sublime Text command re-indents text after pressing a bracket key, and it looks really silly to me.  This plugin indents sensibly.  Helpful in languages that use curlies, e.g. `C`, `Java`, `PHP`.

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
    3.     echo NULL;|   # notice, the cursor moves *inside* the new brackets
    4. }

If you prefer "Kernigan and Ritchie" style brackets, start the selection on the previous line

    1. if ( a )
    2. echo NULL;
    3.

    # select text
    1. if ( a )|
    2. echo NULL;
    3. |

    # press super+]
    1. if ( a )|
    2.     echo NULL;
    3. |

    # press {
    1. if ( a ) {        # a space is inserted before the '{' (unless it's already there!)
    2.     echo NULL;|   # and again, the cursor moves *inside* the new brackets
    3. }

### Command: `bracketeer_indent`

> Default key combination is super+]

If the first line of selected text is empty (and keep in mind this *ignores* whatever text is to the left of the selection, so not necessarily an empty line), that line will not be indented.  See example usage above.


### Command: `bracketeer_select`

> Default key combination is ctrl+shift+[

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

