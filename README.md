<h1>ServeSmart</h1>

# Competition Scope
Our purpose in this competition to develop an AI project for sustainable cities and green tomorrows.

# Presentation 
You can view the presentation [here]().

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

## Sell Product
Our Streamlit application contains three tabs. The first tab is for product selling (adding). The instructions to add product:
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
The second tab provides a search product feature. Here’s how it works:
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

### Result:

<div align="center">
<img src="https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/Assets/buy_product.PNG" width="1000" />
</div>

## Text Generation
We've added a powerful text generation feature in Sell Product tab of our application. After hitting the "Submit Product" button, we're sending an API request to Gemini (gemini-1.5-flash) and improve the title-description of the meal.

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

1. **ahmeterdempmk/FoodLlaMa-LoRA-Based**:
   - **Source:** [Hugging Face](https://huggingface.co/ahmeterdempmk/Llama-3.1-8B-Fast-Food-Based-Tuned)
   - **License:** Apache 2.0

2. **ahmeterdempmk/Gemma2-2b-E-Commerce-Tuned**:
   - **Source:** [Hugging Face](https://huggingface.co/ahmeterdempmk/Gemma2-2b-E-Commerce-Tuned)
   - **License:** Apache 2.0

3. **ahmeterdempmk/Llama-3.1-8B-Fast-Food-Based-Tuned**:
   - **Source:** [Hugging Face](https://huggingface.co/ahmeterdempmk/Llama-3.1-8B-Fast-Food-Based-Tuned)
   - **License:** Apache 2.0
     
4. **Emir Kaan Özdemir - LSTM Based Time Series Model**:
   - **Source:** [GitHub](https://github.com/Lyra-AI-Team/Yarinin-Sehirleri-Hackathon/blob/main/User%20Interface/model.h5)
   - **License:** Apache 2.0

> [!NOTE] 
> Please ensure compliance with each model's license when using or distributing this project.

# Contributors

- **[Ahmet Erdem Pamuk](https://github.com/ahmeterdempmk)**
- **[Emir Kaan Özdemir](https://github.com/emirkaanozdemr)**
- **[İlknur Yaren Karakoç](https://github.com/esholmess)**
