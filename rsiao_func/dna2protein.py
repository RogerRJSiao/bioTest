# 生物序列種類判斷

# 生物序列轉換&顯示


#字串處理 #序列判讀
import re

def adjust_seq(seqType, str_seq):
  temp_seq = ''
  if seqType == 'DNA':
    #序列整理
    str_seq = str_seq.replace(" ","") #刪除空格
    str_seq = str_seq.replace("\r\n","") #刪除換行
    str_seq = str_seq.upper() #全變大寫
    temp_seq = str_seq

    #判斷有無UATGC以外雜訊
    if 'U' in temp_seq:
      temp_seq1 = temp_seq.replace("U","") #刪除U
      file_showMsg = '不是 DNA 序列，可能是 RNA 序列'
      #TODO:胺基酸序列
    else:
      temp_seq1 = temp_seq

    #判斷有無UATGC以外雜訊
    if 'A' in temp_seq or 'T' in temp_seq or 'C' in temp_seq or 'G' in temp_seq:
      temp_seq2 = temp_seq1.replace("A","") #刪除A
      temp_seq2 = temp_seq2.replace("T","") #刪除T
      temp_seq2 = temp_seq2.replace("C","") #刪除C
      temp_seq2 = temp_seq2.replace("G","") #刪除G
      temp_seq3 = temp_seq2
    else:
      temp_seq3 = temp_seq2

    global len_seq
    len_temp_seq3 = len(temp_seq3)
    len_seq = len(str_seq)
    if len_temp_seq3 != 0:
      str_seq = temp_seq
      file_showMsg = '不是 DNA 序列'
    elif len_temp_seq3 == 0 and len_seq % 3 == 0:
      str_seq = temp_seq
      file_showMsg = f'DNA 序列，有 {len_seq} 個鹼基。'
    else:
      str_seq = temp_seq
      file_showMsg = f'可能是 DNA 序列，但只有 {len_seq} 個鹼基。'

  else:
    str_seq = str_seq
    file_showMsg = '不是 DNA 序列'
  return str_seq, file_showMsg