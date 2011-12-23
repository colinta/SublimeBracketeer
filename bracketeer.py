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
                substitute = lines[0] + "\n"
                for line in lines[1:-1]:
                    substitute += tab + line + "\n"
                substitute += lines[-1]
                self.view.replace(edit, region, substitute)

        self.view.end_edit(e)

