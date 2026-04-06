"""
Email alert sender using Gmail SMTP.
Configure credentials in config.json → email section.
"""

import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def load_smtp_config() -> dict:
    with open("config.json", "r") as f:
        return json.load(f)["email"]


def send_alert(to: str, title: str, price: float, currency: str, url: str, reason: str):
    cfg = load_smtp_config()

    subject = f"🔔 ML Price Alert: {title[:50]}"

    html = f"""
    <html><body style="font-family: Arial, sans-serif; padding: 20px; color: #333;">
      <h2 style="color: #FFE600; background: #333; padding: 12px 16px; border-radius: 6px;">
        🛒 MercadoLibre Price Alert
      </h2>
      <p><strong>Product:</strong> {title}</p>
      <p><strong>Current Price:</strong>
        <span style="font-size: 1.4em; color: #009EE3;">
          {currency} {price:,.2f}
        </span>
      </p>
      <p><strong>Reason:</strong><br>
        <span style="color: #e74c3c;">{reason.replace(chr(10), "<br>")}</span>
      </p>
      <a href="{url}"
         style="display:inline-block; margin-top:12px; padding: 10px 20px;
                background:#009EE3; color:#fff; text-decoration:none; border-radius:4px;">
        View on MercadoLibre →
      </a>
      <p style="margin-top:24px; font-size:0.8em; color:#999;">
        Sent by ml-price-tracker · <a href="https://github.com/Lazaro549">github.com/Lazaro549</a>
      </p>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = cfg["from"]
    msg["To"] = to
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(cfg["from"], cfg["app_password"])
            server.sendmail(cfg["from"], to, msg.as_string())
        print(f"  ✉  Alert sent to {to}")
    except smtplib.SMTPException as e:
        print(f"  [ERROR] Failed to send email: {e}")
