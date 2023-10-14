#安裝UI小工具模組
#!pip install ipywidgets
#https://ipywidgets.readthedocs.io/en/latest/index.html

#導入UI小工具模組
import ipywidgets as widgets #導入元件
from IPython.display import display #顯示元件

#選擇物種類別
dd1 = widgets.Dropdown(
    # options=[('請選擇', 0), ('動物 (推薦)', 10), ('植物', 20), ('真菌', 30), ('細菌', 40), ('病毒', 50)],
    options=[('請選擇', 0), ('動物 (推薦)', 10), ('病毒', 50), ],
    value=0,
    description='物種類別 ',
)
#選擇序列種類
dd2 = widgets.Dropdown(
    # options=[('請選擇', 0), ('RNA', 10), ('DNA (推薦)', 20), ('mRNA', 30), ('Proteins', 40), ('Glycans', 50), ('Lipids', 60)],
    options=[('請選擇', 0), ('DNA (推薦)', 20), ('mRNA', 30), ('Proteins', 40),],
    value=0,
    description='序列種類',
)
#確認取值按鈕
btn1 = widgets.Button(description="確 認", button_style='success')

def btn1_click(b):
  global species_type, sequence_type
  species_type = type_to_name('species', dd1.value)
  sequence_type = type_to_name('sequence', dd2.value)
  output.value = f"您目前點選 {species_type} 和 {sequence_type} 。"
  print(output.value)
  if dd1.value == 10 and dd2.value >=20 and dd2.value <= 30:
    print(f"成功選取 {species_type} (代號：{dd1.value}) 和 {sequence_type} (代號：{dd2.value})！\n")
    return species_type, sequence_type
  else:
    print(f"請重新選取！目前不支援 {species_type} 與 {sequence_type} 組合。\n")
    showDropdown1()

def type_to_name(sort, code):
  if sort == 'species':
    match code:
      case 10: name = '動物'
      case 20: name = '植物'
      case 30: name = '真菌'
      case 40: name = '細菌'
      case 50: name = '病毒'
      case _: name = '(未選)'
  elif sort == 'sequence':
    match code:
      case 10: name = 'RNA'
      case 20: name = 'DNA'
      case 30: name = 'mRNA'
      case 40: name = 'Proteins'
      case 50: name = 'Glycans'
      case 60: name = 'Lipids'
      case _: name = '(未選)'
  return name

#按鈕監聽取值
btn1.on_click(btn1_click)

output = widgets.Output()

def showDropdown1():
  print('\n請先選擇物種類別、序列種類\n')
  display(dd1, dd2)
  print()
  display(btn1)
  print()
  display(output)

def showTextarea1(show_seq):
  #顯示輸入原始序列 
  textarea1 = widgets.Textarea(
      value = show_seq,
      placeholder = '(您的檔案沒有序列資料)',
      description = '已上傳序列：',
      disabled = True
  )
  print('\n請確認檔案上傳的序列\n')
  display(textarea1)
  print()





# 生物序列種類判斷
def check_seqType(speCode, seqCode, str_seq):
  temp_seq, temp_seq1, temp_seq2, temp_seq3 = '', '', '', ''

  if speCode == 10 and (seqCode == 20 or seqCode == 30): #【動物+DNA】或【動物+mRNA】
    #序列整理
    str_seq = str_seq.replace(" ","") #刪除空格
    str_seq = str_seq.replace("\r\n","") #刪除換行
    str_seq = str_seq.upper() #全變大寫
    temp_seq = str_seq

    #判斷是否只有ATCG【DNA】
    temp_seq1 = temp_seq.replace("A","") #刪除A
    temp_seq1 = temp_seq1.replace("T","") #刪除T
    temp_seq1 = temp_seq1.replace("C","") #刪除C
    temp_seq1 = temp_seq1.replace("G","") #刪除G
    print('temp_seq1',len(temp_seq1))
    if len(temp_seq1) == 0:
      str_seq = temp_seq
      file_showMsg = '這段序列應該是 DNA'
      print('這段序列應該是 DNA')

    else:
      #判斷是否只有AUCG【RNA】
      temp_seq2 = temp_seq.replace("A","") #刪除A
      temp_seq2 = temp_seq2.replace("U","") #刪除U
      temp_seq2 = temp_seq2.replace("C","") #刪除C
      temp_seq2 = temp_seq2.replace("G","") #刪除G
      print('temp_seq2',len(temp_seq2))
      if len(temp_seq2) == 0:
        str_seq = temp_seq
        file_showMsg = '這段序列應該是 RNA'
        print('這段序列應該是 RNA')

      else:
        str_seq = str_seq
        file_showMsg = '這段序列既不是 DNA，也不是 RNA'
        print('這段序列既不是 DNA，也不是 RNA')

  else:
    str_seq = str_seq
    file_showMsg = "請重新選取【動物+DNA】或【動物+mRNA】任一組合！"

  return str_seq, file_showMsg