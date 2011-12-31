from sublime import Region
import sublime_plugin


class BracketeerCommand(sublime_plugin.TextCommand):
    def run(self, edit, braces='{}'):
        e = self.view.begin_edit('bracketeer')
        for region in self.view.sel():
            if region.empty():
                self.view.insert(edit, region.a, braces)
            else:
                substitute = self.view.substr(region)
                self.view.sel().subtract(region)
                self.view.replace(edit, region, braces[0] + substitute + braces[1])
                b = region.b if region.b > region.a else region.a
                b += len(braces)
                self.view.sel().add(Region(b, b))
        self.view.end_edit(e)


class BracketeerIndentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        e = self.view.begin_edit('bracketeer')
        if self.view.settings().get('translate_tabs_to_spaces'):
            tab = ' ' * self.view.settings().get('tab_size')
        else:
            tab = "\t"

        for region in self.view.sel():
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
                    substitute = lines[0] + "\n"
                    for line in lines[1:-1]:
                        substitute += tab + line + "\n"
                    substitute += lines[-1]
                self.view.replace(edit, region, substitute)

        self.view.end_edit(e)


class BracketeerSelectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        e = self.view.begin_edit('bracketeer')
        for region in self.view.sel():
            self.run_each(edit, region)
        self.view.end_edit(e)

    def run_each(self, edit, region):
        # find next brace
        closing_brackets = ['}', ']', ')']
        opening_brackets = ['{', '[', '(']
        match_map = {
            '}': '{',
            ']': '[',
            ')': '(',
            }
        if region.b > region.a:
            begin_point = region.a - 1
            end_point = region.b
        else:
            begin_point = region.b - 1
            end_point = region.a

        # end_point gets incremented immediately, which skips the first
        # character, *unless* the selection is empty, in which case the
        # inner contents should be selected before scanning past
        if region.empty():
            # if the current character is a bracket, and the character to the left is the
            # *matching* bracket, don't match the empty contents
            c = self.view.substr(end_point)
            if c in closing_brackets and self.view.substr(end_point - 1) == match_map[c]:
                # cursor is between two brackets - select them and return
                self.view.sel().subtract(region)
                self.view.sel().add(Region(begin_point, end_point + 1))
                return

        else:
            # if the selection is inside two brackets, select them and return
            c1 = self.view.substr(begin_point)
            c2 = self.view.substr(end_point)

            if c2 in closing_brackets and c1 == match_map[c2]:
                self.view.sel().subtract(region)
                self.view.sel().add(Region(begin_point, end_point + 1))
                return

        bracket_count = 0
        while True:
            c = self.view.substr(end_point)
            if c in closing_brackets and bracket_count == 0:
                break
            elif c in opening_brackets:
                bracket_count += 1
            elif c in closing_brackets:
                bracket_count -= 1

            end_point += 1
            if end_point >= self.view.size():
                return

        # found a bracket, scan backwards until matching bracket is found.
        # matching bracket is determined by counting closing brackets (+1)
        # and opening brackets (-1) and when the count is zero and the
        # matching opening bracket is found
        # TODO: ignore strings
        bracket_count = 0
        look_for = match_map[c]
        while True:
            c = self.view.substr(begin_point)
            if bracket_count == 0 and c == look_for:
                break
            elif c in opening_brackets:
                bracket_count += 1
            elif c in closing_brackets:
                bracket_count -= 1
            begin_point -= 1
            if begin_point < 0:
                return
            print c, bracket_count
        # the current point is to the left of the opening bracket,
        # I want it to be to the right.
        begin_point += 1
        self.view.sel().subtract(region)
        self.view.sel().add(Region(begin_point, end_point))
