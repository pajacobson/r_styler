import sublime
import sublime_plugin
import os
import subprocess


def read_user_settings():
    return sublime.load_settings('StyleR.sublime-settings')


class StyleROnSave(sublime_plugin.EventListener):

    defaults = {
        "indent_by": 2,
        "strict": "TRUE",
        "on_save": True,
        "selector": "source.r | source.Rmd",
    }

    def get_settings(self):

        user_settings = read_user_settings()
        active = {k: user_settings.get(k, v) for k, v in self.defaults.items()}

        return active

    def on_post_save_async(self, view):
        selector = "{0}".format(self.defaults.get('selector'))
        print(selector)
        if not view.match_selector(0, selector):
            return 0

        self.defaults.update(self.get_settings())
        filepath = view.file_name()

        if self.defaults.get('on_save') is not True:
            return 0

        config = ", ".join(
            [
                "{0} = {1}".format(k, v)
                for k, v in self.defaults.items()
                if k in ['indent_by', "strict"]
            ]
        )

        subprocess.call(
            [
                "R",
                "--slave",
                "--vanilla",
                "-e",
                "library(styler);style_file('{0}', {1})".format(
                    filepath, config
                ),
            ],
            cwd=os.path.dirname(filepath),
        )
