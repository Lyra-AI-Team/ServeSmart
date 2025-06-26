<h1>ServeSmart</h1>

# Yarışma Kapsamı
Bu yarışmadaki amacımız sürdürülebilir şehirler ve yeşil yarınlar için bir yapay zeka projesi geliştirmekti.

# Sunum
Sunumu [buradan](https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Lyra%20AI%20-%20ServeSmart.pptx) görebilirsiniz.

## Gereksinimler
 1. **Python:** Bu kodu kullanmak için Python 3.10 veya üstünü kullanıyor olmanız gerekir.
 2. **Dependencies:** Aşağıdaki kodu kullanarak `requirements.txt` dosyasından bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```
## Uygulamayı Çalıştırma
Başlamak için aşağıdaki adımları izleyin:
Kodu çalıştırmak için Streamlit kullanmanız gerekiyor. Aşağıdaki kodu kullanarak kullanıcı arayüzü klasöründeki `app.py` dosyasını çalıştırın:
```bash
streamlit run app.py
```

# Kod İşlevselliğine Genel Bakış

## Satıcı Hesabı Oluşturma
Streamlit uygulamamız beş sekme içerir. İlk sekme hesap oluşturmak içindir (satıcılar için). Sisteme kaydolmak için adımlar:
1. Kullanıcı adını girin.
2. Şifre girin.
3. Ödemeleri alacağınız IBAN numarasını girin.
4. Kimlik numaranızı girin (güvenlik için).
5. İş adresinizi girin (güvenlik için).

### Arayüz:
<div align="center">
<img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/create_account.PNG" width="1000" />
</div>

## Ürün Satma
İkincisi ürün satışı (ekleme) içindir. Ürün eklemek için adımlar:

1. Yemeğiniz hakkında bilgi girin (AI bunu geliştirecektir).
2. Yemeğinizin bir fotoğrafını çekin.
3. Yemeğinizin fiyatını girin.
4. IBAN numaranızı girin.
5. Kimlik numaranızı girin (güvenlik için).

### Arayüz:
<div align="center">
<img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/sell_product.PNG" width="1000" />
</div>

## Ürün Arama
Üçüncü sekme bir ürün arama özelliği sağlar. İşte nasıl çalıştığı:
1. Satın almak istediğiniz ürün adını girin ve arayın.
2. Satın alacağınız yemeğin ID'sini öğrenmeyi unutmayın.

### Arayüz:

<div align="center">
<img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/search_product.PNG" width="1000" />
</div>

## Ürün Satın Alma
Satın alacağınız yemeğe karar verdikten sonra, ürün satın al sayfasından satın alacaksınız.
1. Yemeğin kimliğini girin.
2. Adresinizi girin.
3. Kimlik numaranızı girin.
4. Kartınızın CVV'sini girin.
5. Kart numaranızı girin.

### Arayüz:

<div align="center">
<img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/buy_product.PNG" width="1000" />
</div>

## Ürünlerinizi Görün/Silin
Satıcı olarak ürünlerinizi ve analizlerinizi bu sayfadan görebilirsiniz. Burada yapmanız gerekenler:
1. Kullanıcı adınızı girin.
2. Şifrenizi giriniz.
3. Giriş yaptıktan sonra, ürününüzü ve sizin için yapılan analizleri görebilirsiniz.
4. Ürünlerinizi silebilirsiniz.

### Arayüz:

<div align="center">

 | Giriş Yapma | Analiz |
|---------|---------|
| <img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/see_products_login.PNG" width="300" /> | <img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/see_products_analysis.PNG" width="300" /> |

</div>

## Text Generation
Uygulamamızın Ürün Sat sekmesine güçlü bir metin oluşturma özelliği ekledik. İlk başta Llama ve Gemma modellerine ince ayar yapmaya çalıştık ve aslında yaptık. Fakat Gemini diye bir seçenek vardı. Testleri yaptık ve gemini-1.5-flash kullanmaya karar verdik. Böylece Gemini API'sini kullanmaya karar verdik. “Ürünü Gönder” butonuna bastıktan sonra Gemini'ye (gemini-1.5-flash) bir API isteği gönderiyoruz ve yemeğin başlık-açıklamasını geliştiriyoruz.

Örneği görebilirsiniz.

### Sonuç:

<div align="center">
<img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/text_generation.PNG" width="1000" />
</div>


# Kullanılan Sistem Özellikleri
- 1 T4-15GB GPU
- 12 GB RAM
>  [!WARNING]  
>  Bunu daha az güçlü donanımlarda çalıştırırken sorun yaşayabilirsiniz.

# Kullanılan Modeller

Proje, aşağıdaki modeller ile geliştirilmiştir:

1. **gemini-1.5-flash**:
   - **Kaynak:** [DeepMind](https://deepmind.google/technologies/gemini/flash/)
   - **Lisans:** API kullanıldı, lisans bilgisi yok
 
2. **ahmeterdempmk/FoodLlaMa-LoRA-Based**:
   - **Kaynak:** [Hugging Face](https://huggingface.co/ahmeterdempmk/Llama-3.1-8B-Fast-Food-Based-Tuned)
   - **Lisans:** Apache 2.0

3. **ahmeterdempmk/Gemma2-2b-E-Commerce-Tuned**:
   - **Kaynak:** [Hugging Face](https://huggingface.co/ahmeterdempmk/Gemma2-2b-E-Commerce-Tuned)
   - **Lisans:** Apache 2.0

4. **ahmeterdempmk/Llama-3.1-8B-Fast-Food-Based-Tuned**:
   - **Kaynak:** [Hugging Face](https://huggingface.co/ahmeterdempmk/Llama-3.1-8B-Fast-Food-Based-Tuned)
   - **Lisans:** Apache 2.0
     
5. **Emir Kaan Özdemir - LSTM Based Time Series Model**:
   - **Kaynak:** [GitHub](https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/User%20Interface/model.h5)
   - **Lisans:** Apache 2.0

> [!NOTE] 
> Lütfen bu projeyi kullanırken veya dağıtırken her modelin lisansına uyduğunuzdan emin olun.

# Katkı Sağlayanlar

- **[Ahmet Erdem Pamuk](https://github.com/ahmeterdempmk)**
- **[Emir Kaan Özdemir](https://github.com/emirkaanozdemr)**
- **[İlknur Yaren Karakoç](https://github.com/esholmess)**
