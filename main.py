"""
QR Code Generator
A simple desktop application that turns a website URL into a QR code.
Run: python main.py
"""

import re
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from urllib.parse import urlparse

import qrcode
from PIL import Image, ImageTk


APP_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = APP_DIR / "generated_qrcodes"
OUTPUT_DIR.mkdir(exist_ok=True)


def normalize_and_validate_url(value: str) -> str | None:
    """Validate a URL and add https:// when the user omits a scheme."""
    value = value.strip()
    if not value:
        return None

    if not re.match(r"^https?://", value, flags=re.IGNORECASE):
        value = "https://" + value

    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        return None
    if "." not in parsed.netloc and parsed.netloc.lower() != "localhost":
        return None
    if any(char.isspace() for char in value):
        return None

    return value


class QRCodeGeneratorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("650x690")
        self.root.minsize(560, 620)
        self.root.configure(bg="#f3f6fb")

        self.current_image = None
        self.current_photo = None
        self.current_url = ""

        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#172554", padx=24, pady=22)
        header.pack(fill="x")

        tk.Label(
            header, text="QR Code Generator",
            font=("Segoe UI", 22, "bold"),
            fg="white", bg="#172554"
        ).pack(anchor="w")

        tk.Label(
            header, text="Turn any website link into a scannable QR code.",
            font=("Segoe UI", 10), fg="#dbeafe", bg="#172554"
        ).pack(anchor="w", pady=(5, 0))

        body = tk.Frame(self.root, bg="#f3f6fb", padx=26, pady=22)
        body.pack(fill="both", expand=True)

        tk.Label(
            body, text="Website URL",
            font=("Segoe UI", 11, "bold"), fg="#172554", bg="#f3f6fb"
        ).pack(anchor="w")

        self.url_entry = tk.Entry(
            body, font=("Segoe UI", 12), relief="solid", bd=1
        )
        self.url_entry.pack(fill="x", ipady=10, pady=(7, 12))
        self.url_entry.insert(0, "https://www.example.com")
        self.url_entry.bind("<Return>", lambda _event: self.generate_qr())

        button_row = tk.Frame(body, bg="#f3f6fb")
        button_row.pack(fill="x")

        tk.Button(
            button_row, text="Generate QR Code",
            command=self.generate_qr, font=("Segoe UI", 10, "bold"),
            bg="#2563eb", fg="white", activebackground="#1d4ed8",
            activeforeground="white", relief="flat", padx=16, pady=10,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            button_row, text="Save QR Code",
            command=self.save_qr, font=("Segoe UI", 10, "bold"),
            bg="#0f766e", fg="white", activebackground="#115e59",
            activeforeground="white", relief="flat", padx=16, pady=10,
            cursor="hand2"
        ).pack(side="left", padx=(10, 0))

        self.preview = tk.Label(
            body, text="Your QR code will appear here",
            font=("Segoe UI", 11), fg="#64748b", bg="white",
            width=34, height=15, relief="solid", bd=1
        )
        self.preview.pack(pady=22, ipadx=12, ipady=12)

        self.status = tk.Label(
            body, text="Enter a website URL to get started.",
            font=("Segoe UI", 9), fg="#475569", bg="#f3f6fb",
            wraplength=540, justify="left"
        )
        self.status.pack(anchor="w")

        tk.Label(
            body,
            text="Tip: QR codes store the link you enter. Scan only links you trust.",
            font=("Segoe UI", 9), fg="#64748b", bg="#f3f6fb",
            wraplength=540, justify="left"
        ).pack(anchor="w", pady=(15, 0))

    def generate_qr(self):
        url = normalize_and_validate_url(self.url_entry.get())
        if not url:
            messagebox.showerror(
                "Invalid URL",
                "Enter a valid website address, such as https://www.google.com."
            )
            return

        try:
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_M,
                box_size=10,
                border=4,
            )
            qr.add_data(url)
            qr.make(fit=True)
            image = qr.make_image(fill_color="black", back_color="white").convert("RGB")

            self.current_image = image
            self.current_url = url
            preview_image = image.copy()
            preview_image.thumbnail((270, 270))
            self.current_photo = ImageTk.PhotoImage(preview_image)
            self.preview.configure(image=self.current_photo, text="", width=270, height=270)
            self.status.configure(text=f"QR code generated for: {url}", fg="#166534")
        except Exception as exc:
            messagebox.showerror("Generation Error", f"Could not generate the QR code.\n\n{exc}")

    def save_qr(self):
        if self.current_image is None:
            messagebox.showinfo("No QR Code", "Generate a QR code before saving it.")
            return

        default_name = "website_qrcode.png"
        path = filedialog.asksaveasfilename(
            title="Save QR Code",
            initialdir=str(OUTPUT_DIR),
            initialfile=default_name,
            defaultextension=".png",
            filetypes=[("PNG image", "*.png"), ("JPEG image", "*.jpg"), ("All files", "*.*")]
        )
        if not path:
            return

        try:
            self.current_image.save(path)
            self.status.configure(text=f"QR code saved to: {path}", fg="#166534")
            messagebox.showinfo("Saved", f"QR code saved successfully:\n{path}")
        except Exception as exc:
            messagebox.showerror("Save Error", f"Could not save the image.\n\n{exc}")


def main():
    root = tk.Tk()
    QRCodeGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
