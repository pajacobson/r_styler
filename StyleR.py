import sublime
import sublime_plugin
import os
import subprocess


class StyleROnSave(sublime_plugin.EventListener):
    defaults = {
        'style_guide': "tidyverse_style",
        "scope": "tokens",
        "indentation": 2,
        "strict": "TRUE",
    }

    def on_post_save_async(self, view):

        filepath = view.file_name()
        settings = view.settings()

        if settings.has("StyleR") is False:
            settings = sublime.load_settings('StyleR.sublime-settings')

        print(settings.get("default"))

        if not view.match_selector(0, "source.r"):
            return 0

        subprocess.call(
            [
                "R",
                "--slave",
                "--vanilla",
                "-e",
                "library(styler);style_file('{0}', strict = TRUE)".format(
                    filepath
                ),
            ],
            cwd=os.path.dirname(filepath),
        )
