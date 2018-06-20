#encoding: utf-8
import sys
import os
from PySide.QtCore import *
from PySide.QtGui import *
import sqlite3
import time



class SimpleFileModel(QStringListModel):

	file_paths = []

	def __init__(self, root_dir_path):
		super(SimpleFileModel, self).__init__([])
		self.conn = sqlite3.connect(':memory:')
		self.conn.text_factory = str
		self.conn.row_factory = sqlite3.Row
		self.cur = self.conn.cursor()
		self.cur.execute(u'create table test (path)')
		self.update_data(root_dir_path)



	def flags(self, index):
		if not index.isValid():
			return Qt.NoItemFlags
		return Qt.ItemIsEnabled | Qt.ItemIsSelectable



	def build(self, values=[]):
		values = self.file_paths if not values else values
		for i in values:
			print i
		super(SimpleFileModel, self).setStringList(values)



	def update_data(self, root_dir_path):
		file_paths = []
		for dir_path, dir_names, file_names in os.walk(root_dir_path):
		    for file_name in file_names:
		    	file_path = os.path.join(dir_path, file_name)
		    	sql = u"insert into test values(?)"
		    	self.cur.execute(sql, (file_path.decode('cp932'),))
		    	file_paths.append(file_path)
		self.file_paths = file_paths



	def filter_data(self, cond):
		cond = u'where path {0}'.format(cond)
		sql = u'select * from test {0}'.format(cond)
		file_path_datas = self.cur.execute(sql)
		file_paths = [row['path'] for row in self.cur]
		self.file_paths = file_paths




if __name__ == '__main__':
	mdl = SimpleFileModel(r'D:\data\sql\db\python\ui')
	app = QApplication(sys.argv)
	item_view = QListView()
	item_view.setWindowTitle('simple explore')
	item_view.setModel(mdl)
	mdl.filter_data('like "%.txt"')
	mdl.build()
	item_view.show()
	app.exec_()
	mdl.cur.close()
	mdl.conn.close()
