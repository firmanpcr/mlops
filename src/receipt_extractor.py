import json, os
from pathlib import Path
import lmstudio as lms

IMAGE = Path("data/raw/nota-sample.jpg")
MODEL = os.environ["LM_STUDIO_MODEL"]
image = lms.prepare_image(str(IMAGE))
model = lms.llm(MODEL)
chat = lms.Chat()
chat.add_user_message(
  "Baca nota. Ekstrak merchant, tanggal, item, subtotal, pajak, dan total. "
  "Keluarkan JSON valid. Jika pajak tidak terlihat, isi 0. Jangan mengarang.",
  images=[image],
)
prediction = model.respond(chat)
##result = json.loads(prediction.content)
text = prediction.content
print("RAW OUTPUT:\n", text)

start, end = text.find("{"), text.rfind("}")
result =  json.loads(text[start:end + 1 ])
Path("reports/receipt.json").write_text(
  json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8"
)
print(json.dumps(result, indent=2, ensure_ascii=False))
