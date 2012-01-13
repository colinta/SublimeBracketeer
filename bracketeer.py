import sublime
import sublime_plugin
from sublime import Region
import re


CLOSING_BRACKETS = ['}', ']', ')']
OPENING_BRACKETS = ['{', '[', '(']


class BracketeerCommand(sublime_plugin.TextCommand):
    def run(self, edit, braces='{}'):
        e = self.view.begin_edit('bracketeer')
        regions = [region for region in self.view.sel()]

        # sort by region.end() DESC
        def compare(region_a, region_b):
            return cmp(region_b.end(), region_a.end())
        regions.sort(compare)

        for region in regions:
            if region.empty():
                self.view.insert(edit, region.a, braces)
            else:
                substitute = self.view.substr(region)
                replacement = braces[0] + substitute + braces[1]
                self.view.sel().subtract(region)

                # if we're inserting "real" brackets, not quotes:
                real_brackets = braces[0] in OPENING_BRACKETS and braces[1] in CLOSING_BRACKETS
                # check to see if entire lines are selected, and if so do some smart indenting
                bol_is_nl = region.begin() == 0 or self.view.substr(region.begin() - 1) == "\n"
                eol_is_nl = region.end() == self.view.size() - 1 or self.view.substr(region.end() - 1) == "\n"
                if real_brackets and bol_is_nl and eol_is_nl:
                    if self.view.settings().get('translate_tabs_to_spaces'):
                        tab = ' ' * self.view.settings().get('tab_size')
                    else:
                        tab = "\t"
                    indent = ''
                    final = ''
                    m = re.match('^([ \t]*)' + tab, self.view.substr(region))
                    if m:
                        indent = m.group(1)
                        final = "\n"
                    else:
                        substitute = tab + substitute
                    replacement = indent + braces[0] + "\n" + substitute + indent + braces[1] + final
                    b = region.begin() + len(replacement) - len("\n" + indent + braces[1] + final)
                else:
                    b = region.begin() + len(replacement)
                self.view.replace(edit, region, replacement)
                self.view.sel().add(Region(b, b))
        self.view.end_edit(e)


class BracketeerIndentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        e = self.view.begin_edit('bracketeer')
        if self.view.settings().get('translate_tabs_to_spaces'):
            tab = ' ' * self.view.settings().get('tab_size')
        else:
            tab = "\t"

        regions = [region for region in self.view.sel()]

        # sort by region.end() DESC
        def compare(region_a, region_b):
            return cmp(region_b.end(), region_a.end())
        regions.sort(compare)

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
    def find_brackets(self, region, search_brackets=None):
        match_map = {
            '}': '{',
            ']': '[',
            ')': '(',
            }
        # find next brace in search_brackets
        if not search_brackets:
            search_brackets = ['}', ']', ')']
        elif isinstance(search_brackets, str):
            search_brackets = [search_brackets]
        begin_point = region.begin() - 1
        end_point = region.end()

        # end_point gets incremented immediately, which skips the first
        # character, *unless* the selection is empty, in which case the
        # inner contents should be selected before scanning past
        if region.empty():
            # if the current character is a bracket, and the character to the left is the
            # *matching* bracket, don't match the empty contents
            c = self.view.substr(end_point)
            if c in search_brackets and self.view.substr(end_point - 1) == match_map[c]:
                # cursor is between two brackets - select them and return
                return Region(begin_point, end_point + 1)

        else:
            # if the selection is inside two brackets, select them and return
            c1 = self.view.substr(begin_point)
            c2 = self.view.substr(end_point)

            if c2 in search_brackets and c1 == match_map[c2]:
                return Region(begin_point, end_point + 1)

        # scan forward searching for a closing bracket.
        bracket_count = 0
        while True:
            c = self.view.substr(end_point)
            if self.view.score_selector(end_point, 'string') == 0:
                if bracket_count <= 0 and c in search_brackets:
                    break
                elif c in OPENING_BRACKETS:
                    bracket_count += 1
                elif c in CLOSING_BRACKETS:
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
            if self.view.score_selector(begin_point, 'string') == 0:
                if bracket_count == 0 and c == look_for:
                    break
                elif c in OPENING_BRACKETS:
                    bracket_count += 1
                elif c in CLOSING_BRACKETS:
                    bracket_count -= 1
            begin_point -= 1
            if begin_point < 0:
                return None
        # the current point is to the left of the opening bracket,
        # I want it to be to the right.
        begin_point += 1
        return Region(begin_point, end_point)


class BracketeerGotoCommand(BracketeerBracketMatcher):
    def run(self, edit, **kwargs):
        e = self.view.begin_edit('bracketeer')
        regions = [region for region in self.view.sel()]

        # sort by region.end() DESC
        def compare(region_a, region_b):
            return cmp(region_b.end(), region_a.end())
        regions.sort(compare)

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
        def compare(region_a, region_b):
            return cmp(region_b.end(), region_a.end())
        regions.sort(compare)

        for region in regions:
            self.run_each(edit, region, **kwargs)
        self.view.end_edit(e)

    def run_each(self, edit, region):
        new_region = self.find_brackets(region)
        if new_region:
            self.view.sel().subtract(region)
            self.view.sel().add(new_region)
            self.view.show(new_region.b)
