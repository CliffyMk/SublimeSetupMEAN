import os
import platform
import sublime
import sublime_plugin

SETTINGS_KEY = 'ESLint.sublime-settings'
DEFAULT_NODE_PATH = ''

class Preferences:
  def load(self, settings):
    self.node_path = settings.get('node_path', DEFAULT_NODE_PATH)

Pref = Preferences()

def plugin_loaded():
  settings = sublime.load_settings(SETTINGS_KEY)
  Pref.load(settings)
  settings.add_on_change('reload', lambda: Pref.load(settings))


class EslintExecCommand(sublime_plugin.WindowCommand):
  def run(self, files=[]):
    packages = sublime.packages_path()
    linter_path = os.path.join(packages, 'ESLint', 'linter.js')

    path = Pref.node_path
    if not path:
      if sublime.platform() == 'osx':
        path = '/usr/local/bin:' + os.environ['PATH']
      else:
        path = os.environ['PATH']

    args = {
      'cmd': [
        'node',
        linter_path,
        files[0]
      ],
      'path': path,
      'file_regex': r'ESLint: (.+)\]',
      'line_regex': r'(\d+),(\d+): (.*)$'
    }
    self.window.run_command('exec', args)

class EslintCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.run_command('eslint_exec', {
      'files': [self.window.active_view().file_name()]
    })

# ST2 backwards compatibility
if int(sublime.version()) < 3000:
  plugin_loaded()
