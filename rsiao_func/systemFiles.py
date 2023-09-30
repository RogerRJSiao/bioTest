#管理檔案、資料夾
import os
import shutil

# 在執行 py 檔案時，需要注意以下兩點
# 1. py 檔案需要放在 Colab Notebook 之下
# 2. 執行前 %cd /content/drive/MyDrive/Colab Notebooks

#在Colab Notebooks建立存取資料夾
def mk_folders_in_Colab():
    folderpath = "/content/drive/MyDrive/Colab Notebooks"
    for dirname in [ 'rsiao_rawData', 'rsiao_resultData']:
        try:
            os.makedirs(folderpath + '/' + dirname) #建立資料夾
            print(f"成功！{dirname} 已建立。", )
        except FileExistsError:
            print(f"注意！{dirname} 已存在。", ) #資料夾已存在

#計算當前dir內py檔案數量
def detect_pyFiles():
    py_files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.py')] 
    print('目前偵測到', len(py_files), '個 py 檔案')
    return py_files

#轉移複製檔案，import py 必在 Colab Notebook 之下，請勿隨意更動
def cp_files_to_Colab():
    cnt = 0
    py_files = detect_pyFiles()
    for py_file in py_files:
        src = "/content/rsiao_bioTest/rsiao_func/" + py_file
        filename = "rsiao_" + py_file
        dest1 = "/content/rsiao_bioTest/rsiao_func/" + filename
        dest2 = "/content/drive/MyDrive/Colab Notebooks/" + filename
        shutil.copy(src, dest1) #複製
        shutil.move(dest1, dest2) #轉移
        cnt += 1
        print(f"完成第 {cnt} 個檔案移轉，新檔名：{filename}")