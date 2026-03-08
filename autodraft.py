import win32com.client
import pythoncom
import time
import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("NVIDIA_API_KEY")

def run_agent():
    """Main loop with auto-restart logic and clean body drafting"""
    print("---")
    print("🚀 AI EMAIL AGENT IS STARTING...")
    print("User: Sandeep Sai Kumar K I")
    print("📍 Monitoring for clean drafts only.")
    print("---")

    while True:
        try:
            pythoncom.CoInitialize()
            
            client = OpenAI(base_url="https://integrate.api.nvidia.com/v1", api_key=API_KEY)
            outlook = win32com.client.Dispatch("Outlook.Application")
            namespace = outlook.GetNamespace("MAPI")
            inbox = namespace.GetDefaultFolder(6)

            print("📡 Monitoring active... (Checking every 30s)")
            
            while True:
                unread_items = inbox.Items.Restrict("[UnRead] = True")
                count = unread_items.Count
                
                if count > 0:
                    for i in range(count, 0, -1):
                        msg = unread_items.Item(i)
                        print(f"📧 New Mail: {msg.Subject}")
                        
                        # UPDATED SYSTEM PROMPT: Strict instructions to avoid headers
                        system_msg = (
                            "You are a professional assistant. Write ONLY the message body. "
                            "Do NOT include 'Subject:', 'Re:', or 'Dear Support Team' as a header. "
                            "Start directly with the salutation and the message."
                        )

                        completion = client.chat.completions.create(
                            model="qwen/qwen2.5-coder-7b-instruct",
                            messages=[
                                {"role": "system", "content": system_msg},
                                {"role": "user", "content": f"Draft a professional reply to this email content: {msg.Body}"}
                            ],
                            temperature=0.3
                        )
                        
                        ai_reply = completion.choices[0].message.content

                        # PYTHON CLEANER: Remove any accidental Subject lines the AI still adds
                        lines = ai_reply.split('\n')
                        clean_lines = [line for line in lines if not line.lower().startswith(("subject:", "re:", "to:", "from:"))]
                        clean_reply = "\n".join(clean_lines).strip()
                        
                        # Create Draft
                        new_mail = outlook.CreateItem(0)
                        new_mail.To = msg.SenderEmailAddress
                        new_mail.Subject = f"Re: {msg.Subject}"
                        new_mail.Body = clean_reply
                        new_mail.Display()
                        
                        msg.UnRead = False # Mark as read
                
                time.sleep(30)
                
        except Exception as e:
            print(f"⚠️ Connection dropped or Error: {e}")
            print("🔄 Attempting to reconnect in 10 seconds...")
            time.sleep(10)
        finally:
            pythoncom.CoUninitialize()

if __name__ == "__main__":
    if not API_KEY:
        print("❌ Missing API Key!")
    else:
        try:
            run_agent()
        except KeyboardInterrupt:
            print("\n🛑 Agent stopped by user.")