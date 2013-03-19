# coding: utf8
import sublime
import sublime_plugin
from sublime import Region
import re

# for detecting "real" brackets in BracketeerCommand, and bracket matching in BracketeerBracketMatcher
OPENING_BRACKETS = ['{', '[', '(']
OPENING_BRACKET_LIKE = ['{', '[', '(', '"', "'", u'“', '‘', '«', '‹']
CLOSING_BRACKETS = ['}', ']', ')']
CLOSING_BRACKET_LIKE = ['}', ']', ')', '"', "'", u'”', '’', '»', '›']
QUOTING_BRACKETS = ['\'', "\""]


class BracketeerCommand(sublime_plugin.TextCommand):
    def run(self, edit, **kwargs):
        e = self.view.begin_edit('bracketeer')
        regions = [region for region in self.view.sel()]

        # sort by region.end() DESC
        def get_end(region):
            return region.end()
        regions.sort(key=get_end, reverse=True)

        for region in regions:
            self.run_each(edit, region, **kwargs)

        self.view.end_edit(e)

    def complicated_quote_checker(self, insert_braces, region, pressed, after, r_brace):
        in_string_scope = self.view.score_selector(region.a, 'string')
        in_double_string_scope = in_string_scope and self.view.score_selector(region.a, 'string.quoted.double')
        in_single_string_scope = in_string_scope and self.view.score_selector(region.a, 'string.quoted.single')
        at_eol = region.a == self.view.line(region.a).b
        in_comment_scope = self.view.score_selector(region.a, 'comment')
        in_text_scope = self.view.score_selector(region.a, 'text')
        in_embedded_scope = self.view.score_selector(region.a, 'source.php') + self.view.score_selector(region.a, 'source.js')
        in_text_scope = in_text_scope and not in_embedded_scope

        if pressed and pressed in QUOTING_BRACKETS and (in_comment_scope or in_text_scope or in_string_scope):
            # if the cursor:
            # (a) is preceded by odd numbers of '\'s?
            if in_comment_scope:
                scope_test = 'comment'
            else:
                scope_test = 'string'
            begin_of_string = region.a
            while begin_of_string and self.view.score_selector(begin_of_string - 1, scope_test):
                begin_of_string -= 1
            check_a = self.view.substr(Region(begin_of_string, region.a))
            check_a = len(re.search(r'[\\]*$', check_a).group(0))
            check_a = check_a % 2

            # (b) is an apostrophe and (inside double quotes or in text or comment scope)
            check_b = (in_double_string_scope or in_text_scope or in_comment_scope) and pressed == "'"

            # (c) we are at the end of the line and pressed the closing quote
            check_c = at_eol and (
                in_single_string_scope and pressed == "'"
                or
                in_double_string_scope and pressed == '"'
                )

            # then don't insert both, just insert the one.
            if check_a or check_b or check_c:
                return pressed

    def run_each(self, edit, region, braces='{}', pressed=None, unindent=False, select=False, replace=False):
        self.view.sel().subtract(region)
        if self.view.settings().get('translate_tabs_to_spaces'):
            tab = ' ' * self.view.settings().get('tab_size')
        else:
            tab = "\t"

        row, col = self.view.rowcol(region.begin())
        indent_point = self.view.text_point(row, 0)
        if indent_point < region.begin():
            indent = self.view.substr(Region(indent_point, region.begin()))
            indent = re.match('[ \t]*', indent).group(0)
        else:
            indent = ''
        line = self.view.substr(self.view.line(region.a))
        selection = self.view.substr(region)

        # for braces that have newlines ("""), insert the current line's indent
        if isinstance(braces, list):
            l_brace = braces[0]
            r_brace = braces[1]
            braces = ''.join(braces)
            braces = braces.replace("\n", "\n" + indent)
            length = len(l_brace)
        else:
            braces = braces.replace("\n", "\n" + indent)
            length = len(braces) / 2
            l_brace = braces[:length]
            r_brace = braces[length:]

        if region.empty():
            after = self.view.substr(Region(region.a, region.a + length))

            insert_braces = braces
            complicated_check = self.complicated_quote_checker(insert_braces, region, pressed, after, r_brace)

            if complicated_check:
                insert_braces = complicated_check
            elif pressed and after == r_brace and r_brace[-1] == pressed:  # and (pressed not in QUOTING_BRACKETS or in_string_scope):
                # in this case we pressed the closing character, and that's the character that is to the right
                # so do nothing except advance cursor position
                insert_braces = False
            elif unindent and row > 0 and indent and line == indent:
                # indent has the current line's indent
                # get previous line's indent:
                prev_point = self.view.text_point(row - 1, 0)
                prev_line = self.view.line(prev_point)
                prev_indent = self.view.substr(prev_line)
                prev_indent = re.match('[ \t]*', prev_indent).group(0)

                if (not pressed or pressed == l_brace) and len(indent) > len(prev_indent) and indent[len(prev_indent):] == tab:
                    # move region.a back by 'indent' amount
                    region = Region(region.a - len(tab), region.b - len(tab))
                    # and remove the tab
                    self.view.replace(edit, Region(region.a, region.a + len(tab) - 1), '')
                elif pressed and pressed == r_brace:
                    if len(indent) == len(prev_indent):
                        # move region.a back by 'indent' amount
                        region = Region(region.a - len(tab), region.b - len(tab))
                        # and remove the tab
                        self.view.replace(edit, Region(region.a, region.a + len(tab) - 1), '')
                    insert_braces = r_brace
            elif pressed and pressed != l_brace:
                # we pressed the closing bracket or quote.  This *never*
                insert_braces = r_brace

            if insert_braces:
                self.view.insert(edit, region.a, insert_braces)
            self.view.sel().add(Region(region.a + length, region.a + length))
        elif selection in QUOTING_BRACKETS and pressed in QUOTING_BRACKETS and selection != pressed:
            # changing a quote from single <=> double, just insert the quote.
            self.view.replace(edit, region, pressed)
            self.view.sel().add(Region(region.end(), region.end()))
        elif pressed and pressed != l_brace:
            b = region.begin() + len(r_brace)
            self.view.replace(edit, region, r_brace)
            self.view.sel().add(Region(b, b))
        else:
            substitute = self.view.substr(region)
            replacement = l_brace + substitute + r_brace
            # if we're inserting "real" brackets, not quotes:
            real_brackets = l_brace in OPENING_BRACKETS and r_brace in CLOSING_BRACKETS
            # check to see if entire lines are selected, and if so do some smart indenting
            bol_is_nl = region.begin() == 0 or self.view.substr(region.begin() - 1) == "\n"
            eol_is_nl = region.end() == self.view.size() - 1 or self.view.substr(region.end() - 1) == "\n"
            if real_brackets and bol_is_nl and eol_is_nl:
                indent = ''
                final = ''
                m = re.match('([ \t]*)' + tab, self.view.substr(region))
                if m:
                    indent = m.group(1)
                    final = "\n"
                else:
                    substitute = tab + substitute
                replacement = indent + l_brace + "\n" + substitute + indent + r_brace + final
                b = region.begin() + len(replacement) - len("\n" + indent + r_brace + final)
            else:
                b = region.begin() + len(replacement)

            if replace and self.view.substr(region.begin() - 1) in OPENING_BRACKET_LIKE and self.view.substr(region.end()) in CLOSING_BRACKET_LIKE:
                b -= 1
                self.view.replace(edit, Region(region.begin() - 1, region.end() + 1), replacement)
            elif replace and self.view.substr(region.begin()) in OPENING_BRACKET_LIKE and self.view.substr(region.end() - 1) in CLOSING_BRACKET_LIKE:
                replacement = l_brace + replacement[2:-2] + r_brace
                b -= 2
                self.view.replace(edit, region, replacement)
                l_brace = r_brace = ''
            else:
                self.view.replace(edit, region, replacement)

            if select:
                self.view.sel().add(Region(b - len(replacement) + len(l_brace), b - len(r_brace)))
            else:
                self.view.sel().add(Region(b, b))


class BracketeerIndentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        e = self.view.begin_edit('bracketeer')
        if self.view.settings().get('translate_tabs_to_spaces'):
            tab = ' ' * self.view.settings().get('tab_size')
        else:
            tab = "\t"

        regions = [region for region in self.view.sel()]

        # sort by region.end() DESC
        def get_end(region):
            return region.end()
        regions.sort(key=get_end, reverse=True)

        for region in regions:
            if region.empty():
                # insert tab at beginning of line
                point = self.view.text_point(self.view.rowcol(region.a)[0], 0)
                self.view.insert(edit, point, tab)
            else:
                # insert tab in front of lines 1:-1
                lines = self.view.substr(region).split("\n")
                # just one line?  indent it
                if len(lines) == 1:
                    substitute = tab + lines[0] + "\n"
                else:
                    default_settings = sublime.load_settings("bracketeer.sublime-settings")
                    dont_indent_list = default_settings.get('dont_indent')

                    # lines that start with these strings don't get indented
                    def dont_indent(line):
                        return any(dont for dont in dont_indent_list if line[:len(dont)] == dont)

                    # cursor is at start of line?  indent that, too
                    if len(lines[0]) > 0 and not dont_indent(lines[0]):
                        substitute = tab
                    else:
                        substitute = ''
                    substitute += lines[0] + "\n"

                    for line in lines[1:-1]:
                        if len(line):
                            if not dont_indent(line):
                                substitute += tab
                            substitute += line
                        substitute += "\n"
                    substitute += lines[-1]
                self.view.replace(edit, region, substitute)

        self.view.end_edit(e)


class BracketeerBracketMatcher(sublime_plugin.TextCommand):
    def find_brackets(self, region, closing_search_brackets=None):
        match_map = {
            '}': '{',
            ']': '[',
            ')': '(',
            }
        # find next brace in closing_search_brackets
        if not closing_search_brackets:
            closing_search_brackets = CLOSING_BRACKETS
        elif isinstance(closing_search_brackets, basestring):
            closing_search_brackets = [closing_search_brackets]

        opening_search_brackets = [match_map[bracket] for bracket in closing_search_brackets]
        begin_point = region.begin() - 1
        end_point = region.end()

        # LaTEX: if selection directly preceeds \right, examine the string that includes \right instead of the actual selection
        if self.view.substr( Region(end_point, min(end_point+6,self.view.size())) ) == '\\right': end_point += 6
        # /LaTEX

        # end_point gets incremented immediately, which skips the first
        # character, *unless* the selection is empty, in which case the
        # inner contents should be selected before scanning past
        if region.empty():
            # if the current character is a bracket, and the character to the left is the
            # *matching* bracket, don't match the empty contents
            c = self.view.substr(end_point)
            if c in closing_search_brackets and self.view.substr(end_point - 1) == match_map[c]:
                # cursor is between two brackets - select them and return
                return Region(begin_point, end_point + 1)

        else:
            # if the selection is inside two brackets, select them and return
            c1 = self.view.substr(begin_point)
            c2 = self.view.substr(end_point)

            if c2 in closing_search_brackets and c1 == match_map[c2]:
                # LaTEX: if \left preceeds selection, select it as well
                if self.view.substr(Region(max(begin_point-5,0), begin_point))=='\left': begin_point -= 5
                # /LaTEX
                return Region(begin_point, end_point + 1)

        # scan forward searching for a closing bracket.
        started_in_string = bool(self.view.score_selector(end_point, 'string') or self.view.score_selector(begin_point, 'string'))
        bracket_count = 0
        while True:
            c = self.view.substr(end_point)
            if started_in_string or not self.view.score_selector(end_point, 'string'):
                if bracket_count <= 0 and c in closing_search_brackets:
                    break
                elif c in opening_search_brackets and c in OPENING_BRACKETS:
                    bracket_count += 1
                elif c in closing_search_brackets and c in CLOSING_BRACKETS:
                    bracket_count -= 1

            end_point += 1
            if end_point >= self.view.size():
                return None

        # found a bracket, scan backwards until matching bracket is found.
        # matching bracket is determined by counting closing brackets (+1)
        # and opening brackets (-1) and when the count is zero and the
        # matching opening bracket is found
        look_for = match_map[c]
        while True:
            c = self.view.substr(begin_point)
            if started_in_string or not self.view.score_selector(begin_point, 'string'):
                if bracket_count == 0 and c == look_for:
                    break
                elif c in opening_search_brackets and c in OPENING_BRACKETS:
                    bracket_count += 1
                elif c in closing_search_brackets and c in CLOSING_BRACKETS:
                    bracket_count -= 1
            begin_point -= 1
            if begin_point < 0:
                return None
        # the current point is to the left of the opening bracket,
        # I want it to be to the right.
        begin_point += 1

        # LaTEX: if selection ends in \right, don't select it
        if self.view.substr( Region(max(end_point-6,0), end_point) ) == '\\right': end_point -= 6
        # /LaTEX
        return Region(begin_point, end_point)


class BracketeerGotoCommand(BracketeerBracketMatcher):
    def run(self, edit, **kwargs):
        e = self.view.begin_edit('bracketeer')
        regions = [region for region in self.view.sel()]

        # sort by region.end() DESC
        def get_end(region):
            return region.end()
        regions.sort(key=get_end, reverse=True)

        for region in regions:
            self.run_each(edit, region, **kwargs)
        self.view.end_edit(e)

    def run_each(self, edit, region, goto):
        cursor = region.b
        if goto == "left" and self.view.substr(cursor - 1) == '{':
            cursor -= 1
        elif goto == "both" and self.view.substr(cursor) == '{':
            cursor += 1
        elif goto in ["left", "both"] and self.view.substr(cursor - 1) == '}':
            cursor -= 1

        new_region = self.find_brackets(Region(cursor, cursor), '}')

        if new_region:
            self.view.sel().subtract(region)
            a = new_region.begin()
            b = new_region.end()
            if self.view.substr(a) in OPENING_BRACKETS:
                a += 1
            if self.view.substr(b) in CLOSING_BRACKETS:
                b += 1

            if goto == "left":
                new_region = Region(a, a)
                self.view.sel().add(new_region)
                self.view.show(new_region)
            elif goto == "right":
                new_region = Region(b, b)
                self.view.sel().add(new_region)
                self.view.show(new_region)
            elif goto == "both":
                self.view.sel().add(Region(a, a))
                self.view.sel().add(Region(b, b))
                self.view.show(new_region.b)
            else:
                raise ValueError("`goto` should have a value of 'left', 'right', or 'both'), not '" + goto + '"')


class BracketeerSelectCommand(BracketeerBracketMatcher):
    def run(self, edit, **kwargs):
        e = self.view.begin_edit('bracketeer')
        regions = [region for region in self.view.sel()]

        # sort by region.end() DESC
        def get_end(region):
            return region.end()
        regions.sort(key=get_end, reverse=True)

        for region in regions:
            self.run_each(edit, region, **kwargs)
        self.view.end_edit(e)

    def run_each(self, edit, region):
        new_region = self.find_brackets(region)
        if new_region:
            self.view.sel().subtract(region)
            self.view.sel().add(new_region)
            self.view.show(new_region.b)
