import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
 
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
 
def authorize_and_save_token():
    if os.path.exists('token.pkl'):
        print("Plik token.pkl już istnieje.")
        return
 
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
 
    with open('token.pkl', 'wb') as token_file:
        pickle.dump(creds, token_file)
    print("Autoryzacja zakończona i token zapisany jako token.pkl.")
 
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()
    print("Twoje etykiety Gmail:")
    for label in results.get('labels', []):
        print("•", label['name'])
 
if __name__ == '__main__':
    authorize_and_save_token()