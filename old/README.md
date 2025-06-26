<h1>ServeSmart</h1>

# Competition Scope
Our purpose in this competition to develop an AI project for sustainable cities and green tomorrows.

## Requirements
 1. **Python:** To use this code you have to be using Python 3.10 or higher.
 2. **Dependencies:** Install dependencies from the `requirements.txt` file using the following code:
```bash
pip install -r requirements.txt
```
## Running the Application
To get started, follow these steps:
Now to run the code, you need to use Streamlit. Run the `app.py` file in the user interface folder using the following code:
```bash
streamlit run app.py
```

# Overview of Code Functionality

## Create Account to Sell
Our Streamlit application contains five tabs. The first tab is for creating accounts (for sellers). The instructions to sign up to system:
1. Enter username.
2. Enter password.
3. Enter the IBAN that you will get the payments.
4. Enter your ID no (for security).
5. Enter your business adress (for security).

### User Interface:
<div align="center">
<img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/create_account.PNG" width="1000" />
</div>

## Sell Product
The second one is for product selling (adding). The instructions to add product:
1. Enter informations about your meal (AI will improve it).
2. Take a photo of your meal.
3. Enter the price of your meal.
4. Enter your IBAN.
5. Enter your ID no (for security).

### User Interface:
<div align="center">
<img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/sell_product.PNG" width="1000" />
</div>

## Search Product
The third tab provides a search product feature. Here’s how it works:
1. Enter the product name you want to buy and search it.
2. Don't forget learn the ID of the meal you will buy.

### User Interface:

<div align="center">
<img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/search_product.PNG" width="1000" />
</div>

## Buy Product
After decide the meal that you will buy, you're going to buy it from buy product page.
1. Enter the ID of the meal.
2. Enter your adress.
3. Enter your ID no.
4. Enter the CVV of your card.
5. Enter your card number.

### User Interface:

<div align="center">
<img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/buy_product.PNG" width="1000" />
</div>

## See Your Products
As a seller, you can see your products and analysis from this page. Here what should you do:
1. Enter your username.
2. Enter your password.
3. After login, you can see your product and analysis that made for you.

### User Interface:

<div align="center">

 | Login | Analysis |
|---------|---------|
| <img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/see_products_login.PNG" width="300" /> | <img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/see_products_analysis.PNG" width="300" /> |

</div>

## Text Generation
We've added a powerful text generation feature in Sell Product tab of our application. At first, we tried to fine-tune Llama and Gemma models, and actually we did it. But there was an option called Gemini. We did the tests and decided to use gemini-1.5-flash. So we decided to use Gemini API. After hitting the "Submit Product" button, we're sending an API request to Gemini (gemini-1.5-flash) and improve the title-description of the meal.

You can see the example.

### Result:

<div align="center">
<img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/text_generation.PNG" width="1000" />
</div>


# Used System Specifications
- 1 T4-15GB GPU
- 12 GB RAM
>  [!WARNING]  
>  You may experience issues running this on less powerful hardware.

# Models Used

This project makes use of the following models:

1. **gemini-1.5-flash**:
   - **Source:** [DeepMind](https://deepmind.google/technologies/gemini/flash/)
   - **License:** API Used - No License Info
 
2. **ahmeterdempmk/FoodLlaMa-LoRA-Based**:
   - **Source:** [Hugging Face](https://huggingface.co/ahmeterdempmk/Llama-3.1-8B-Fast-Food-Based-Tuned)
   - **License:** Apache 2.0

3. **ahmeterdempmk/Gemma2-2b-E-Commerce-Tuned**:
   - **Source:** [Hugging Face](https://huggingface.co/ahmeterdempmk/Gemma2-2b-E-Commerce-Tuned)
   - **License:** Apache 2.0

4. **ahmeterdempmk/Llama-3.1-8B-Fast-Food-Based-Tuned**:
   - **Source:** [Hugging Face](https://huggingface.co/ahmeterdempmk/Llama-3.1-8B-Fast-Food-Based-Tuned)
   - **License:** Apache 2.0
     
5. **Emir Kaan Özdemir - LSTM Based Time Series Model**:
   - **Source:** [GitHub](https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/User%20Interface/model.h5)
   - **License:** Apache 2.0

> [!NOTE] 
> Please ensure compliance with each model's license when using or distributing this project.

# Contributors

- **[Ahmet Erdem Pamuk](https://github.com/ahmeterdempmk)**
- **[Emir Kaan Özdemir](https://github.com/emirkaanozdemr)**
- **[İlknur Yaren Karakoç](https://github.com/esholmess)**
