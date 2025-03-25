import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

# Streamlit app başlığı
st.title("ODTÜ Yayın ve Proje Başvuru Planları Analizi")

# Unvan sıralaması (en az nitelikliden en çok nitelikliye)
title_order = ["Arş. Gör.", "Öğr. Gör.", "Dr. Öğr. Üyesi", "Doç. Dr.", "Prof. Dr.", "Diğer"]

# İçindekiler tablosu için başlıklar ve ID'ler
toc_items = [
    ("Veri Dosyası Yükleme", "veri-dosyasi-yukleme"),
    ("Veri Hataları Nedeniyle Kaldırılan Araştırmacılar", "veri-hatalari"),
    ("Veri Özeti", "veri-ozeti"),
    ("Bölüm Bazında Proje/Yayın Dağılımı", "bolum-bazinda-dagilim"),
    ("Birim Bazında Proje/Yayın Dağılımı", "birim-bazinda-dagilim"),
    ("Bölüm ve Unvan Bazında Başvuru Sayısı (Balon Grafiği)", "bolum-unvan-balon"),
    ("Birim ve Unvan Bazında Başvuru Sayısı (Balon Grafiği)", "birim-unvan-balon"),
    ("Bölüm ve Unvan Bazında Dağılım (Isı Haritası)", "bolum-unvan-isi"),
    ("Birim ve Unvan Bazında Dağılım (Isı Haritası)", "birim-unvan-isi"),
    ("Bölüm ve Unvan Bazında Başvuru Sayısı (Etkileşimli Çubuk Grafiği)", "bolum-unvan-cubuk"),
    ("Birim ve Unvan Bazında Başvuru Sayısı (Etkileşimli Çubuk Grafiği)", "birim-unvan-cubuk"),
    ("Yıl Bazında Yayın Türü Dağılımı", "yil-bazinda-yayin"),
    ("Bölüm Bazında Proje Türü Dağılımı", "bolum-proje-turu"),
    ("Birim Bazında Proje Türü Dağılımı", "birim-proje-turu"),
    ("Bölüm Bazında Araştırmacı Verimliliği", "bolum-verimlilik"),
    ("Birim Bazında Araştırmacı Verimliliği", "birim-verimlilik"),
    ("Bölüm Bazında Zaman İçindeki Planlanan Çıktılar", "bolum-zaman"),
    ("Birim Bazında Zaman İçindeki Planlanan Çıktılar", "birim-zaman"),
    ("Bölüm Bazında Yayın Kalitesi ve Proje Katılımı", "bolum-yayin-kalitesi"),
    ("Birim Bazında Yayın Kalitesi ve Proje Katılımı", "birim-yayin-kalitesi"),
    ("Birim Bazında AB Projesi Dağılımı", "birim-ab-projesi"),
    ("Yıl Bazında Yayın Kalitesi Dağılımı", "yil-yayin-kalitesi"),
    ("Toplam Yayın Sayısına Göre İlk 5 Bölüm", "top-5-bolum"),
    ("Toplam Yayın Sayısına Göre İlk 5 Birim", "top-5-birim"),
    ("Zaman İçindeki Proje Türü Dağılımı", "zaman-proje-turu"),
    ("Birim Bazında AB Projeleri ve Ulusal Projeler", "birim-ab-ulusal"),
    ("Bölüm Bazında AB Projeleri ve Ulusal Projeler", "bolum-ab-ulusal"),
    ("Birim Bazında Yayın Çeyreklik Dağılımı", "birim-yayin-ceyreklik"),
    ("Toplam Sayıya Göre En İyi Proje Türleri", "en-iyi-proje-turleri"),
    ("Birim Bazında Yüksek Etkili (Q1+Q2) Yayınlar Zaman İçinde", "birim-yuksek-etki"),
    ("Bölüm Bazında Yüksek Etkili (Q1+Q2) Yayınlar Zaman İçinde", "bolum-yuksek-etki"),
    ("Proje Finansman Kaynağı Dağılımı", "proje-finansman"),
    ("Birim Bazında Yayın ve Proje Dengesi", "birim-yayin-proje-dengesi"),
    ("Bölüm Bazında Yayın ve Proje Dengesi", "bolum-yayin-proje-dengesi"),
]

# Sidebar'da İçindekiler Tablosu oluştur
with st.sidebar:
    st.header("İçindekiler")
    for title, anchor in toc_items:
        st.markdown(f'<a href="#{anchor}" style="text-decoration: none; color: #1f77b4;">{title}</a>', unsafe_allow_html=True)

# Define custom order for faculties and departments
FACULTY_ORDER = [
    "Mimarlık Fakültesi",
    "Fen Edebiyat Fakültesi",
    "İktisadi ve İdari Bilimler Fakültesi",
    "Eğitim Fakültesi",
    "Mühendislik Fakültesi",
    "Enstitüler",
    "Meslek Yüksekokulu",
    "Yabancı Diller Yüksekokulu",
    "Rektörlük",
    "ODTÜ Kuzey Kıbrıs Kampusu",
    "ODTÜ-SUNY Uluslararası Ortak Lisans Programları"
]

DEPARTMENT_ORDER = [
    # Mimarlık Fakültesi
    "Mimarlık Bölümü",
    "Şehir ve Bölge Planlama Bölümü",
    "Endüstriyel Tasarım Bölümü",
    # Fen Edebiyat Fakültesi
    "Biyolojik Bilimler Bölümü",
    "Kimya Bölümü",
    "Tarih Bölümü",
    "Matematik Bölümü",
    "Felsefe Bölümü",
    "Fizik Bölümü",
    "Psikoloji Bölümü",
    "Sosyoloji Bölümü",
    "İstatistik Bölümü",
    # İktisadi ve İdari Bilimler Fakültesi
    "İşletme Bölümü",
    "İktisat Bölümü",
    "Uluslararası İlişkiler Bölümü",
    "Siyaset Bilimi ve Kamu Yönetimi Bölümü",
    # Eğitim Fakültesi
    "Bilgisayar ve Öğretim Teknolojileri Eğitimi Bölümü",
    "Eğitim Bilimleri Bölümü",
    "Temel Eğitim Bölümü",
    "Yabancı Diller Eğitimi Bölümü",
    "Beden Eğitimi ve Spor Bölümü",
    "Matematik ve Fen Bilimleri Eğitimi Bölümü",
    # Mühendislik Fakültesi
    "Havacılık ve Uzay Mühendisliği Bölümü",
    "Kimya Mühendisliği Bölümü",
    "İnşaat Mühendisliği Bölümü",
    "Bilgisayar Mühendisliği Bölümü",
    "Elektrik ve Elektronik Mühendisliği Bölümü",
    "Mühendislik Bilimleri Bölümü",
    "Çevre Mühendisliği Bölümü",
    "Gıda Mühendisliği Bölümü",
    "Jeoloji Mühendisliği Bölümü",
    "Endüstri Mühendisliği Bölümü",
    "Makina Mühendisliği Bölümü",
    "Metalurji ve Malzeme Mühendisliği Bölümü",
    "Maden Mühendisliği Bölümü",
    "Petrol ve Doğal Gaz Mühendisliği Bölümü",
    # Enstitüler
    "Uygulamalı Matematik Enstitüsü",
    "Enformatik Enstitüsü",
    "Deniz Bilimleri Enstitüsü",
    "Fen Bilimleri Enstitüsü",
    "Sosyal Bilimler Enstitüsü",
    # Meslek Yüksekokulu
    "Elektrik Programı",
    "Elektronik Teknolojisi Programı",
    "Endüstriyel Elektronik Programı",
    "Endüstriyel Otomasyon Programı",
    "Gıda Teknolojisi Programı",
    "Kaynak Teknolojisi Programı",
    "Teknik Programlar Bölümü",
    # Yabancı Diller Yüksekokulu
    "Temel İngilizce Birimi",
    "Modern Diller Birimi",
    "Yabancı Diller Bölümü",
    "Akademik Yazı Merkezi",
    # Rektörlüğe Bağlı Bölümler
    "Türk Dili Bölümü",
    "Müzik ve Güzel Sanatlar Bölümü"
]

# Official METU Faculty and Department Mapping
FACULTY_MAPPING = {
    "Mimarlık Fakültesi": "Mimarlık Fakültesi",
    "Faculty of Architecture": "Mimarlık Fakültesi",
    "Fen Edebiyat Fakültesi": "Fen Edebiyat Fakültesi",
    "Faculty of Arts and Sciences": "Fen Edebiyat Fakültesi",
    "İktisadi ve İdari Bilimler Fakültesi": "İktisadi ve İdari Bilimler Fakültesi",
    "Faculty of Economic and Administrative Sciences": "İktisadi ve İdari Bilimler Fakültesi",
    "Eğitim Fakültesi": "Eğitim Fakültesi",
    "Faculty of Education": "Eğitim Fakültesi",
    "Mühendislik Fakültesi": "Mühendislik Fakültesi",
    "Faculty of Engineering": "Mühendislik Fakültesi",
    "Enstitüler": "Enstitüler",
    "Uygulamalı Matematik Enstitüsü": "Uygulamalı Matematik Enstitüsü",
    "Institute of Applied Mathematics": "Uygulamalı Matematik Enstitüsü",
    "Enformatik Enstitüsü": "Enformatik Enstitüsü",
    "Graduate School of Informatics": "Enformatik Enstitüsü",
    "Deniz Bilimleri Enstitüsü": "Deniz Bilimleri Enstitüsü",
    "Institute of Marine Sciences": "Deniz Bilimleri Enstitüsü",
    "Fen Bilimleri Enstitüsü": "Fen Bilimleri Enstitüsü",
    "Graduate School of Natural and Applied Sciences": "Fen Bilimleri Enstitüsü",
    "Sosyal Bilimler Enstitüsü": "Sosyal Bilimler Enstitüsü",
    "Graduate School of Social Sciences": "Sosyal Bilimler Enstitüsü",
    "Meslek Yüksekokulu": "Meslek Yüksekokulu",
    "Yabancı Diller Yüksekokulu": "Yabancı Diller Yüksekokulu",
    "School of Foreign Languages": "Yabancı Diller Yüksekokulu",
    "Rektörlük": "Rektörlük",
    "Presidency Office": "Rektörlük",
    "ODTÜ Kuzey Kıbrıs Kampusu": "ODTÜ Kuzey Kıbrıs Kampusu",
    "ODTU-SUNY Uluslararası Ortak Lisans Programları": "ODTÜ-SUNY Uluslararası Ortak Lisans Programları",
    "Directorate of Computing (Computer Center)": "Rektörlük"
}

DEPARTMENT_MAPPING = {
    # Mimarlık Fakültesi
    "Mimarlık Bölümü": "Mimarlık Bölümü",
    "Department of Architecture": "Mimarlık Bölümü",
    "Şehir ve Bölge Planlama Bölümü": "Şehir ve Bölge Planlama Bölümü",
    "Department of City and Regional Planning": "Şehir ve Bölge Planlama Bölümü",
    "Endüstriyel Tasarım Bölümü": "Endüstriyel Tasarım Bölümü",
    "Department of Industrial Design": "Endüstriyel Tasarım Bölümü",
    
    # Fen Edebiyat Fakültesi
    "Biyolojik Bilimler Bölümü": "Biyolojik Bilimler Bölümü",
    "Department of Biology": "Biyolojik Bilimler Bölümü",
    "Kimya Bölümü": "Kimya Bölümü",
    "Department of Chemistry": "Kimya Bölümü",
    "Tarih Bölümü": "Tarih Bölümü",
    "Department of History": "Tarih Bölümü",
    "Matematik Bölümü": "Matematik Bölümü",
    "Department of Mathematics": "Matematik Bölümü",
    "Felsefe Bölümü": "Felsefe Bölümü",
    "Department of Philosophy": "Felsefe Bölümü",
    "Fizik Bölümü": "Fizik Bölümü",
    "Department of Physics": "Fizik Bölümü",
    "Psikoloji Bölümü": "Psikoloji Bölümü",
    "Department of Psychology": "Psikoloji Bölümü",
    "Sosyoloji Bölümü": "Sosyoloji Bölümü",
    "Department of Sociology": "Sosyoloji Bölümü",
    "İstatistik Bölümü": "İstatistik Bölümü",
    "Department of Statistics": "İstatistik Bölümü",
    
    # İktisadi ve İdari Bilimler Fakültesi
    "İşletme Bölümü": "İşletme Bölümü",
    "Department of Business Administration": "İşletme Bölümü",
    "İktisat Bölümü": "İktisat Bölümü",
    "Department of Economics": "İktisat Bölümü",
    "Uluslararası İlişkiler Bölümü": "Uluslararası İlişkiler Bölümü",
    "Department of International Relations": "Uluslararası İlişkiler Bölümü",
    "Siyaset Bilimi ve Kamu Yönetimi Bölümü": "Siyaset Bilimi ve Kamu Yönetimi Bölümü",
    "Department of Political Science and Public Administration": "Siyaset Bilimi ve Kamu Yönetimi Bölümü",
    
    # Eğitim Fakültesi
    "Bilgisayar ve Öğretim Teknolojileri Eğitimi Bölümü": "Bilgisayar ve Öğretim Teknolojileri Eğitimi Bölümü",
    "Department of Computer Education and Instructional Technology": "Bilgisayar ve Öğretim Teknolojileri Eğitimi Bölümü",
    "Eğitim Bilimleri Bölümü": "Eğitim Bilimleri Bölümü",
    "Department of Educational Sciences": "Eğitim Bilimleri Bölümü",
    "Temel Eğitim Bölümü": "Temel Eğitim Bölümü",
    "Department of Elementary and Early Childhood Education": "Temel Eğitim Bölümü",
    "Yabancı Diller Eğitimi Bölümü": "Yabancı Diller Eğitimi Bölümü",
    "Department of Foreign Language Education": "Yabancı Diller Eğitimi Bölümü",
    "Beden Eğitimi ve Spor Bölümü": "Beden Eğitimi ve Spor Bölümü",
    "Department of Physical Education and Sports": "Beden Eğitimi ve Spor Bölümü",
    "Matematik ve Fen Bilimleri Eğitimi Bölümü": "Matematik ve Fen Bilimleri Eğitimi Bölümü",
    "Mathematics and Science Education": "Matematik ve Fen Bilimleri Eğitimi Bölümü",
    
    # Mühendislik Fakültesi
    "Havacılık ve Uzay Mühendisliği Bölümü": "Havacılık ve Uzay Mühendisliği Bölümü",
    "Department of Aerospace Engineering": "Havacılık ve Uzay Mühendisliği Bölümü",
    "Kimya Mühendisliği Bölümü": "Kimya Mühendisliği Bölümü",
    "Department of Chemical Engineering": "Kimya Mühendisliği Bölümü",
    "İnşaat Mühendisliği Bölümü": "İnşaat Mühendisliği Bölümü",
    "Department of Civil Engineering": "İnşaat Mühendisliği Bölümü",
    "Bilgisayar Mühendisliği Bölümü": "Bilgisayar Mühendisliği Bölümü",
    "Department of Computer Engineering": "Bilgisayar Mühendisliği Bölümü",
    "Elektrik ve Elektronik Mühendisliği Bölümü": "Elektrik ve Elektronik Mühendisliği Bölümü",
    "Department of Electrical and Electronics Engineering": "Elektrik ve Elektronik Mühendisliği Bölümü",
    "Mühendislik Bilimleri Bölümü": "Mühendislik Bilimleri Bölümü",
    "Department of Engineering Sciences": "Mühendislik Bilimleri Bölümü",
    "Çevre Mühendisliği Bölümü": "Çevre Mühendisliği Bölümü",
    "Department of Environmental Engineering": "Çevre Mühendisliği Bölümü",
    "Gıda Mühendisliği Bölümü": "Gıda Mühendisliği Bölümü",
    "Department of Food Engineering": "Gıda Mühendisliği Bölümü",
    "Jeoloji Mühendisliği Bölümü": "Jeoloji Mühendisliği Bölümü",
    "Department of Geological Engineering": "Jeoloji Mühendisliği Bölümü",
    "Endüstri Mühendisliği Bölümü": "Endüstri Mühendisliği Bölümü",
    "Department of Industrial Engineering": "Endüstri Mühendisliği Bölümü",
    "Makina Mühendisliği Bölümü": "Makina Mühendisliği Bölümü",
    "Department of Mechanical Engineering": "Makina Mühendisliği Bölümü",
    "Metalurji ve Malzeme Mühendisliği Bölümü": "Metalurji ve Malzeme Mühendisliği Bölümü",
    "Department of Metallurgical and Materials Engineering": "Metalurji ve Malzeme Mühendisliği Bölümü",
    "Maden Mühendisliği Bölümü": "Maden Mühendisliği Bölümü",
    "Department of Mining Engineering": "Maden Mühendisliği Bölümü",
    "Petrol ve Doğal Gaz Mühendisliği Bölümü": "Petrol ve Doğal Gaz Mühendisliği Bölümü",
    "Department of Petroleum and Natural Gas Engineering": "Petrol ve Doğal Gaz Mühendisliği Bölümü",
    
    # Enstitüler (Sub-divisions)
    "Modelleme ve Simülasyon Anabilim Dalı": "Modelleme ve Simülasyon Anabilim Dalı",
    "Bilişim Sistemleri Anabilim Dalı": "Bilişim Sistemleri Anabilim Dalı",
    "Information Systems": "Bilişim Sistemleri Anabilim Dalı",
    "Siber Güvenlik Anabilim Dalı": "Siber Güvenlik Anabilim Dalı",
    "Cognitive Science": "Bilişsel Bilimler Anabilim Dalı",
    "Data Informatics": "Veri Bilişimi Anabilim Dalı",
    "Medical Informatics": "Tıbbi Bilişim Anabilim Dalı",
    "Bilimsel Hesaplama Anabilim Dalı": "Bilimsel Hesaplama Anabilim Dalı",
    "Actuarial Science": "Aktüerya Bilimleri Anabilim Dalı",
    "Cryptography": "Kriptografi Anabilim Dalı",
    "Financial Mathematics": "Finansal Matematik Anabilim Dalı",
    "Deniz Biyolojisi ve Balıkçılık Anabilim Dalı": "Deniz Biyolojisi ve Balıkçılık Anabilim Dalı",
    "Marine Biology and Fisheries": "Deniz Biyolojisi ve Balıkçılık Anabilim Dalı",
    "Deniz Jeolojisi ve Jeofiziği Anabilim Dalı": "Deniz Jeolojisi ve Jeofiziği Anabilim Dalı",
    "Deniz Bilim (Osinografi) Anabilim Dalı": "Deniz Bilimleri (Oşinografi) Anabilim Dalı",
    "Oceanography": "Deniz Bilimleri (Oşinografi) Anabilim Dalı",
    
    # Yabancı Diller Yüksekokulu
    "Yabancı Diller Bölümü": "Yabancı Diller Bölümü",
    "Depatment of Foreign Languages": "Yabancı Diller Bölümü",  # Typo correction
    
    # Rektörlüğe Bağlı Bölümler
    "Türk Dili Bölümü": "Türk Dili Bölümü",
    "Müzik ve Güzel Sanatlar Bölümü": "Müzik ve Güzel Sanatlar Bölümü",
    "Bilim İletişimi Ofisi": "Bilim İletişimi Ofisi",
    "Uluslararası İşbirliği Ofisi": "Uluslararası İşbirliği Ofisi",
    "Kurumsal Veri Yönetimi Koordinatörlüğü": "Kurumsal Veri Yönetimi Koordinatörlüğü",
    "Yapı Teknolojileri ve İleri Hesaplama Yöntemleri Koordinatörlüğü": "Yapı Teknolojileri ve İleri Hesaplama Yöntemleri Koordinatörlüğü",
    "İleri Teknolojilerde Test ve Ölçüm Merkezi": "İleri Teknolojilerde Test ve Ölçüm Merkezi",
    "Tasarım ve Önmodelleme Uygulama ve Araştırma Merkezi (Tasarım Fabrikası)": "Tasarım ve Önmodelleme Uygulama ve Araştırma Merkezi (Tasarım Fabrikası)",
    "METU Distance Education Application and Research Center": "ODTÜ Uzaktan Eğitim Uygulama ve Araştırma Merkezi",
    "Central Laboratory": "Merkez Laboratuvarı",
    "Teknik Destek Grubu": "Teknik Destek Grubu"
}

# Mapping Functions (Updated to handle non-string inputs)
def map_faculty(faculty_name):
    """Map faculty names to official METU faculty names."""
    if isinstance(faculty_name, str):  # Check if the input is a string
        return FACULTY_MAPPING.get(faculty_name.strip(), faculty_name)
    return faculty_name  # Return as-is if not a string (e.g., NaN or number)

def map_department(department_name):
    """Map department names to official METU department names."""
    if isinstance(department_name, str):  # Check if the input is a string
        return DEPARTMENT_MAPPING.get(department_name.strip(), department_name)
    return department_name  # Return as-is if not a string (e.g., NaN or number)

# Dosya yükleme desteği
st.header("Veri Dosyası Yükleme", anchor="veri-dosyasi-yukleme")
uploaded_file = st.file_uploader("Lütfen <ODTU Yayın ve Proje Başvuru Planları> dosyasını yükleyin", type=["xlsx"])

if uploaded_file is not None:
    # Excel dosyasını oku ve hata yönetimi
    try:
        df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip()  # Sütun isimlerinden boşlukları temizle
        
        # Apply mapping to 'Birim' and 'Bölüm' columns
        if 'Birim' in df.columns:
            df['Birim'] = df['Birim'].apply(map_faculty)
        if 'Bölüm' in df.columns:
            df['Bölüm'] = df['Bölüm'].apply(map_department)
        
        # Apply custom sorting order
        df['Birim'] = pd.Categorical(df['Birim'], categories=[f for f in FACULTY_ORDER if f in df['Birim'].unique()], ordered=True)
        df['Bölüm'] = pd.Categorical(df['Bölüm'], categories=[d for d in DEPARTMENT_ORDER if d in df['Bölüm'].unique()], ordered=True)
        
        st.success("Dosya başarıyla yüklendi ve fakülte/bölüm isimleri standardize edildi!")
        
        # Check for unmapped faculties or departments
        unmapped_faculties = df['Birim'][~df['Birim'].isin(FACULTY_MAPPING.values())].unique()
        unmapped_departments = df['Bölüm'][~df['Bölüm'].isin(DEPARTMENT_MAPPING.values())].unique()
        
        if unmapped_faculties.size > 0 or unmapped_departments.size > 0:
            with st.expander("Eşleştirilemeyen Birim ve Bölümler"):
                if unmapped_faculties.size > 0:
                    st.warning("Eşleştirilemeyen Birimler:")
                    for faculty in unmapped_faculties:
                        st.write(f"- {faculty}")
                if unmapped_departments.size > 0:
                    st.warning("Eşleştirilemeyen Bölümler:")
                    for dept in unmapped_departments:
                        st.write(f"- {dept}")
        
    except Exception as e:
        st.error(f"Dosya okunurken bir hata oluştu: {e}")
        st.stop()

    # Hataları kontrol eden ve sorunlu araştırmacıları kaldıran fonksiyon
    def check_and_remove_errors(df):
        numeric_cols = [col for col in df.columns if "(202" in col]
        eu_cols = [col for col in df.columns if "AB Projesi" in col]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        removed_entries = []
        neg_mask = df[numeric_cols].lt(0).any(axis=1)
        neg_indices = df[neg_mask].index
        for idx in neg_indices:
            researcher = df.loc[idx, "Ad Soyad"]
            neg_cols = [col for col in numeric_cols if df.loc[idx, col] < 0]
            for col in neg_cols:
                reason = f"Negative value ({df.loc[idx, col]}) in {col}"
                removed_entries.append({"Ad Soyad": researcher, "Reason": reason})
        eu_threshold = 50
        eu_mask = df[eu_cols].gt(eu_threshold).any(axis=1)
        eu_indices = df[eu_mask].index
        for idx in eu_indices:
            researcher = df.loc[idx, "Ad Soyad"]
            high_eu_cols = [col for col in eu_cols if df.loc[idx, col] > eu_threshold]
            for col in high_eu_cols:
                reason = f"Abnormally high project count ({df.loc[idx, col]}) in {col}"
                removed_entries.append({"Ad Soyad": researcher, "Reason": reason})
        indices_to_remove = set(neg_indices).union(set(eu_indices))
        removed_df = pd.DataFrame(removed_entries)
        cleaned_df = df.drop(index=indices_to_remove).reset_index(drop=True)
        return cleaned_df, removed_df

    # Hata kontrolü ve kaldırma fonksiyonunu uygula
    df, removed_df = check_and_remove_errors(df)

    # Kaldırılan girişleri gizli/tıklanabilir bir listede göster
    st.header("Veri Hataları Nedeniyle Kaldırılan Araştırmacılar", anchor="veri-hatalari")
    if not removed_df.empty:
        with st.expander("View Removed Entries"):
            for _, row in removed_df.iterrows():
                st.write(f"- **{row['Ad Soyad']}**: {row['Reason']}")
    else:
        st.info("Veri hataları nedeniyle kaldırılan araştırmacı yok.")

    # Optimize edilmiş "Unvan" çıkarma fonksiyonu
    def extract_title(name):
        titles = [
            "Prof. Dr.", "Prof.", "Doç. Dr.", "Dr. Öğr. Üyesi", "Öğr. Gör.", "Arş. Gör.",
            "Asst. Prof.", "Assoc. Prof.", "Lect. PhD", "Res. Asst."
        ]
        title_mapping = {
            "Prof. Dr.": "Prof. Dr.",
            "Prof.": "Prof. Dr.",
            "Doç. Dr.": "Doç. Dr.",
            "Dr. Öğr. Üyesi": "Dr. Öğr. Üyesi",
            "Öğr. Gör.": "Öğr. Gör.",
            "Arş. Gör.": "Arş. Gör.",
            "Asst. Prof.": "Dr. Öğr. Üyesi",
            "Assoc. Prof.": "Doç. Dr.",
            "Lect. PhD": "Öğr. Gör.",
            "Res. Asst.": "Arş. Gör."
        }
        for title in titles:
            if title in name:
                return title_mapping[title]
        return "Diğer"

    # Unvan sütununu ekle
    df["Unvan"] = df["Ad Soyad"].apply(extract_title)

    # Veri özeti (Veri bilgisi gizlenebilir şekilde)
    st.header("Veri Özeti", anchor="veri-ozeti")
    st.write("**İlk birkaç satır:**")
    st.dataframe(df.head())

    with st.expander("Veri Bilgisini Görüntüle"):
        st.write("**Veri bilgisi:**")
        buffer = StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())
        st.write("**Benzersiz değer sayıları:**")
        st.write(df.nunique())

    # 1. Bölüm Bazında Proje/Yayın Dağılımı
    st.header("Bölüm Bazında Proje/Yayın Dağılımı", anchor="bolum-bazinda-dagilim")
    count_data = df["Bölüm"].value_counts().reset_index()
    count_data.columns = ["Bölüm", "Sayı"]
    count_data["Bölüm"] = pd.Categorical(count_data["Bölüm"], categories=DEPARTMENT_ORDER, ordered=True)
    count_data = count_data.sort_values("Bölüm")
    fig1 = px.bar(count_data, x="Bölüm", y="Sayı", title="Bölüm Bazında Proje/Yayın Dağılımı")
    fig1.update_layout(
        xaxis={'tickangle': 45},
        height=600,
        width=3000,
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=False
    )
    fig1.update_traces(marker_color="blue")
    st.plotly_chart(fig1, use_container_width=True)
    st.write("**Açıklama:** Bölüm başına araştırmacı sayısı.")

    # 2. Birim Bazında Proje/Yayın Dağılımı
    st.header("Birim Bazında Proje/Yayın Dağılımı", anchor="birim-bazinda-dagilim")
    count_data_birim = df["Birim"].value_counts().reset_index()
    count_data_birim.columns = ["Birim", "Sayı"]
    count_data_birim["Birim"] = pd.Categorical(count_data_birim["Birim"], categories=FACULTY_ORDER, ordered=True)
    count_data_birim = count_data_birim.sort_values("Birim")
    fig2 = px.bar(count_data_birim, x="Birim", y="Sayı", title="Birim Bazında Proje/Yayın Dağılımı")
    fig2.update_layout(
        xaxis={'tickangle': 45},
        height=500,
        width=3000,
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=False
    )
    fig2.update_traces(marker_color="blue")
    st.plotly_chart(fig2, use_container_width=True)
    st.write("**Açıklama:** Birim (örneğin fakülte) başına araştırmacı sayısı.")

    # 3. Bölüm ve Unvan Bazında Başvuru Sayısı (Balon Grafiği)
    st.header("Bölüm ve Unvan Bazında Başvuru Sayısı (Balon Grafiği)", anchor="bolum-unvan-balon")
    bubble_data = df.groupby(["Bölüm", "Unvan"]).size().reset_index(name="Başvuru Sayısı")
    bubble_data["Unvan"] = pd.Categorical(bubble_data["Unvan"], categories=title_order, ordered=True)
    bubble_data["Bölüm"] = pd.Categorical(bubble_data["Bölüm"], categories=DEPARTMENT_ORDER, ordered=True)
    bubble_data = bubble_data.sort_values(["Bölüm", "Unvan"])
    fig3 = px.scatter(bubble_data, x="Unvan", y="Bölüm", size="Başvuru Sayısı", 
                      title="Bölüm ve Unvan Bazında Başvuru Sayısı",
                      labels={"Başvuru Sayısı": "Başvuru Sayısı"})
    fig3.update_layout(
        height=600,
        width=3000,
        xaxis={'tickangle': 45},
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=False
    )
    st.plotly_chart(fig3, use_container_width=True)
    st.write("**Açıklama:** Bölüm ve unvan başına araştırmacı sayısı. Balon büyüklüğü sayıyı gösterir.")

    # 3b. Birim ve Unvan Bazında Başvuru Sayısı (Balon Grafiği)
    st.header("Birim ve Unvan Bazında Başvuru Sayısı (Balon Grafiği)", anchor="birim-unvan-balon")
    bubble_data_birim = df.groupby(["Birim", "Unvan"]).size().reset_index(name="Başvuru Sayısı")
    bubble_data_birim["Unvan"] = pd.Categorical(bubble_data_birim["Unvan"], categories=title_order, ordered=True)
    bubble_data_birim["Birim"] = pd.Categorical(bubble_data_birim["Birim"], categories=FACULTY_ORDER, ordered=True)
    bubble_data_birim = bubble_data_birim.sort_values(["Birim", "Unvan"])
    fig3b = px.scatter(bubble_data_birim, x="Unvan", y="Birim", size="Başvuru Sayısı", 
                       title="Birim ve Unvan Bazında Başvuru Sayısı",
                       labels={"Başvuru Sayısı": "Başvuru Sayısı"})
    fig3b.update_layout(
        height=600,
        width=3000,
        xaxis={'tickangle': 45},
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=False
    )
    st.plotly_chart(fig3b, use_container_width=True)
    st.write("**Açıklama:** Birim ve unvan başına araştırmacı sayısı. Balon büyüklüğü sayıyı gösterir.")

    # 4. Bölüm ve Unvan Bazında Dağılım (Isı Haritası)
    st.header("Bölüm ve Unvan Bazında Dağılım (Isı Haritası)", anchor="bolum-unvan-isi")
    title_counts = df["Unvan"].value_counts()
    rare_titles = title_counts[title_counts < 5].index
    df_heatmap = df.copy()
    df_heatmap["Unvan"] = df_heatmap["Unvan"].replace(rare_titles, "Diğer")
    heatmap_data = df_heatmap.pivot_table(index="Bölüm", columns="Unvan", aggfunc="size", fill_value=0)
    heatmap_data = heatmap_data.loc[heatmap_data.sum(axis=1) > 0, heatmap_data.sum(axis=0) > 0]
    heatmap_data = heatmap_data.reindex(index=[d for d in DEPARTMENT_ORDER if d in heatmap_data.index], columns=title_order)
    fig4 = px.imshow(
        heatmap_data,
        text_auto=True,
        color_continuous_scale="Blues",
        title="Bölüm ve Unvan Bazında Dağılım",
        labels=dict(x="Unvan", y="Bölüm", color="Sayı")
    )
    fig4.update_layout(
        height=1200,
        width=1800,
        xaxis_tickfont_size=14,
        yaxis_tickfont_size=14,
        xaxis={'tickangle': 45},
        title_font_size=20,
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=False
    )
    fig4.update_traces(
        hovertemplate="Bölüm: %{y}<br>Unvan: %{x}<br>Sayı: %{z}",
        textfont=dict(size=12)
    )
    st.plotly_chart(fig4, use_container_width=True)
    st.write("**Açıklama:** Bölüm ve unvan başına araştırmacı sayısı. Renkler sayıyı gösterir, koyu renk daha fazla kişi demek.")

    # 4b. Birim ve Unvan Bazında Dağılım (Isı Haritası)
    st.header("Birim ve Unvan Bazında Dağılım (Isı Haritası)", anchor="birim-unvan-isi")
    df_heatmap_birim = df.copy()
    df_heatmap_birim["Unvan"] = df_heatmap_birim["Unvan"].replace(rare_titles, "Diğer")
    heatmap_data_birim = df_heatmap_birim.pivot_table(index="Birim", columns="Unvan", aggfunc="size", fill_value=0)
    heatmap_data_birim = heatmap_data_birim.loc[heatmap_data_birim.sum(axis=1) > 0, heatmap_data_birim.sum(axis=0) > 0]
    heatmap_data_birim = heatmap_data_birim.reindex(index=[f for f in FACULTY_ORDER if f in heatmap_data_birim.index], columns=title_order)
    fig4b = px.imshow(
        heatmap_data_birim,
        text_auto=True,
        color_continuous_scale="Blues",
        title="Birim ve Unvan Bazında Dağılım",
        labels=dict(x="Unvan", y="Birim", color="Sayı")
    )
    fig4b.update_layout(
        height=1200,
        width=1800,
        xaxis_tickfont_size=14,
        yaxis_tickfont_size=14,
        xaxis={'tickangle': 45},
        title_font_size=20,
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=False
    )
    fig4b.update_traces(
        hovertemplate="Birim: %{y}<br>Unvan: %{x}<br>Sayı: %{z}",
        textfont=dict(size=12)
    )
    st.plotly_chart(fig4b, use_container_width=True)
    st.write("**Açıklama:** Birim ve unvan başına araştırmacı sayısı. Renkler sayıyı gösterir, koyu renk daha fazla kişi demek.")

    # 5. Bölüm ve Unvan Bazında Başvuru Sayısı (Etkileşimli Çubuk Grafiği)
    st.header("Bölüm ve Unvan Bazında Başvuru Sayısı (Etkileşimli Çubuk Grafiği)", anchor="bolum-unvan-cubuk")
    bar_data = df.groupby(["Bölüm", "Unvan"]).size().reset_index(name="Başvuru Sayısı")
    bar_data["Unvan"] = pd.Categorical(bar_data["Unvan"], categories=title_order, ordered=True)
    bar_data["Bölüm"] = pd.Categorical(bar_data["Bölüm"], categories=DEPARTMENT_ORDER, ordered=True)
    bar_data = bar_data.sort_values(["Bölüm", "Unvan"])
    fig7 = px.bar(bar_data, x="Bölüm", y="Başvuru Sayısı", color="Unvan",
                  title="Bölüm ve Unvan Bazında Başvuru Sayısı",
                  labels={"Başvuru Sayısı": "Başvuru Sayısı"})
    fig7.update_layout(
        xaxis={'tickangle': 45},
        height=600,
        width=3000,
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=False
    )
    st.plotly_chart(fig7, use_container_width=True)
    st.write("**Açıklama:** Bölüm başına araştırmacı sayısı. Unvanlara göre renklere ayrılmıştır.")

    # 5b. Birim ve Unvan Bazında Başvuru Sayısı (Etkileşimli Çubuk Grafiği)
    st.header("Birim ve Unvan Bazında Başvuru Sayısı (Etkileşimli Çubuk Grafiği)", anchor="birim-unvan-cubuk")
    bar_data_birim = df.groupby(["Birim", "Unvan"]).size().reset_index(name="Başvuru Sayısı")
    bar_data_birim["Unvan"] = pd.Categorical(bar_data_birim["Unvan"], categories=title_order, ordered=True)
    bar_data_birim["Birim"] = pd.Categorical(bar_data_birim["Birim"], categories=FACULTY_ORDER, ordered=True)
    bar_data_birim = bar_data_birim.sort_values(["Birim", "Unvan"])
    fig7b = px.bar(bar_data_birim, x="Birim", y="Başvuru Sayısı", color="Unvan",
                   title="Birim ve Unvan Bazında Başvuru Sayısı",
                   labels={"Başvuru Sayısı": "Başvuru Sayısı"})
    fig7b.update_layout(
        xaxis={'tickangle': 45},
        height=600,
        width=3000,
        margin=dict(l=30, r=30, t=30, b=30),
        autosize=False
    )
    st.plotly_chart(fig7b, use_container_width=True)
    st.write("**Açıklama:** Birim başına araştırmacı sayısı. Unvanlara göre renklere ayrılmıştır.")

    # 6. Yıl Bazında Yayın Türü Dağılımı (Yığılmış Çubuk Grafiği)
    st.header("Yıl Bazında Yayın Türü Dağılımı", anchor="yil-bazinda-yayin")
    pub_cols = [col for col in df.columns if "SCI" in col or "ESCI" in col or "Scopus" in col]
    pub_data = df[pub_cols].sum().reset_index()
    pub_data["Yıl"] = pub_data["index"].str.extract(r"\((\d{4})\)")[0]
    pub_data["Tür"] = pub_data["index"].str.replace(r"\(\d{4}\)\s*", "", regex=True)
    fig8 = px.bar(pub_data, x="Yıl", y=0, color="Tür", barmode="stack",
                  title="Yıl Bazında Yayın Türü Dağılımı")
    fig8.update_layout(height=600, width=1000)
    st.plotly_chart(fig8, use_container_width=True)
    st.write("**Açıklama:** Her yıl için yayın türleri (SCI, ESCI, Scopus). Türler renklere ayrılmıştır.")

    # 7. Bölüm Bazında Proje Türü Dağılımı (Isı Haritası)
    st.header("Bölüm Bazında Proje Türü Dağılımı", anchor="bolum-proje-turu")
    proj_cols = [col for col in df.columns if any(p in col for p in ["1001", "1002", "1003", "1004", "1005", "1007", "1505", "1513", "AB Projesi"])]
    for col in proj_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    heatmap_proj_data = df.groupby("Bölüm")[proj_cols].sum()
    heatmap_proj_data = heatmap_proj_data.loc[heatmap_proj_data.sum(axis=1) > 0, heatmap_proj_data.sum(axis=0) > 0]
    heatmap_proj_data = heatmap_proj_data.reindex(index=[d for d in DEPARTMENT_ORDER if d in heatmap_proj_data.index])
    fig9 = px.imshow(heatmap_proj_data, title="Bölüm Bazında Proje Türü Dağılımı",
                     labels=dict(x="Proje Türü", y="Bölüm", color="Sayı"))
    fig9.update_layout(height=800, width=1200, xaxis={'tickangle': 45})
    st.plotly_chart(fig9, use_container_width=True)
    st.write("**Açıklama:** Bölüm başına proje türleri (örneğin 1001, AB Projesi). Renkler proje sayısını gösterir.")

    # 7b. Birim Bazında Proje Türü Dağılımı (Isı Haritası)
    st.header("Birim Bazında Proje Türü Dağılımı", anchor="birim-proje-turu")
    heatmap_proj_data_birim = df.groupby("Birim")[proj_cols].sum()
    heatmap_proj_data_birim = heatmap_proj_data_birim.loc[heatmap_proj_data_birim.sum(axis=1) > 0, heatmap_proj_data_birim.sum(axis=0) > 0]
    heatmap_proj_data_birim = heatmap_proj_data_birim.reindex(index=[f for f in FACULTY_ORDER if f in heatmap_proj_data_birim.index])
    fig9b = px.imshow(heatmap_proj_data_birim, title="Birim Bazında Proje Türü Dağılımı",
                      labels=dict(x="Proje Türü", y="Birim", color="Sayı"))
    fig9b.update_layout(height=800, width=1200, xaxis={'tickangle': 45})
    st.plotly_chart(fig9b, use_container_width=True)
    st.write("**Açıklama:** Birim başına proje türleri. Renkler proje sayısını gösterir.")

    # 8. Bölüm Bazında Araştırmacı Verimliliği (Kutu Grafiği)
    st.header("Bölüm Bazında Araştırmacı Verimliliği", anchor="bolum-verimlilik")
    output_cols = [col for col in df.columns if "(202" in col]
    for col in output_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    df["Toplam Çıktı"] = df[output_cols].sum(axis=1)
    fig10 = px.box(df, x="Bölüm", y="Toplam Çıktı", title="Bölüm Bazında Araştırmacı Verimliliği")
    fig10.update_layout(
        height=600,
        width=3000,
        xaxis={'tickangle': 45}
    )
    st.plotly_chart(fig10, use_container_width=True)
    st.write("**Açıklama:** Bölüm başına toplam çıktı (yayın ve proje). Kutu grafiği dağılımı gösterir.")

    # 8b. Birim Bazında Araştırmacı Verimliliği (Kutu Grafiği)
    st.header("Birim Bazında Araştırmacı Verimliliği", anchor="birim-verimlilik")
    fig10b = px.box(df, x="Birim", y="Toplam Çıktı", title="Birim Bazında Araştırmacı Verimliliği")
    fig10b.update_layout(
        height=600,
        width=3000,
        xaxis={'tickangle': 45}
    )
    st.plotly_chart(fig10b, use_container_width=True)
    st.write("**Açıklama:** Birim başına toplam çıktı (yayın ve proje). Kutu grafiği dağılımı gösterir.")

    # 9. Bölüm Bazında Zaman İçindeki Planlanan Çıktılar (Çizgi Grafiği)
    st.header("Bölüm Bazında Zaman İçindeki Planlanan Çıktılar", anchor="bolum-zaman")
    yearly_cols = {year: [col for col in df.columns if f"({year})" in col] for year in ["2025", "2026", "2027"]}
    yearly_sums = {year: df.groupby("Bölüm")[cols].sum().sum(axis=1) for year, cols in yearly_cols.items()}
    time_data = pd.DataFrame(yearly_sums).stack().reset_index()
    time_data.columns = ["Bölüm", "Yıl", "Sayı"]
    time_data["Yıl"] = pd.Categorical(time_data["Yıl"], categories=["2025", "2026", "2027"], ordered=True)
    time_data["Bölüm"] = pd.Categorical(time_data["Bölüm"], categories=DEPARTMENT_ORDER, ordered=True)
    fig11 = px.line(time_data, x="Yıl", y="Sayı", color="Bölüm", title="Bölüm Bazında Zaman İçindeki Planlanan Çıktılar")
    fig11.update_layout(
        height=600,
        width=1000,
        xaxis=dict(
            type='category',
            tickmode='array',
            tickvals=["2025", "2026", "2027"],
            ticktext=["2025", "2026", "2027"]
        )
    )
    st.plotly_chart(fig11, use_container_width=True)
    st.write("**Açıklama:** Bölüm başına 2025-2027 yılları için planlanan toplam çıktı. Her çizgi bir bölümü gösterir.")

    # 9b. Birim Bazında Zaman İçindeki Planlanan Çıktılar (Çizgi Grafiği)
    st.header("Birim Bazında Zaman İçindeki Planlanan Çıktılar", anchor="birim-zaman")
    yearly_sums_birim = {year: df.groupby("Birim")[cols].sum().sum(axis=1) for year, cols in yearly_cols.items()}
    time_data_birim = pd.DataFrame(yearly_sums_birim).stack().reset_index()
    time_data_birim.columns = ["Birim", "Yıl", "Sayı"]
    time_data_birim["Yıl"] = pd.Categorical(time_data_birim["Yıl"], categories=["2025", "2026", "2027"], ordered=True)
    time_data_birim["Birim"] = pd.Categorical(time_data_birim["Birim"], categories=FACULTY_ORDER, ordered=True)
    fig11b = px.line(time_data_birim, x="Yıl", y="Sayı", color="Birim", title="Birim Bazında Zaman İçindeki Planlanan Çıktılar")
    fig11b.update_layout(
        height=600,
        width=1000,
        xaxis=dict(
            type='category',
            tickmode='array',
            tickvals=["2025", "2026", "2027"],
            ticktext=["2025", "2026", "2027"]
        )
    )
    st.plotly_chart(fig11b, use_container_width=True)
    st.write("**Açıklama:** Birim başına 2025-2027 yılları için planlanan toplam çıktı. Her çizgi bir birimi gösterir.")

    # 10. Bölüm Bazında Yayın Kalitesi ve Proje Katılımı (Dağılım Grafiği)
    st.header("Bölüm Bazında Yayın Kalitesi ve Proje Katılımı", anchor="bolum-yayin-kalitesi")
    q1q2_cols = [col for col in df.columns if "Q1" in col or "Q2" in col]
    proj_cols = [col for col in df.columns if any(p in col for p in ["1001", "1002", "1003", "1004", "1005", "1007", "1505", "1513", "AB Projesi"])]
    df["Q1+Q2 Yayınlar"] = df[q1q2_cols].sum(axis=1)
    df["Projeler"] = df[proj_cols].sum(axis=1)
    df["Toplam Çıktı"] = df[output_cols].sum(axis=1)
    df["Toplam Çıktı (Kesilmiş)"] = df["Toplam Çıktı"].clip(lower=0)
    fig12 = px.scatter(df, x="Q1+Q2 Yayınlar", y="Projeler", color="Bölüm", size="Toplam Çıktı (Kesilmiş)",
                       title="Bölüm Bazında Yayın Kalitesi ve Proje Katılımı")
    fig12.update_layout(height=600, width=1000)
    st.plotly_chart(fig12, use_container_width=True)
    st.write("**Açıklama:** Q1+Q2 yayınlar ve projeler. Bölümlere göre renklendirilmiş. Nokta büyüklüğü toplam çıktıyı gösterir.")

    # 10b. Birim Bazında Yayın Kalitesi ve Proje Katılımı (Dağılım Grafiği)
    st.header("Birim Bazında Yayın Kalitesi ve Proje Katılımı", anchor="birim-yayin-kalitesi")
    fig12b = px.scatter(df, x="Q1+Q2 Yayınlar", y="Projeler", color="Birim", size="Toplam Çıktı (Kesilmiş)",
                        title="Birim Bazında Yayın Kalitesi ve Proje Katılımı")
    fig12b.update_layout(height=600, width=1000)
    st.plotly_chart(fig12b, use_container_width=True)
    st.write("**Açıklama:** Q1+Q2 yayınlar ve projeler. Birimlere göre renklendirilmiş. Nokta büyüklüğü toplam çıktıyı gösterir.")

    # 11. Birim Bazında AB Projesi Dağılımı (Pasta Grafiği)
    st.header("Birim Bazında AB Projesi Dağılımı", anchor="birim-ab-projesi")
    eu_cols = [col for col in df.columns if "AB Projesi" in col]
    eu_data = df.groupby("Birim")[eu_cols].sum().sum(axis=1).reset_index()
    eu_data.columns = ["Birim", "AB Projeleri"]
    eu_data["Birim"] = pd.Categorical(eu_data["Birim"], categories=FACULTY_ORDER, ordered=True)
    fig13 = px.pie(eu_data, names="Birim", values="AB Projeleri", title="Birim Bazında AB Projesi Dağılımı")
    fig13.update_layout(height=600, width=1000)
    st.plotly_chart(fig13, use_container_width=True)
    st.write("**Açıklama:** Birimlere göre AB projeleri. Her dilim bir birimi gösterir.")

    # 12. Yıl Bazında Yayın Kalitesi Dağılımı (Pasta Grafiği)
    st.header("Yıl Bazında Yayın Kalitesi Dağılımı", anchor="yil-yayin-kalitesi")
    pub_quality_cols = [col for col in df.columns if "SCI, SCI-E, SSCI veya AHCI kapsamındaki hakemli dergide yayımlanan tam makale veya derleme" in col]
    pub_quality_data = df[pub_quality_cols].sum().reset_index()
    pub_quality_data["Yıl"] = pub_quality_data["index"].str.extract(r"\((\d{4})\)")[0]
    pub_quality_data["Kalite"] = pub_quality_data["index"].str.extract(r"\((Q\d Grubu)\)")
    pub_quality_data = pub_quality_data.dropna(subset=["Kalite"])
    pub_quality_data = pub_quality_data.groupby(["Yıl", "Kalite"]).sum().reset_index()
    for year in ["2025", "2026", "2027"]:
        year_data = pub_quality_data[pub_quality_data["Yıl"] == year]
        fig = px.pie(year_data, names="Kalite", values=0, title=f"{year} Yılında Yayın Kalitesi Dağılımı")
        fig.update_layout(height=500, width=800)
        st.plotly_chart(fig, use_container_width=True)
        st.write(f"**Açıklama:** {year} yılı için yayın kalitesi (Q1, Q2, Q3, Q4). Her dilim bir kalite grubunu gösterir.")

    # 13. Toplam Yayın Sayısına Göre İlk 5 Bölüm (Çubuk Grafiği)
    st.header("Toplam Yayın Sayısına Göre İlk 5 Bölüm", anchor="top-5-bolum")
    pub_cols_all = [col for col in df.columns if any(p in col for p in ["SCI", "ESCI", "Scopus", "AHCI kapsamındaki hakemli dergide yayımlanan tam makale veya derleme (Quartile Sınıflandırması Bulunmayan)"])]
    df["Toplam Yayınlar"] = df[pub_cols_all].sum(axis=1)
    top_depts = df.groupby("Bölüm")["Toplam Yayınlar"].sum().reset_index()
    top_depts = top_depts.sort_values("Toplam Yayınlar", ascending=False).head(5)
    top_depts["Bölüm"] = pd.Categorical(top_depts["Bölüm"], categories=DEPARTMENT_ORDER, ordered=True)
    fig14 = px.bar(top_depts, x="Bölüm", y="Toplam Yayınlar", title="Toplam Yayın Sayısına Göre İlk 5 Bölüm")
    fig14.update_layout(
        xaxis={'tickangle': 45},
        height=500,
        width=1000
    )
    fig14.update_traces(marker_color="green")
    st.plotly_chart(fig14, use_container_width=True)
    st.write("**Açıklama:** En çok yayın yapan 5 bölüm. Toplam yayınlar SCI, ESCI, Scopus vb. içerir.")

    # 13b. Toplam Yayın Sayısına Göre İlk 5 Birim (Çubuk Grafiği)
    st.header("Toplam Yayın Sayısına Göre İlk 5 Birim", anchor="top-5-birim")
    top_faculties = df.groupby("Birim")["Toplam Yayınlar"].sum().reset_index()
    top_faculties = top_faculties.sort_values("Toplam Yayınlar", ascending=False).head(5)
    top_faculties["Birim"] = pd.Categorical(top_faculties["Birim"], categories=FACULTY_ORDER, ordered=True)
    fig14b = px.bar(top_faculties, x="Birim", y="Toplam Yayınlar", title="Toplam Yayın Sayısına Göre İlk 5 Birim")
    fig14b.update_layout(
        xaxis={'tickangle': 45},
        height=500,
        width=1000
    )
    fig14b.update_traces(marker_color="green")
    st.plotly_chart(fig14b, use_container_width=True)
    st.write("**Açıklama:** En çok yayın yapan 5 birim. Toplam yayınlar SCI, ESCI, Scopus vb. içerir.")

    # 14. Zaman İçindeki Proje Türü Dağılımı (Çizgi Grafiği)
    st.header("Zaman İçindeki Proje Türü Dağılımı", anchor="zaman-proje-turu")
    proj_type_data = df[proj_cols].sum().reset_index()
    proj_type_data["Yıl"] = proj_type_data["index"].str.extract(r"\((\d{4})\)")[0]
    proj_type_data["Proje Türü"] = proj_type_data["index"].str.replace(r"\(\d{4}\)\s*", "", regex=True)
    proj_type_data = proj_type_data.groupby(["Yıl", "Proje Türü"]).sum().reset_index()
    proj_type_data["Yıl"] = pd.Categorical(proj_type_data["Yıl"], categories=["2025", "2026", "2027"], ordered=True)
    fig15 = px.line(proj_type_data, x="Yıl", y=0, color="Proje Türü", title="Zaman İçindeki Proje Türü Dağılımı")
    fig15.update_layout(
        height=600,
        width=1000,
        xaxis=dict(
            type='category',
            tickmode='array',
            tickvals=["2025", "2026", "2027"],
            ticktext=["2025", "2026", "2027"]
        )
    )
    st.plotly_chart(fig15, use_container_width=True)
    st.write("**Açıklama:** 2025-2027 yılları için proje türleri (örneğin 1001, AB Projesi). Her çizgi bir türü gösterir.")

    # 15. Birim Bazında AB Projeleri ve Ulusal Projeler (Yığılmış Çubuk Grafiği)
    st.header("Birim Bazında AB Projeleri ve Ulusal Projeler", anchor="birim-ab-ulusal")
    national_proj_cols = [col for col in proj_cols if "AB Projesi" not in col]
    df["Ulusal Projeler"] = df[national_proj_cols].sum(axis=1)
    df["AB Projeleri"] = df[eu_cols].sum(axis=1)
    proj_comparison = df.groupby("Birim")[["Ulusal Projeler", "AB Projeleri"]].sum().reset_index()
    proj_comparison["Birim"] = pd.Categorical(proj_comparison["Birim"], categories=FACULTY_ORDER, ordered=True)
    proj_comparison_melted = proj_comparison.melt(id_vars="Birim", value_vars=["Ulusal Projeler", "AB Projeleri"], 
                                                  var_name="Proje Türü", value_name="Sayı")
    fig16 = px.bar(proj_comparison_melted, x="Birim", y="Sayı", color="Proje Türü", barmode="stack",
                   title="Birim Bazında AB Projeleri ve Ulusal Projeler")
    fig16.update_layout(
        xaxis={'tickangle': 45},
        height=600,
        width=3000
    )
    st.plotly_chart(fig16, use_container_width=True)
    st.write("**Açıklama:** Birim başına AB ve ulusal projeler. Renklere ayrılmıştır.")

    # 15b. Bölüm Bazında AB Projeleri ve Ulusal Projeler (Yığılmış Çubuk Grafiği)
    st.header("Bölüm Bazında AB Projeleri ve Ulusal Projeler", anchor="bolum-ab-ulusal")
    proj_comparison_dept = df.groupby("Bölüm")[["Ulusal Projeler", "AB Projeleri"]].sum().reset_index()
    proj_comparison_dept["Bölüm"] = pd.Categorical(proj_comparison_dept["Bölüm"], categories=DEPARTMENT_ORDER, ordered=True)
    proj_comparison_dept_melted = proj_comparison_dept.melt(id_vars="Bölüm", value_vars=["Ulusal Projeler", "AB Projeleri"], 
                                                            var_name="Proje Türü", value_name="Sayı")
    fig16b = px.bar(proj_comparison_dept_melted, x="Bölüm", y="Sayı", color="Proje Türü", barmode="stack",
                    title="Bölüm Bazında AB Projeleri ve Ulusal Projeler")
    fig16b.update_layout(
        xaxis={'tickangle': 45},
        height=600,
        width=3000
    )
    st.plotly_chart(fig16b, use_container_width=True)
    st.write("**Açıklama:** Bölüm başına AB ve ulusal projeler. Renklere ayrılmıştır.")

    # 16. Birim Bazında Yayın Çeyreklik Dağılımı (Pasta Grafiği)
    st.header("Birim Bazında Yayın Çeyreklik Dağılımı", anchor="birim-yayin-ceyreklik")
    pub_quartile_cols = [col for col in df.columns if "Q1 Grubu" in col or "Q2 Grubu" in col or "Q3 Grubu" in col or "Q4 Grubu" in col]
    pub_quartile_data = df.groupby("Birim")[pub_quartile_cols].sum().sum(axis=1).reset_index(name="Toplam")
    for quartile in ["Q1 Grubu", "Q2 Grubu", "Q3 Grubu", "Q4 Grubu"]:
        quartile_cols = [col for col in pub_quartile_cols if quartile in col]
        pub_quartile_data[quartile] = df.groupby("Birim")[quartile_cols].sum().sum(axis=1)
    pub_quartile_data["Birim"] = pd.Categorical(pub_quartile_data["Birim"], categories=FACULTY_ORDER, ordered=True)
    pub_quartile_melted = pub_quartile_data.melt(id_vars="Birim", value_vars=["Q1 Grubu", "Q2 Grubu", "Q3 Grubu", "Q4 Grubu"],
                                                 var_name="Çeyreklik", value_name="Sayı")
    for faculty in pub_quartile_data["Birim"].unique():
        faculty_data = pub_quartile_melted[pub_quartile_melted["Birim"] == faculty]
        if faculty_data["Sayı"].sum() > 0:
            fig = px.pie(faculty_data, names="Çeyreklik", values="Sayı", title=f"{faculty} için Yayın Çeyreklik Dağılımı")
            fig.update_layout(height=500, width=800)
            st.plotly_chart(fig, use_container_width=True)
            st.write(f"**Açıklama:** {faculty} için yayın çeyreklikleri (Q1, Q2, Q3, Q4). Her dilim bir çeyrekliği gösterir.")

    # 17. Toplam Sayıya Göre En İyi Proje Türleri (Çubuk Grafiği)
    st.header("Toplam Sayıya Göre En İyi Proje Türleri", anchor="en-iyi-proje-turleri")
    proj_type_totals = df[proj_cols].sum().reset_index()
    proj_type_totals["Proje Türü"] = proj_type_totals["index"].str.replace(r"\(\d{4}\)\s*", "", regex=True)
    proj_type_totals = proj_type_totals.groupby("Proje Türü").sum().reset_index()
    proj_type_totals = proj_type_totals.sort_values(0, ascending=False)
    fig17 = px.bar(proj_type_totals, x="Proje Türü", y=0, title="Toplam Sayıya Göre En İyi Proje Türleri")
    fig17.update_layout(
        xaxis={'tickangle': 45},
        height=500,
        width=1000
    )
    fig17.update_traces(marker_color="purple")
    st.plotly_chart(fig17, use_container_width=True)
    st.write("**Açıklama:** En çok kullanılan proje türleri. 2025-2027 toplamları.")

    # 18. Birim Bazında Yüksek Etkili (Q1+Q2) Yayınlar Zaman İçinde (Çizgi Grafiği)
    st.header("Birim Bazında Yüksek Etkili (Q1+Q2) Yayınlar Zaman İçinde", anchor="birim-yuksek-etki")
    q1q2_yearly = {year: df.groupby("Birim")[[col for col in q1q2_cols if f"({year})" in col]].sum().sum(axis=1) for year in ["2025", "2026", "2027"]}
    q1q2_time_data = pd.DataFrame(q1q2_yearly).stack().reset_index()
    q1q2_time_data.columns = ["Birim", "Yıl", "Q1+Q2 Yayınlar"]
    q1q2_time_data["Yıl"] = pd.Categorical(q1q2_time_data["Yıl"], categories=["2025", "2026", "2027"], ordered=True)
    q1q2_time_data["Birim"] = pd.Categorical(q1q2_time_data["Birim"], categories=FACULTY_ORDER, ordered=True)
    fig18 = px.line(q1q2_time_data, x="Yıl", y="Q1+Q2 Yayınlar", color="Birim",
                    title="Birim Bazında Yüksek Etkili (Q1+Q2) Yayınlar Zaman İçinde")
    fig18.update_layout(
        height=600,
        width=1000,
        xaxis=dict(
            type='category',
            tickmode='array',
            tickvals=["2025", "2026", "2027"],
            ticktext=["2025", "2026", "2027"]
        )
    )
    st.plotly_chart(fig18, use_container_width=True)
    st.write("**Açıklama:** Birim başına Q1+Q2 yayınlar (2025-2027). Her çizgi bir birimi gösterir.")

    # 18b. Bölüm Bazında Yüksek Etkili (Q1+Q2) Yayınlar Zaman İçinde (Çizgi Grafiği)
    st.header("Bölüm Bazında Yüksek Etkili (Q1+Q2) Yayınlar Zaman İçinde", anchor="bolum-yuksek-etki")
    q1q2_yearly_dept = {year: df.groupby("Bölüm")[[col for col in q1q2_cols if f"({year})" in col]].sum().sum(axis=1) for year in ["2025", "2026", "2027"]}
    q1q2_time_data_dept = pd.DataFrame(q1q2_yearly_dept).stack().reset_index()
    q1q2_time_data_dept.columns = ["Bölüm", "Yıl", "Q1+Q2 Yayınlar"]
    q1q2_time_data_dept["Yıl"] = pd.Categorical(q1q2_time_data_dept["Yıl"], categories=["2025", "2026", "2027"], ordered=True)
    q1q2_time_data_dept["Bölüm"] = pd.Categorical(q1q2_time_data_dept["Bölüm"], categories=DEPARTMENT_ORDER, ordered=True)
    fig18b = px.line(q1q2_time_data_dept, x="Yıl", y="Q1+Q2 Yayınlar", color="Bölüm",
                     title="Bölüm Bazında Yüksek Etkili (Q1+Q2) Yayınlar Zaman İçinde")
    fig18b.update_layout(
        height=600,
        width=1000,
        xaxis=dict(
            type='category',
            tickmode='array',
            tickvals=["2025", "2026", "2027"],
            ticktext=["2025", "2026", "2027"]
        )
    )
    st.plotly_chart(fig18b, use_container_width=True)
    st.write("**Açıklama:** Bölüm başına Q1+Q2 yayınlar (2025-2027). Her çizgi bir bölümü gösterir.")

    # 19. Proje Finansman Kaynağı Dağılımı (Pasta Grafiği)
    st.header("Proje Finansman Kaynağı Dağılımı", anchor="proje-finansman")
    funding_cols = [col for col in df.columns if any(p in col for p in ["1001", "1002", "1003", "1004", "1005", "1007", "1505", "1513", "AB Projesi", "CB Strateji ve Bütçe"])]
    funding_data = df[funding_cols].sum().reset_index()
    funding_data["Finansman Kaynağı"] = funding_data["index"].str.replace(r"\(\d{4}\)\s*", "", regex=True)
    funding_data = funding_data.groupby("Finansman Kaynağı").sum().reset_index()
    fig19 = px.pie(funding_data, names="Finansman Kaynağı", values=0, title="Proje Finansman Kaynağı Dağılımı")
    fig19.update_layout(height=600, width=1000)
    st.plotly_chart(fig19, use_container_width=True)
    st.write("**Açıklama:** Proje türlerine göre finansman kaynakları. Her dilim bir kaynağı gösterir.")

    # 20. Birim Bazında Yayın ve Proje Dengesi (Çubuk Grafiği)
    st.header("Birim Bazında Yayın ve Proje Dengesi", anchor="birim-yayin-proje-dengesi")
    balance_data = df.groupby("Birim")[["Toplam Yayınlar", "Projeler"]].sum().reset_index()
    balance_data["Birim"] = pd.Categorical(balance_data["Birim"], categories=FACULTY_ORDER, ordered=True)
    balance_data_melted = balance_data.melt(id_vars="Birim", value_vars=["Toplam Yayınlar", "Projeler"],
                                            var_name="Tür", value_name="Sayı")
    fig20 = px.bar(balance_data_melted, x="Birim", y="Sayı", color="Tür", barmode="group",
                   title="Birim Bazında Yayın ve Proje Dengesi")
    fig20.update_layout(
        xaxis={'tickangle': 45},
        height=600,
        width=3000
    )
    st.plotly_chart(fig20, use_container_width=True)
    st.write("**Açıklama:** Birim başına toplam yayın ve proje sayısı. Yan yana gösterilmiştir.")

    # 20b. Bölüm Bazında Yayın ve Proje Dengesi (Çubuk Grafiği)
    st.header("Bölüm Bazında Yayın ve Proje Dengesi", anchor="bolum-yayin-proje-dengesi")
    balance_data_dept = df.groupby("Bölüm")[["Toplam Yayınlar", "Projeler"]].sum().reset_index()
    balance_data_dept["Bölüm"] = pd.Categorical(balance_data_dept["Bölüm"], categories=DEPARTMENT_ORDER, ordered=True)
    balance_data_dept_melted = balance_data_dept.melt(id_vars="Bölüm", value_vars=["Toplam Yayınlar", "Projeler"],
                                                      var_name="Tür", value_name="Sayı")
    fig20b = px.bar(balance_data_dept_melted, x="Bölüm", y="Sayı", color="Tür", barmode="group",
                    title="Bölüm Bazında Yayın ve Proje Dengesi")
    fig20b.update_layout(
        xaxis={'tickangle': 45},
        height=600,
        width=3000
    )
    st.plotly_chart(fig20b, use_container_width=True)
    st.write("**Açıklama:** Bölüm başına toplam yayın ve proje sayısı. Yan yana gösterilmiştir.")

else:
    st.warning("Lütfen bir Excel dosyası yükleyin.")

# Uygulama sonu
st.write("---")
st.write("Kerem Delialioğlu")
st.write("Orta Doğu Teknik Üniversitesi — Proje Destek Ofisi")
st.write("2025")
