# to w colab
import json
import random
import math
import os
import glob
import base64
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from pprint import pprint

# --- Dane i model Naiwny Bayes ---

def load_email_data(spam_path, ham_path):
    with open(spam_path, encoding="utf-8") as f1, open(ham_path, encoding="utf-8") as f2:
        return json.load(f1) + json.load(f2)

def train_test_split(data, test_ratio=0.2):
    random.shuffle(data)
    cut = int(len(data) * (1 - test_ratio))
    return data[:cut], data[cut:]

def preprocess(text):
    return text.lower().replace('-', ' ').replace('.', ' ').replace('?', ' ')\
               .replace('!', ' ').replace(',', ' ').split()

def train_nb(train, alpha=1.0):
    class_counts, word_counts, total_words = {}, {}, {}
    for rec in train:
        L = rec["label"]
        class_counts[L] = class_counts.get(L, 0) + 1
        word_counts.setdefault(L, {})
        total_words.setdefault(L, 0)
        for w in preprocess(rec["text"]):
            word_counts[L][w] = word_counts[L].get(w, 0) + 1
            total_words[L] += 1
    vocab = set().union(*[wc.keys() for wc in word_counts.values()])
    return {
        "class_counts": class_counts,
        "word_counts": word_counts,
        "total_words": total_words,
        "vocab": vocab,
        "alpha": alpha,
        "total_docs": len(train)
    }

def log_prob(model, words, cls):
    lp = math.log(model["class_counts"][cls] / model["total_docs"])
    V, a = len(model["vocab"]), model["alpha"]
    for w in words:
        wc = model["word_counts"][cls].get(w, 0)
        lp += math.log((wc + a) / (model["total_words"][cls] + a * V))
    return lp

def predict(model, text):
    ws = preprocess(text)
    best, best_lp = None, -1e99
    for c in model["class_counts"]:
        lp = log_prob(model, ws, c)
        if lp > best_lp:
            best, best_lp = c, lp
    return best

def evaluate_model(model, test):
    acc = sum(predict(model, r["text"]) == r["label"] for r in test) / len(test)
    print(f"Accuracy: {acc*100:.2f}%")
    return acc

# ——————— Gmail + wiele tokenów ———————

def load_all_credentials(pattern="token*.pkl"):
    creds_list = []
    for fn in glob.glob(pattern):
        try:
            with open(fn, 'rb') as f:
                creds = pickle.load(f)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            creds_list.append((fn, creds))
        except Exception as e:
            print(f"[WARN] Nie załadowano {fn}: {e}")
    return creds_list

def build_services(token_pattern="token*.pkl"):
    services = []
    for fn, creds in load_all_credentials(token_pattern):
        try:
            svc = build("gmail", "v1", credentials=creds)
            services.append((fn, svc))
        except Exception as e:
            print(f"[ERROR] Gmail build dla {fn}: {e}")
    return services

def get_label_id(service, name):
    for lb in service.users().labels().list(userId='me').execute().get('labels', []):
        if lb['name'].lower() == name.lower():
            return lb['id']
    return None

def get_message_body(payload):
    if 'parts' in payload:
        for p in payload['parts']:
            if p.get('mimeType') == 'text/plain' and p.get('body', {}).get('data'):
                return base64.urlsafe_b64decode(p['body']['data']).decode('utf-8', 'ignore')
    if payload.get('body', {}).get('data'):
        return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', 'ignore')
    return ""

def fetch_and_relabel(model, label_test="Test", label_spam="spam2", label_ham="ham"):
    services = build_services()
    if not services:
        print("[ERROR] Brak załadowanych tokenów.")
        return

    for fn, svc in services:
        print(f"\n--- Przetwarzam token: {fn} ---")
        lt = get_label_id(svc, label_test)
        ls = get_label_id(svc, label_spam)
        lh = get_label_id(svc, label_ham)
        if not lt:
            print(f" Brak etykiety '{label_test}'")
            continue

        resp = svc.users().messages().list(userId='me',
                                           labelIds=[lt, 'UNREAD'],
                                           maxResults=100).execute()
        for m in resp.get('messages', []):
            msg = svc.users().messages().get(userId='me', id=m['id'], format='full').execute()
            hdrs = msg['payload'].get('headers', [])
            subj = next((h['value'] for h in hdrs if h['name']=='Subject'), "")
            body = get_message_body(msg['payload'])
            txt = f"{subj} {body}"

            pred = predict(model, txt)
            add = ls if pred=='spam' else lh
            svc.users().messages().modify(
                userId='me', id=m['id'],
                body={'addLabelIds':[add], 'removeLabelIds':[lt]}
            ).execute()
            print(f"  {subj[:30]:30} → {pred.upper()}")


def main():
    data = load_email_data("spam.json", "ham.json")
    train, test = train_test_split(data)
    model = train_nb(train)
    evaluate_model(model, test)
    fetch_and_relabel(model)


main()