import torch
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from transformers import (AutoConfig, AutoModelForSequenceClassification, AutoTokenizer, GPT2LMHeadModel, GPT2Tokenizer)
from kafka import KafkaProducer, KafkaConsumer

label2id= {
    "negative":0,
    "positive":1,
}
id2label= {
    0:"negative",
    1:"positive",
}
config = AutoConfig.from_pretrained("./checkpoint-125000", label2id=label2id, id2label=id2label)
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tokenizer = AutoTokenizer.from_pretrained("./checkpoint-125000")
model = GPT2LMHeadModel.from_pretrained("./checkpoint-125000",config=config).to(DEVICE)

producer_tosend = KafkaProducer(bootstrap_servers='localhost:9092')
consumer_toget = KafkaConsumer('quickstart-events2',bootstrap_servers='localhost:9092')
for msg in consumer_toget:
    print(msg)
    print(msg.key.decode("utf-8") )
    s = msg.key.decode("utf-8")
    if (s  == '123'):
        print("Im HERE/n\n\n")
        text2 = '[SJ] - ' + msg.value.decode("utf-8")
        print(text2)
        input_ids = tokenizer.encode(text2, return_tensors="pt").to(DEVICE)
        model.eval()
        with torch.no_grad():
            out = model.generate(input_ids, 
                            do_sample=True,
                            num_beams=2,
                            temperature=1.5,
                            top_p=0.9,
                            max_length=100, pad_token_id=tokenizer.eos_token_id,
                            )
        generated_text = list(map(tokenizer.decode, out))[0]
        print (generated_text)
        generated_text = generated_text.replace('[SJ]', '').split("[")[0]
        key_bytes = bytes('333', encoding='utf-8') 
        value_bytes = bytes(generated_text, encoding='utf-8') 
        producer_tosend.send('quickstart-events1', key=key_bytes, value=value_bytes) 
        producer_tosend.flush()