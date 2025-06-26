import streamlit as st
from unsloth import FastLanguageModel
from transformers import BitsAndBytesConfig
import torch

torch.cuda.empty_cache()

@st.cache_resource
def load_model():
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="ahmeterdempmk/FoodLlaMa-LoRA-Based",
        max_seq_length=2048,
        load_in_8bit=True,
        load_in_4bit=False,
        llm_int8_enable_fp32_cpu_offload=True
    )
    
    FastLanguageModel.for_inference(model)
    return model, tokenizer

model, tokenizer = load_model()

torch.cuda.empty_cache()

user = st.text_input('Info:')

if user:
    prompt = f"""
    You are extracting Food title and description from given text and rewriting the description and enhancing it when necessary.
    Always give response in the user's input language.
    Always answer in the given json format. Do not use any other keywords. Do not make up anything.
    The description part must contain at least 5 sentences for each.

    Json Format:
    {{
    "title": "<title of the Food>",
    "description": "<description of the Food>"
    }}
    Examples:
    Food Information: Rosehip Marmalade, keep it cold
    Answer: {{"title": "Rosehip Marmalade", "description": "You should store this delicious rose marmalade in a cold place. It is an excellent flavor used in meals and desserts. Sold in grocery stores. It is in the form of 24 gr / 1 package. You can use this wonderful flavor in your meals and desserts!"}}
    Food Information: Blackberry jam spoils in the heat
    Answer: {{"title": "Blackberry Jam", "description": "Please store in a cold environment. It is recommended to be consumed for breakfast. It is very sweet. It is a traditional flavor and can be found in markets etc. You can also use it in your meals other than breakfast."}}
    Now answer this:
    Food Information: {user}
    """

    inputs = tokenizer([prompt], return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=128)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    answer_start = response.find("Now answer this:") + len("Now answer this:")
    answer = response[answer_start:].strip()

    json_start = answer.find("{")
    json_end = answer.find("}") + 1
    json_response = answer[json_start:json_end].strip()

    import json
    json_data = json.loads(json_response)

    title = json_data["title"]
    description = json_data["description"]

    st.write(title)
    st.write(description)
