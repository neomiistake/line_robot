from groq import Groq

client = Groq(api_key="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")

available_models = client.models.list()
print("✅ 你的 API Key 可用的模型：")
for model in available_models.data:
    print(model.id)
