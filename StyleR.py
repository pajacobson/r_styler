import sublime
import sublime_plugin
import os
import subprocess


class StyleROnSave(sublime_plugin.EventListener):

    defaults = {
        "indent_by": 2,
        "strict": "TRUE",
        "on_save": True,
        "selector": "source.r | source.Rmd",
    }

    def get_settings(self):
        user_settings = sublime.load_settings('StyleR.sublime-settings')
        active = {k: user_settings.get(k, v) for k, v in self.defaults.items()}

        return active

    def on_post_save_async(self, view):

        if not view.match_selector(0, self.defaults.get('selector')):
            return 0

        settings = self.get_settings()

        if settings.get('on_save') is not True:
            return 0

        filepath = view.file_name()

        config = ", ".join(
            [
                "{0} = {1}".format(k, v)
                for k, v in settings.items()
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
