import argparse
import requests
from pyzbar.pyzbar import decode
from PIL import Image

API_URL = "http://localhost:8000"
API_KEY = "T9f$K2wQ"
headers = {
    "X-API-KEY": API_KEY
}

def save_qr(logo_path: str):
    files = {
        "file": (logo_path, open(logo_path, "rb"), "image/png")
    }
    response = requests.post(f"{API_URL}/save", files=files, headers=headers)
    print("Status:", response.status_code)
    print("Response:", response.json())

def create_qr(url: str, name: str = None):
    data = {
        "url": url,
        "logoname": name
    }
    response = requests.post(f"{API_URL}/create", json=data, headers=headers)
    print("Status:", response.status_code)
    if response.status_code == 200:
        with open("qr_created.png", "wb") as f:
            f.write(response.content)
        print("QR code created and saved as qr_created.png")
    else:
        print("Error:", response.text)

def qr_scan(image_path: str):
    # open the image file
    image = Image.open(image_path)

    # decode the QR code
    decoded = decode(image)

    if not decoded:
        print("No QR code found in the image.")
        return

    qr_text = decoded[0].data.decode("utf-8")
    
    qr_id = qr_text.rstrip("/").split("/")[-1]
    
    response = requests.get(f"{API_URL}/scam/{qr_id}", allow_redirects=False)

    if response.status_code in (301, 302, 307):
        redirect_url = response.headers.get("location")

        print("✅ Valid QR code")
        print("🔗 Redirects to:")
        print(redirect_url)
    elif response.status_code == 404:
        print("❌ QR not found in the system")
    else:
        print("⚠️ Unexpected response")
        print("Status:", response.status_code)

def main():
    parser = argparse.ArgumentParser(
        description="CLI Tool for creating and scanning QRs"
    )

    subparsers = parser.add_subparsers(dest="command")

    # This is for the create command
    save_parser = subparsers.add_parser("save", help="Save Qr")

    save_parser.add_argument(
        "--logo",
        required=True,
        help="Path to the logo image to embed in the QR code"
    )

    create_parser = subparsers.add_parser("create", help="Create Qr")

    create_parser.add_argument(
        "--url",
        required=True,
        help="URL to encode in the QR code"
    )

    create_parser.add_argument(
        "--name",
        required=None,
        help="Name of the QR code file to create"
    )

    scan_parser = subparsers.add_parser("scan", help="Scan Qr")

    scan_parser.add_argument(
        "--image",
        required=True,
        help="Path to the image file containing the QR code to scan"
    )

    args = parser.parse_args()

    if args.command == "save":
        save_qr(args.logo)
    elif args.command == "create":
        create_qr(args.url, args.name)
    elif args.command == "scan":
        qr_scan(args.image)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()