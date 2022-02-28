import datetime
import os
import shutil

"""
Сохранение данных в архив
"""
def main_save_archive(version_mk):
	# if check_click("Сохранить все данные в архив и удалить файлы в текущих папках?"):
		now = datetime.datetime.now()
		form_path = str(now.day) + "_" + str(now.month) + "_" + str(now.year)
		try:
			os.mkdir("../archive/" + str(version_mk) + "/" + form_path)
		except:
			print ("Создать директорию не удалось " + str(os.getcwd()))
		path_data_archive = "../archive/" + str(version_mk) + "/" + form_path + "/data/"
		path_address_archive = "../archive/" + str(version_mk) + "/" + form_path + "/microchip_life/"
		path_finaly_test_archive = "../archive/" + str(version_mk) + "/" + form_path + "/logger/"
		try:
			os.mkdir(path_data_archive)
			os.mkdir(path_address_archive)
			os.mkdir(path_finaly_test_archive)
		except:
			print("Создать директорию не удалось")

		list_file_data = os.listdir("../data/")
		for i in list_file_data:
			shutil.copyfile("../data/" + i, path_data_archive + i)
			os.remove("../data/" + i)
		list_file_finaly_test = os.listdir("../logger/")
		for i in list_file_finaly_test:
			shutil.copyfile("../logger/" + i, path_finaly_test_archive + i)
			os.remove("../logger/" + i)
		list_file_data = os.listdir("../microchip_life/")
		for i in list_file_data:
			shutil.copyfile("../microchip_life/" + i, path_address_archive + i)
			os.remove("../microchip_life/" + i)