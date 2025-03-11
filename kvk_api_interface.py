import tkinter as tk
from tkinter import ttk
import requests
import json
from tkinter import scrolledtext

class KvKZoekApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KVK Zoeker")
        self.root.geometry("800x600")
        
        # API configuratie
        self.api_key = "l7xx1f2691f2520d487b902f4e0b57a0b197"
        
        # Zoek frame
        search_frame = ttk.LabelFrame(root, text="Zoeken", padding="10")
        search_frame.pack(fill="x", padx=10, pady=5)
        
        # KVK nummer invoer
        ttk.Label(search_frame, text="KVK Nummer:").grid(row=0, column=0, padx=5)
        self.kvk_entry = ttk.Entry(search_frame)
        self.kvk_entry.grid(row=0, column=1, padx=5)
        
        # Bedrijfsnaam invoer
        ttk.Label(search_frame, text="Bedrijfsnaam:").grid(row=1, column=0, padx=5)
        self.naam_entry = ttk.Entry(search_frame)
        self.naam_entry.grid(row=1, column=1, padx=5)
        
        # Zoekknop
        ttk.Button(search_frame, text="Zoeken", command=self.zoek_bedrijf).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Resultaten frame
        result_frame = ttk.LabelFrame(root, text="Resultaten", padding="10")
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Resultaten weergave
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, height=20)
        self.result_text.pack(fill="both", expand=True, pady=(0, 10))
        
        # Kopieer knop
        ttk.Button(result_frame, text="Kopieer Resultaten", command=self.kopieer_resultaten).pack(pady=5)

    def format_results(self, data):
        if 'resultaten' not in data or not data['resultaten']:
            return "Geen resultaten gevonden."
            
        bedrijf = data['resultaten'][0]
        formatted = "Bedrijfsinformatie:\n\n"
        formatted += f"KVK Nummer: {bedrijf.get('kvkNummer', 'Onbekend')}\n"
        formatted += f"Naam: {bedrijf.get('naam', 'Onbekend')}\n"
        
        if 'adres' in bedrijf and 'binnenlandsAdres' in bedrijf['adres']:
            adres = bedrijf['adres']['binnenlandsAdres']
            formatted += "\nAdres:\n"
            formatted += f"Straat: {adres.get('straatnaam', '')} {adres.get('huisnummer', '')}\n"
            formatted += f"Postcode: {adres.get('postcode', '')}\n"
            formatted += f"Plaats: {adres.get('plaats', '')}\n"
        
        return formatted

    def zoek_bedrijf(self):
        self.result_text.delete(1.0, tk.END)
        
        kvk_nummer = self.kvk_entry.get().strip()
        naam = self.naam_entry.get().strip()
        
        if not kvk_nummer and not naam:
            self.result_text.insert(tk.END, "Vul een KVK nummer of bedrijfsnaam in.")
            return
            
        url = "https://api.kvk.nl/test/api/v2/zoeken"
        headers = {
            "apikey": self.api_key,
            "Accept": "application/json"
        }
        
        params = {}
        if kvk_nummer:
            params['kvkNummer'] = kvk_nummer
        if naam:
            params['naam'] = naam
            
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            # Toon geformatteerde resultaten
            formatted_results = self.format_results(data)
            self.result_text.insert(tk.END, formatted_results)
            
        except Exception as e:
            self.result_text.insert(tk.END, f"Er is een fout opgetreden: {str(e)}")

    def kopieer_resultaten(self):
        resultaten = self.result_text.get(1.0, tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(resultaten)
        self.root.update()
        
        # Toon tijdelijke bevestiging
        original_text = self.result_text.get(1.0, tk.END)
        self.result_text.insert(tk.END, "\n\nTekst gekopieerd naar klembord!")
        self.root.after(2000, lambda: self.result_text.delete(1.0, tk.END))
        self.root.after(2000, lambda: self.result_text.insert(1.0, original_text))

if __name__ == "__main__":
    root = tk.Tk()
    app = KvKZoekApp(root)
    root.mainloop()