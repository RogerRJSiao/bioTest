import re #字串處理 #序列判讀
# from urllib.request import urlopen
from google.colab import files

#檢視DNA序列，取出合乎codon序列
def reviewDNA(seq):
  seqType = 'DNA'
  ori_seq = seq
  seq = seq.upper().replace("U","T") #U變更為T
  arr_seq_success = [] #定序合乎3nts且有起始、終止condon
  arr_seq_error = [] #定序不合乎3nts或無起始、終止condon
  arr_pos_start = []
  pos_start_last = -1

  #確認轉譯起始、終止位置
  while seq.find('ATG') != -1:
    #轉譯起始位置
    pos_start = seq.find('ATG') 
    new_seq = seq[pos_start:] #從ATG開始取序列
    temp_seq = new_seq #用來處理轉譯終止
    # print(temp_seq)

    #轉譯終止位置
    pos_stopX = temp_seq.find('TAG')
    pos_stopY = temp_seq.find('TAA')
    pos_stopZ = temp_seq.find('TGA')
    pos_stopXYZ = [pos_stopX, pos_stopY, pos_stopZ]
    # print(pos_stopXYZ)
    pos_stop = list(filter(lambda a: a >= 0 and a % 3 == 0, pos_stopXYZ)) #篩選非-1且位值是3的倍數 #filter結果需有list() #lambda
    if not pos_stop:
      pos_stop = len(temp_seq) #序列原本長度
    else:
      pos_stop = min(pos_stop) #最小值

    pos_start_last = pos_start_last + pos_start + 1
    print(pos_start_last)
    #存取序列判讀資訊
    if pos_stop % 3 == 0 and pos_stopXYZ != [-1,-1,-1]:
      temp_seq = temp_seq[0:pos_stop+3].lower()
      print(f'DNA 修整後(成功，序列第 {pos_start_last} 位)： ',temp_seq)
      arr_seq_success.append([temp_seq, len(temp_seq), seqType])
      arr_pos_start.append(pos_start_last)
    else:
      temp_seq = temp_seq.lower()
      print(f'DNA 修整後(失敗，序列第 {pos_start_last} 位)： ',temp_seq)
      arr_seq_error.append([temp_seq, len(temp_seq), seqType])

    #整理序列
    seq = new_seq[1:] #剪除第一個nt，再次搜尋下一個ATG
    # print()

  print('reviewDNA success:', arr_seq_success)
  print('reviewDNA error:', arr_seq_error)
  print('reviewDNA start_pos:',arr_pos_start)

  return arr_seq_success, arr_seq_error, arr_pos_start


#DNA 轉錄成 mRNA [arr, 批次]
def DNA2mRNA(arr_seq):
  temp_arr_seq = arr_seq
  arr_seq_success = []
  arr_seq_error = []

  for seq in temp_arr_seq:
    seqContent, seqLen, seqType = seq[0].strip().upper(), seq[1], seq[2]
    if seqLen % 3 == 0 and seqContent.find('ATG') == 0 and seqType.lower() == 'dna':
      #轉譯
      seqContent = seqContent.replace("T","U").lower()
      arr_seq_success.append([seqContent, len(seqContent), 'mRNA']) #成功
    else:
      seq = seq.lower()
      arr_seq_error.append(seq)
  
  print('DNA2mRNA success:', arr_seq_success) #成功
  print('DNA2mRNA error:', arr_seq_error) #失敗

  return arr_seq_success, arr_seq_error


#mRNA 反轉錄成 DNA [arr, 批次]
def mRNA2cDNA(arr_seq):
  temp_arr_seq = arr_seq.upper()
  arr_seq_success = []
  arr_seq_error = []

  for seq in temp_arr_seq:
    seqContent, seqLen, seqType = seq[0].strip(), seq[1], seq[2]
    if seqLen % 3 == 0 and seqContent.find('AUG') == 0 and seqType.lower() == 'mrna':
      #反轉譯
      cDNA = ''
      seqContent = list(seqContent)
      while len(seqContent) > 0:
        last_nt = seqContent.pop() #從[]取出最後一個值
        match last_nt:
          case 'A':
            cDNA += 'T'
          case 'U':
            cDNA += 'A'
          case 'C':
            cDNA += 'G'
          case 'G':
            cDNA += 'C'
          case _:
            cDNA += '_'
      cDNA = cDNA.lower()
      arr_seq_success.append([cDNA, len(cDNA), 'cDNA']) #成功
    else:
      seq = seq.lower()
      arr_seq_error.append(seq) #失敗

  print('mRNA2cDNA success:', arr_seq_success) #成功
  print('mRNA2cDNA error:', arr_seq_error) #失敗

  return arr_seq_success, arr_seq_error


#DNA 轉譯成 protein [arr, 批次]
def DNA2protein(arr_seq):
  temp_arr_seq = arr_seq.upper()
  arr_seq_success = []
  arr_seq_error = []

  #建立字典
  codon_table = {
      'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
      'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
      'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
      'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',                 
      'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
      'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
      'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
      'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
      'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
      'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
      'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
      'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
      'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
      'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
      'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_',
      'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W',
  }

  for seq in temp_arr_seq:
    seqContent, seqLen, seqType = seq[0].strip(), seq[1], seq[2]
    # seqContent = seqContent.replace("U","T")
    if seqLen % 3 == 0 and seqContent.find('ATG') == 0 and seqType.lower() in ['dna', 'cdna']:
      #轉錄
      protein = ""
      for i in range(0, len(seqContent), 3):
        codon = seqContent[i:i + 3]
        protein += codon_table[codon]
      arr_seq_success.append([protein, len(protein)-1, 'protein']) #成功
    else:
      arr_seq_error.append(seq) #失敗
  
  print('DNA2protein success:', arr_seq_success) #成功
  print('DNA2protein error:', arr_seq_error) #失敗

  return arr_seq_success, arr_seq_error

#匯出DNA轉錄、轉譯資料
def transcript_translate(arr_seq):
  arr_dna_success, arr_cdna_success, arr_mrna_success, arr_protein_success = [], [], [], []
  arr_dna_success, arr_dna_err, arr_pos_start = reviewDNA(arr_seq)
  if len(arr_pos_start) > 0:
    arr_mrna_success, arr_mrna_err = DNA2mRNA(arr_dna_success)
    arr_cdna_success, arr_cdna_err = mRNA2cDNA(arr_mrna_success)
    arr_protein_success, arr_protein_err = DNA2protein(arr_dna_success)

  #寫入txt檔案
  f = open("myResult.txt","w+")
  #原始序列
  f.write("讀取序列\r\n\r\n%s\r\n" % (arr_seq))
  #Coding 序列
  if len(arr_pos_start) > 0:
    #標示Coding用的AUG起始
    x_last = -1
    for x in arr_pos_start:
      if x == arr_pos_start[0]:
        f.write("%s" % (" " * x + "^^^"))  #標示^^^在ATG下方
      else:
        space = x - x_last - 3
        f.write("%s" % (" " * space + "^^^"))  #標示^^^在ATG下方
      x_last = x
    f.write("\r\n\r\n")
    #分段顯示Coding序列
    for i in range(len(arr_dna_success)):
      f.write("Coding 序列 %d\r\n" % (i + 1))
      f.write("    DNA seq: 5'-{0}-3' (nt = {1})\r\n" .format(arr_dna_success[i][0], arr_dna_success[i][1]))
      # f.write("   {0}{1}\r\n" .format(" " * 13, "|" * len(arr_dna_success[i][0])))
      f.write("   cDNA seq: 3'-{0}-5' \r\n" .format(arr_cdna_success[i][0][::-1])) #反序顯示
      f.write("   mRNA seq: 5'-{0}-3' (nt = {1})\r\n" .format(arr_mrna_success[i][0], arr_mrna_success[i][1]))
      f.write("   Protein seq: {0} (aa = {1})\r\n\r\n" .format(arr_protein_success[i][0], arr_protein_success[i][1]))
  else:
    f.write("這段序列可能為 non-coding DNA\r\n\r\n")

  f.write(" = = = 以下空白 = = = ")

  #下載txt檔案
  files.download("myResult.txt")

  return arr_dna_success, arr_cdna_success, arr_mrna_success, arr_protein_success