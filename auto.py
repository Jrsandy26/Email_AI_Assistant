import win32com.client
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=os.getenv("NVIDIA_API_KEY"))

def create_clean_outlook_draft():
    # 1. Access Outlook
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")
    inbox = namespace.GetDefaultFolder(6)
    
    # 2. Get the latest message to reply to
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)
    last_message = messages.GetFirst()
    
    # Extract details for the AI
    sender_email = last_message.SenderEmailAddress
    subject = last_message.Subject
    body_content = last_message.Body

    # 3. Generate ONLY the reply text via NVIDIA
    prompt = f"Write a professional reply to this email. Provide ONLY the reply body text. \nEmail: {body_content}"
    
    completion = client.chat.completions.create(
        model="qwen/qwen2.5-coder-7b-instruct",
        messages=[{"role": "system", "content": "You are a professional assistant. Do not include signatures or 'Re:' lines. Just the message body."},
                  {"role": "user", "content": prompt}],
        temperature=0.3
    )
    ai_reply = completion.choices[0].message.content

    # 4. Create a BRAND NEW mail item (Clean)
    # Instead of last_message.Reply(), we use outlook.CreateItem(0)
    new_mail = outlook.CreateItem(0) 
    new_mail.To = sender_email
    new_mail.Subject = f"Re: {subject}"
    new_mail.Body = ai_reply  # This will now contain ONLY the AI text
    
    # 5. Show it on screen
    new_mail.Display()

if __name__ == "__main__":
    create_clean_outlook_draft()