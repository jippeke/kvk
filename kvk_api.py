import tkinter as tk
from tkinter import ttk
import requests
import json
from config import API_KEY  # Importeer API key uit config

class KvKAPI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("KVK Zoeker")
        self.root.geometry("800x600")
        
        # API configuratie
        self.api_key = API_KEY
        
              
        # Zoekframe
        search_frame = ttk.LabelFrame(self.root, text="Zoeken", padding="10")
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
        result_frame = ttk.LabelFrame(self.root, text="Resultaten", padding="10")
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Kopieerknop bovenaan
        copy_button = ttk.Button(
            result_frame,
            text="📋 Kopieer naar klembord",
            command=self.kopieer_resultaten,
            style='Accent.TButton'
        )
        copy_button.pack(fill='x', padx=5, pady=5)
        
        # Resultaten tekstveld
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, height=15)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Stijl voor de kopieerknop
        style = ttk.Style()
        style.configure('Accent.TButton', font=('Arial', 11, 'bold'))

    def zoek_bedrijf(self):
        kvk_nummer = self.kvk_entry.get().strip()
        
        if not kvk_nummer:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Vul een KVK nummer in")
            return
            
        url = "https://api.kvk.nl/test/api/v2/zoeken"
        headers = {
            "apikey": self.api_key,
            "Accept": "application/json"
        }
        
        params = {"kvkNummer": kvk_nummer}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            
            # Maak nette weergave van resultaten
            if 'resultaten' in data and data['resultaten']:
                bedrijf = data['resultaten'][0]
                formatted_result = f"""
KVK Nummer: {bedrijf.get('kvkNummer', 'Onbekend')}
Naam: {bedrijf.get('naam', 'Onbekend')}
"""
                if 'adres' in bedrijf and 'binnenlandsAdres' in bedrijf['adres']:
                    adres = bedrijf['adres']['binnenlandsAdres']
                    formatted_result += f"""
Adres:
Straat: {adres.get('straatnaam', '')} {adres.get('huisnummer', '')}
Postcode: {adres.get('postcode', '')}
Plaats: {adres.get('plaats', '')}
"""
                
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, formatted_result)
            else:
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "Geen resultaten gevonden")
                
        except Exception as e:
            self.result_text.delete(1.0, tk.END)
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
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = KvKAPI()
    app.run()