#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import os
from re import S
from winsound import Beep
from playsound import playsound
import wx
import sys

from Puzzle import Puzzle

sys.path.append("ui")
from KeyboardListenerWindow import KeyboardListenerWindow
from SelectRowColWindow import SelectRowColWindow

class PuzzleWindow(KeyboardListenerWindow):

	def __init__(self,title="拜玛拼图",message="按光标键可以查看方块。",*args, **kw) -> None:
		super().__init__(title=title, message=message,*args, **kw)
		row, col=self.read_row_col()
		self.puzzle=Puzzle(row=row, col=col)


	def read_row_col(self):
		"读取保存的行列数。"

		self.row_col_path="config/row_col.json"
		if not os.path.exists(self.row_col_path): return 3,3

		with open(self.row_col_path, "r")as f:
			d =json.load(f)
			return d["row"], d["col"]


	def on_char_hook(self, event:wx.KeyEvent):
		self.view_puzzle_block(event)
		self.move_puzzle_block(event)
		self.disorder(event)
		self.order(event)
		self.start_select_row_col(event)
		event.Skip()


	def    start_select_row_col(self, event:wx.KeyEvent):
		if event.ControlDown() and event.GetKeyCode()==ord("R"):
			SelectRowColWindow(self.select_row_col)


	def select_row_col(self, row,col):
		self.puzzle=Puzzle(row=row, col=col)
		super().show_message("拼图现在已经是%s行%s列了。" %(row, col)+self.puzzle.get_focus_block_message())

		# 保存到本地
		d={"row": row, "col": col}
		if not os.path.exists(self.row_col_path): os.makedirs(os.path.dirname(self.row_col_path))
		with open(self.row_col_path,"w", encoding="utf-8") as f:
			json.dump(d, f)


	def order(self, event:wx.KeyEvent):
		if event.GetKeyCode()!=wx.WXK_F6: return
		self.puzzle.order()
		super().show_message("顺序已经调整好。" +self.puzzle.get_focus_block_message())


	def disorder(self,event:wx.KeyEvent):
		if event.GetKeyCode()!=wx.WXK_F5: return
		self.puzzle.disorder()
		super().show_message("顺序已经打乱。" +self.puzzle.get_focus_block_message())

		
	def move_puzzle_block(self, event:wx.KeyEvent):
		"""移动拼图方块"""
		# 需要按下ctrl
		if not event.ControlDown(): return
		moved=False
		key_code=event.GetKeyCode()
		if key_code==wx.WXK_LEFT: moved=self.puzzle.move_to_left()
		elif key_code==wx.WXK_UP: moved =self.puzzle.move_to_up()
		elif key_code==wx.WXK_RIGHT: moved=self.puzzle.move_to_right()
		elif key_code==wx.WXK_DOWN: moved=self.puzzle.move_to_down()
		else: return

		if not moved: Beep(220, 400)
		else: self.show_focus_block_message()

		if self.puzzle.check_successful():
			super().show_message("恭喜你！拼图完成了！按F5可以打乱 顺序重新开始。")
			playsound(r"sounds/congratulation/congratulation.wav")


	def view_puzzle_block(self, event:wx.KeyEvent):
		"""查看拼图方块"""
		# 不按下ctrl
		if event.ControlDown(): return
		key_code=event.GetKeyCode()
		block=None
		if key_code==wx.WXK_LEFT:block=self.puzzle.view_left()
		elif key_code==wx.WXK_UP:block=self.puzzle.view_up()
		elif key_code==wx.WXK_RIGHT: block=self.puzzle.view_right()
		elif key_code==wx.WXK_DOWN:block=self.puzzle.view_down()
		else: return
		
		if not block:
			Beep(440, 50)
			# block=self.puzzle.get_focus_block()
			return
		self.show_focus_block_message()


	def show_focus_block_message(self):
		"""显示焦点方块信息"""
		message=self.puzzle.get_focus_block_message()
		super().show_message(message)


app=wx.App(False)
PuzzleWindow()
app.MainLoop()