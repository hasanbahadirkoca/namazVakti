import os,sys
import time
import urllib.request
import json
import requests
from datetime import datetime, timedelta
import subprocess



data_file_path = 'data.json'

# Tarih ve Saat bilgisini güncelleme fonksiyonu
def zamanGuncelle():
  global date, now, xtime#, realtime
  #x = datetime.now()
  xtime = datetime.now() #+ timedelta(hours=3)
  date  = xtime.strftime("%d.%m.%Y")
  #realtime  = x.strftime("%H:%M")
  now = datetime.today()
   


def readTimes():
  #print("> Sabah vakti aliniyor...")

  with urllib.request.urlopen("https://api.thehbk.com/output") as url:
    data = json.loads(url.read().decode())

  for i in data:
      if i ['vakitAdi'] == "sabahNamazi":
          #print("> Sabah vakti alindi. > " + i['vakit'])
          return i['vakit']
          break

# Dosya indirme fonksiyonu
def downloadDataFile():
  global data_file_path

  print("> ---- Vakit dosyasi indiriliyor...")

  url = 'https://ezanvakti.herokuapp.com/vakitler/9541'
  headers = {'Accept': 'application/json'}
  response = requests.get(url, headers=headers)

  with open(data_file_path, 'wb') as outf:
      outf.write(response.content)
      print("> ---- Vakit dosyasi indirildi.")


# Vakit dosyasini okuma fonksiyonu
def readDataFile():
    global data, admin_data, data_file_path, admin_data_path
    data_file = open(data_file_path)
    #admin_data_path = open('admin_data.json')
    data = json.load(data_file)
    #admin_data = json.load(admin_data_path)
    print("> ---- Vakit dosyasi acildi.")


# Dosya doğruluğunu kontrol etme fonksiyonu
def dataFileControl():
  global data_file_path

  zamanGuncelle()
  if os.path.exists(data_file_path):
      print("> ---- Vakit dosyasi mevcut.")

      readDataFile()
      jsonControl = False
      for i in data:
          if i ['MiladiTarihKisa'] == date:
              print("> ---- Vakit dosyasi dogru.")
              jsonControl = True
              break
      if jsonControl == False:
          print("> ---- Vakit dosyasi hatali!")
          os.remove("data.json")
          print("> ---- Vakit dosyasi silindi.")
          downloadDataFile()
          dataFileControl()
  else:
      print("> ---- Vakit dosyasi mevcut degil!")
      downloadDataFile()
      dataFileControl()

# Gunluk vakit ogren.
def gunlukVakitAl():
  readDataFile()
  zamanGuncelle()
  global imsakVakti, sabahVakti, gunesVakti, ogleVakti, ikindiVakti, aksamVakti, yatsiVakti, gun, ramazanAyi

  for i in data:
    if i['MiladiTarihKisa'] == date:
        imsakVakti  = datetime.strptime(str(date + " " + i['Imsak']),  '%d.%m.%Y %H:%M')
        try:
          sabahVakti  = datetime.strptime(str(date + " " + readTimes()),  '%d.%m.%Y %H:%M')
        except:
          print("sabah vakti hata")
        gunesVakti  = datetime.strptime(str(date + " " + i['Gunes']),  '%d.%m.%Y %H:%M')
        ogleVakti   = datetime.strptime(str(date + " " + i['Ogle']),   '%d.%m.%Y %H:%M')
        ikindiVakti = datetime.strptime(str(date + " " + i['Ikindi']), '%d.%m.%Y %H:%M')
        aksamVakti  = datetime.strptime(str(date + " " + i['Aksam']),  '%d.%m.%Y %H:%M')
        yatsiVakti  = datetime.strptime(str(date + " " + i['Yatsi']),  '%d.%m.%Y %H:%M')

        gun = (i['MiladiTarihUzun'].split())[3]

        if( (i['HicriTarihKisa'].split('.'))[1] == "9" ):
          # Eğer ramazan ayı ise:
          print(i['HicriTarihKisa'])
          ramazanAyi = True
        else:
          ramazanAyi = False

        break




# Sistem Başlangıcı
print("> Dosya kontrolu basladi...\n> -- Vakit dosyasi kontrolu basladi...")
dataFileControl()
print("> -- Dosya kontrolu tamamlandi.")


# Başlangıç mesajı
print("\n----------------\nSistem basladi.\n"+ str(xtime.strftime("%d.%m.%Y %H.%M.%S")) +"\n----------------\n")
gunlukVakitAl()
print(  "Sabah Vakti:  " + str(sabahVakti)  +
      "\nOgle Vakti:   " + str(ogleVakti)   +
      "\nIkindi Vakti: " + str(ikindiVakti) +
      "\nAksam Vakti:  " + str(aksamVakti)  +
      "\nYatsi Vakti:  " + str(yatsiVakti)  +
      "\nGun:          " + gun              )

def vakte_kalan():
  global imsakVakti, sabahVakti, gunesVakti, ogleVakti, ikindiVakti, aksamVakti, yatsiVakti, now, xtime, onumuzdekiVakitAdi, onumuzdekiVakit
  zamanGuncelle()

  onumuzdekiVakitAdi = "vakitGuncelleme"
  onumuzdekiVakit    = xtime
  """
  if imsakVakti > xtime:
    onumuzdekiVakitAdi = "Imsak"
    onumuzdekiVakit    = imsakVakti
  el"""
  """
  elif gunesVakti > xtime:
    onumuzdekiVakitAdi = "Güneş"
    onumuzdekiVakit    = gunesVakti
  """

  if sabahVakti > xtime:
    if ramazanAyi == True:
      #Ramazan'da İmsak vaktine göre sabah ezanı okunmasını sağlar.
      onumuzdekiVakitAdi = "Sahur"
      onumuzdekiVakit    = imsakVakti
    else:
      onumuzdekiVakitAdi = "Sabah"
      onumuzdekiVakit    = sabahVakti
  elif ogleVakti > xtime:
    onumuzdekiVakitAdi = "Ogle"
    onumuzdekiVakit    = ogleVakti
  elif ikindiVakti > xtime:
    onumuzdekiVakitAdi = "Ikindi"
    onumuzdekiVakit    = ikindiVakti
  elif aksamVakti > xtime:
    onumuzdekiVakitAdi = "Aksam"
    onumuzdekiVakit    = aksamVakti
  elif yatsiVakti > xtime:
    onumuzdekiVakitAdi = "Yatsi"
    onumuzdekiVakit    = yatsiVakti
    

  msg = onumuzdekiVakit - xtime

  return msg



while True:
  global onumuzdekiVakitAdi, onumuzdekiVakit
  vakteKalan = vakte_kalan()
  #print(vakteKalan)

  if vakteKalan == timedelta(hours = 0, minutes = 0, seconds = 0):
    gunlukVakitAl()
    print("Vakit bekleniyor...")
    time.sleep(7200)
  elif vakteKalan <= timedelta(hours = 1, minutes = 0, seconds = 0) and vakteKalan >= timedelta(hours = 0, minutes = 59, seconds = 55):
      if(ramazanAyi == True and onumuzdekiVakitAdi == "Sahur"):
        # Eğer ramazan ayı ise:
        print("Sahur selasi okunuyor.")
        subprocess.call(['amixer -q sset Speaker 40%'], shell=True)
        subprocess.call(['mpg123 -q -v ezanSesleri/sahurSelasi.mp3'], shell=True)
      elif gun == "Cuma" and onumuzdekiVakitAdi == "Ogle":
        print("Cuma selasi okunuyor.")
        subprocess.call(['amixer -q sset Speaker 70%'], shell=True)
        subprocess.call(['mpg123 -q -v ezanSesleri/cumaSelasi.mp3'], shell=True)
        subprocess.call(['mpg123 -q -v ezanSesleri/cumaSelasi.mp3'], shell=True)
      else:
        print(onumuzdekiVakitAdi + " ezanina bir saat kaldi.")
  elif vakteKalan <= timedelta(hours = 0, minutes = 0, seconds = 1) and vakteKalan >= timedelta(hours = 0, minutes = 0, seconds = 0):
    print(onumuzdekiVakitAdi + " Vakti > " + str(onumuzdekiVakit) + " geldi.")
    if(onumuzdekiVakitAdi == "Sabah" or onumuzdekiVakitAdi == "Sahur"):
        print("Sabah ezani okunuyor.")
        subprocess.call(['amixer -q sset Speaker 40%'], shell=True)
        subprocess.call(['mpg123 -q -v ezanSesleri/sabahEzani.mp3'], shell=True)
    elif(onumuzdekiVakitAdi == "Ogle"):
        print("Ogle ezani okunuyor.")
        subprocess.call(['amixer -q sset Speaker 80%'], shell=True)
        subprocess.call(['mpg123 -q -v ezanSesleri/ogleEzani.mp3'], shell=True)
    elif(onumuzdekiVakitAdi == "Ikindi"):
        print("Ikindi ezani okunuyor.")
        subprocess.call(['amixer -q sset Speaker 80%'], shell=True)
        subprocess.call(['mpg123 -q -v ezanSesleri/ikindiEzani.mp3'], shell=True)
    elif(onumuzdekiVakitAdi == "Aksam"):
        print("Aksam ezani okunuyor.")
        subprocess.call(['amixer -q sset Speaker 80%'], shell=True)
        subprocess.call(['mpg123 -q -v ezanSesleri/aksamEzani.mp3'], shell=True)
    elif(onumuzdekiVakitAdi == "Yatsi"):
        print("Yatsi ezani okunuyor.")
        subprocess.call(['amixer -q sset Speaker 80%'], shell=True)
        subprocess.call(['mpg123 -q -v ezanSesleri/yatsiEzani.mp3'], shell=True)

  
  #print(onumuzdekiVakitAdi + " Vakti(" + str(onumuzdekiVakit) + ") > " + str(vakteKalan))
  #time.sleep(2)
