import pandas as pd
import geopandas as gpd
import folium 
import shapely.geometry as shp
from folium import plugins
import streamlit as st
from streamlit_folium import folium_static
import numpy as np
from PIL import Image


## GeoData
ilceler=gpd.read_file("C:/Users/rebaa/Desktop/cbs/ank/ilceler.geojson")
ilceler.to_crs(epsg=4326,inplace=True)
#geodata ile data uyumluluğu için sütun ismi değiştirildi ve ilçeler büyük harfle yazdırıldı
ilceler.rename(columns = {'name':'İLÇE'}, inplace = True)
ilceler['İLÇE'] = ilceler['İLÇE'].str.upper()


## Data
data=pd.read_excel("C:/Users/rebaa/Desktop/cbs/ank/veriler/OTEL.xlsx")
data["geometry"]=data[["BOYLAM","ENLEM"]].apply(shp.Point,axis=1)
data=gpd.GeoDataFrame(data)
data=data.set_crs(epsg=4326,inplace=True)
data["İLÇE"]=data["İLÇE"].str.upper()
##görsel fonks
style_function = lambda x: {'fillColor': '#000000', 
                            #'color':'#000000', 
                            'fillOpacity':0.4,
                            'weight':0.5}

style_function1 = lambda x: {'fillColor': '#FFFFFF', 
                             'color':'#000000', 
                             'fillOpacity':0.5,
                             'weight':0.5}



highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
     

## Streamlit
st.set_page_config(page_title="ANKARA_OTELLER",page_icon=":smile:")
st.header("Ankar Oteller Projesi")
st.markdown("Çalışmada Ankara'nın ilçelerindeki Oteller interaktif harita  biçiminde gösterilmiştir. Harita gösterimi, yıldız sayısı ve İlçe adına göre filtrelenenebilmektedir. Sol taraftaki filtre barı ile sorgulama işlemlerinizi yapabilirsiniz.. ")
st.sidebar.header("FİLTRELER:")



ilce_list=["ÇANKAYA","YENIMAHALLE","ALTINDAĞ","GÖLBAŞI","AKYURT","AYAŞ","KIZILCAHAMAM","HAYMANA","ETIMESGUT","POLATLI","ALTINDAĞ","ULUS","ŞEREFLIKOÇHISAR","TÜMÜ"]

seçim=st.sidebar.selectbox(label = "İlçe Seçiniz", options = (ilce_list))
yıldız_sayısı=st.sidebar.selectbox(label="Yıldız Sayısını Seçiniz" , options=("Tümü",3,4,5,))


if yıldız_sayısı=="Tümü":
    Df=data[data["İLÇE"]==seçim]
else:
 Df=data[data["İLÇE"]==seçim]
 Df=Df[Df["YILDIZ"]==yıldız_sayısı]






## zoom MERKEZLERİ
konum_enlem=Df["ENLEM"].mean()
konum_boylam=Df["BOYLAM"].mean()
location=(konum_enlem,konum_boylam)

    
## zoom sayısı
if seçim=="ÇANKAYA":
 zs=12
elif (seçim=="ALTINDAĞ"):
 zs=13
else:
 zs=10

 ## Eğer seçim kümesi boşsa;
if pd.notna(location[0])==False:
 st.error("İstediğiniz kriterlerde otel bulunamamıştır. Lütfen Filtreleri değiştiriniz..") 
 st.stop()



else:
## Map
 map=folium.Map(zoom_start=zs,location=location,tiles="Stamen Terrain" )
 folium.features.GeoJson(
    ilceler, 
    style_function=style_function1).add_to(map)
  
 ##SEÇİLEN İLÇEYE VURGU
 NIL = folium.features.GeoJson(
    ilceler[ilceler["İLÇE"]==seçim], 
    style_function=style_function, 
    #control=False,
    #highlight_function=highlight_function, 
    #tooltip=folium.features.GeoJsonTooltip(
        #fields=['İLÇE'],
        #aliases=['İlçe:'],
        #style=('background-color: grey; color: white;')      
    )
#)
NIL.add_to(map)
 ##TÜMÜNE  VURGU






## otel popuplarının oluşturulması
for i in range(len(Df)):
 adres=Df["ADRES"].iloc[i]
 adı=Df["ADI"].iloc[i]
 folium.Marker([Df["ENLEM"].iloc[i],Df["BOYLAM"].iloc[i]],
               popup=adres,
               tooltip=adı,
              icon=folium.Icon(icon="building",prefix="fa",color="red")).add_to(map)
##konum ekleme
konum=plugins.LocateControl(setView=True,enableHighAccuracy=True,auto_start=False).add_to(map)  
##label1

if yıldız_sayısı=="Tümü":
    st.info("Şuanda "+ str(seçim) + " İlçesindeki " + " tüm otelleri görmektesiniz.")
else:
 st.info("Şuanda "+ str(seçim) + " İlçesindeki " + str(yıldız_sayısı) + " yıldızlı otelleri görmektesiniz.")

image = Image.open("C:/Users/rebaa/Desktop/cbs/ank/veriler/seffaf.png")
st.sidebar.image(image)

folium_static(map)
ilceler
st.info("Bu projede kullanılan veriler Şeffaf Ankara platformundan temin edilmiştir.")