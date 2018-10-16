# -*- coding: utf-8 -*-
# Last modification: 03-09-2018 22:16:01
# --Prologue--
	# Version:
	# Author: Francisco Sobrinho
	# e-mail: francicsobrinho@gmail.com

import sublime
import sublime_plugin
from datetime import datetime as dt

def check_syntax(arr,view):
	syntax = view.settings().get('syntax').lower()
	return any([d in syntax and 'json' not in syntax for d in arr])
def comment_line(line_start,view):
	sel_origin = [sublime.Region(sel.begin()+2,sel.end()+2) for sel in view.sel()]
	view.sel().clear()
	view.sel().add(line_start)
	smart_comment([line_start],view)
	view.sel().clear()
	view.sel().add_all(sel_origin)
def getstart_offthe_currentline(view):
	
	return view.lines(list(view.sel())[0])[0]
def smart_comment(regs,view):
	
	view.run_command('toggle_comment', { 'block': sum([len(view.lines(sublime.Region(reg) if type(reg)==int else reg)) for reg in regs])>1})
def selection_to(attr,view):
	word = view.substr(view.word(list(view.sel()).pop().begin()))
	view.run_command(attr, { 'word': word })

class append_modification(sublime_plugin.TextCommand):
	def run(self,edit):
		label = 'Last modification'
		tosave = "%s: %s\n"%(label,dt.now().strftime("%d-%m-%Y %H:%M:%S"))
		linetoinsert = self.view.full_line(self.view.full_line(0).end())

		if label in self.view.substr(linetoinsert):
			self.view.replace(edit, linetoinsert, tosave)
		else:
			self.view.insert(edit, linetoinsert.begin(), tosave)

		comment_line(linetoinsert.begin(),self.view)
class smart_toggle_comment(sublime_plugin.TextCommand):
	def run(self,edit):
		smart_comment(self.view.sel(),self.view)
class append_utf8(sublime_plugin.TextCommand):
	def run(self,edit):
		if check_syntax(['python'],self.view):
			line_start = getstart_offthe_currentline(self.view).begin()
			self.view.insert(edit, line_start, '-*- coding: utf-8 -*-\n')
			comment_line(line_start,self.view)		
class append_prologue(sublime_plugin.TextCommand):
	def run(self,edit):
		sel_start = getstart_offthe_currentline(self.view).begin()
		sel_end = sel_start+self.view.insert(edit, sel_start, "--Prologue--\n\tVersion:\n\tAuthor: Francisco Sobrinho\n\te-mail: francicsobrinho@gmail.com\n\n")
		comment_line(sublime.Region(sel_start,sel_end-1),self.view)		
class ignore_word_selection(sublime_plugin.TextCommand):
	def run(self,edit):
		selection_to('ignore_word',self.view)
class add_word_selection(sublime_plugin.TextCommand):
	def run(self,edit):
		selection_to(self.view,'add_word')

class save_date(sublime_plugin.EventListener):
	def on_pre_save(self,view):
		if check_syntax(['javascript','shell','python','sql','html'],view):
			view.run_command('append_modification')