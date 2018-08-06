"""Dynamically completes text for relative paths.

This looks for text scoped by meta.filepath.relative.
"""
import sublime
import sublime_plugin
import os


class FilenameCompletion(sublime_plugin.EventListener):
	def on_query_completions(self, view, prefix, locations):
		if view.file_name() is None:
			return
		if len(locations) != 1:
			return

		[point] = locations  # type: sublime.Point

		if not view.match_selector(point, "meta.filepath.relative"):
			return

		region = view.extract_scope(point)
		region.b = min(region.b, point) # Ignore stuff after the cursor.

		prefix = view.substr(region)

		if os.path.isdir(prefix):
			folder = prefix
			stem = ''
		else:
			folder, stem = os.path.split(prefix)

		try:
			contents = os.listdir(os.path.join(
				os.path.dirname(view.file_name()), 
				folder,
			))
		except FileNotFoundError:
			return ([], sublime.INHIBIT_WORD_COMPLETIONS)

		return (
			[
				hint(folder, item)
				for item in contents
				if item.startswith(stem)
			],
			sublime.INHIBIT_WORD_COMPLETIONS,
		)

def hint(folder, stem):
	if folder:
		path = folder + '/' + stem
	else:
		path = stem
	if '.' in stem:
		return '{}\t.{}'.format(path, stem.rsplit('.', 1)[-1]), path
	else: 
		return path + '\t<none>', path
