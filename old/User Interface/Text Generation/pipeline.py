model, tokenizer = FastLanguageModel.from_pretrained(
  model_name="ahmeterdempmk/FoodLlaMa-LoRA-Based",
  max_seq_length=2048,
  load_in_8bit=True,
  load_in_4bit=False,
  llm_int8_enable_fp32_cpu_offload=True
)
