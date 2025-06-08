import os
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "default_token")

@app.route('/', methods=['GET'])
def home():
    return "Webhook WhatsApp actif", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'Erreur de vérification', 403

    if request.method == 'POST':
        data = request.get_json()
        print("=== Nouveau message reçu ===")

        try:
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']

            contact = value['contacts'][0]
            message = value['messages'][0]

            name = contact['profile']['name']
            phone = contact['wa_id']
            msg_type = message['type']

            if msg_type == 'text':
                content = message['text']['body']
            else:
                content = f"[Message de type {msg_type} non géré]"

            print(f"👤 Nom       : {name}")
            print(f"📞 Téléphone : {phone}")
            print(f"💬 Message   : {content}")

        except Exception as e:
            print("❌ Erreur lors du traitement du message :", e)
            print("📦 Données reçues :", data)

        return 'Événement reçu', 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
