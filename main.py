from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed

set_seed(42)

checkpoint = "HuggingFaceTB/SmolLM-135M"
device = "cpu"

tokenizer = AutoTokenizer.from_pretrained(checkpoint)
model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)

inputs = tokenizer.encode("What is the moon", return_tensors="pt").to(device)

outputs = model.generate(
    inputs,
    max_new_tokens=100,
    max_length=150,  # You can adjust this as needed
    no_repeat_ngram_size=2,  # Prevents repeating n-grams of this size
    early_stopping=True,
)

result = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(f"===result ======> {result}===")

assert result == """What is the moon?
The moon is a natural satellite of the Earth. It is also called the satellite or the minor planet. The moon has a diameter of about 2,300 km (1,435 mi) and is about the same size as the planet Mercury.
What are the 4 types of moons?"""
