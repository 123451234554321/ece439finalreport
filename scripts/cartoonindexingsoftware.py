import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from datetime import datetime

class IndexingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cartoon Indexing App")

        # data storgae icin
        self.df = pd.DataFrame(columns=[
            'Timestamp', 'Start Time', 'End Time', 'Emotional Intensity',
            'Emotional Theme', 'Emotional Complexity', 'Behavioral Impact'
        ])
        self.data = []

        # gui kisimlari ayarlamaya baslamak icin
        self._setup_widgets()

    def _setup_widgets(self):
        # dropdown secenekler
        self._create_dropdown('Emotional Intensity', ['Low', 'Medium', 'High'], 0)
        self._create_dropdown('Emotional Theme', ['Confusion', 'Anger', 'Fear', 'Sadness', 'Happiness', 'Excitement'], 1)
        self._create_dropdown('Emotional Complexity', ['Simple', 'Complex'], 2)
        self._create_dropdown('Behavioral Impact', ['Empathy', 'Aggression', 'Insecurity', 'Cooperation', 'Defiance', 'Indifference', 'Kindness', 'Gratitude', 'Jealousy'], 3)

        # frame zamanlaması
        self._create_label_entry('Start Time', 4)
        self._create_label_entry('End Time', 5)

        # data submit ve excel butonu
        self.submit_button = tk.Button(self.root, text="Submit", command=self._submit_data)
        self.submit_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))

        self.calculate_button = tk.Button(self.root, text="Calculate", command=self._calculate_scores)
        self.calculate_button.grid(row=7, column=0, columnspan=2)

        self.save_button = tk.Button(self.root, text="Save to Excel", command=self._save_to_excel)
        self.save_button.grid(row=8, column=0, columnspan=2)

        # kaydedildi yazisi icin
        self.data_display = tk.Text(self.root, height=10, width=100)
        self.data_display.grid(row=9, column=0, columnspan=2)

    def _create_label_entry(self, label_text, row):
        label = tk.Label(self.root, text=label_text)
        label.grid(row=row, column=0, padx=10, pady=5, sticky='w')
        entry = tk.Entry(self.root)
        entry.grid(row=row, column=1, padx=10, pady=5, sticky='w')
        setattr(self, f"{label_text.lower().replace(' ', '_')}_entry", entry)

    def _create_dropdown(self, label_text, options, row):
        label = tk.Label(self.root, text=label_text)
        label.grid(row=row, column=0, padx=10, pady=5, sticky='w')
        dropdown = ttk.Combobox(self.root, values=options)
        dropdown.grid(row=row, column=1, padx=10, pady=5, sticky='w')
        setattr(self, f"{label_text.lower().replace(' ', '_')}_dropdown", dropdown)

    def _submit_data(self):
        # guiye girilen datanin data olarak taninması
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()

        # datanin aslen storagei
        data = {
            'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Start Time': start_time,
            'End Time': end_time,
            'Emotional Intensity': self.emotional_intensity_dropdown.get(),
            'Emotional Theme': self.emotional_theme_dropdown.get(),
            'Emotional Complexity': self.emotional_complexity_dropdown.get(),
            'Behavioral Impact': self.behavioral_impact_dropdown.get()
        }

        # datalarin eklenmesi
        self.data.append(data)

        # submit edildikten sonra input yapilan yerlerin temizlenmesi
        self._clear_inputs()

        # en guncel halini gostermesi
        self._update_display()

    def _clear_inputs(self):
        # her seyin temizlenmesi
        self.start_time_entry.delete(0, tk.END)
        self.end_time_entry.delete(0, tk.END)
        self.emotional_intensity_dropdown.set('')
        self.emotional_theme_dropdown.set('')
        self.emotional_complexity_dropdown.set('')
        self.behavioral_impact_dropdown.set('')

    def _update_display(self):
        # datanin gösterilmesi
        self.data_display.delete(1.0, tk.END)
        df = pd.DataFrame(self.data)
        self.data_display.insert(tk.END, df.to_string(index=False))

    def _calculate_scores(self):
        # skor semasi
        pos_scores = {'Happiness': 2, 'Excitement': 2, 'Empathy': 2, 'Gratitude': 2, 'Kindness': 1, 'Cooperation': 1}
        neg_scores = {'Anger': -3, 'Aggression': -3, 'Fear': -3, 'Sadness': -2, 'Insecurity': -3, 'Defiance': -3, 'Jealousy': -3}
        intensity_scores = {'Low': 1, 'Medium': 2, 'High': 3}
        complexity_scores = {'Simple': 1, 'Complex': 2}
        
        weight_factors = {
            'Emotional Intensity': 0.35,
            'Emotional Theme': 0.30,
            'Behavioral Impact': 0.25,
            'Emotional Complexity': 0.10
        }

        # basta olusturdugumuz dataframe objesine datanin cevrilmesi
        df = pd.DataFrame(self.data)

        # arkaplanda bir düzenleme, skorlarin dataframe objesine haritalanarak gosterilmesi
        df['Intensity Score'] = df['Emotional Intensity'].map(intensity_scores)
        df['Theme Score'] = df['Emotional Theme'].apply(lambda x: pos_scores.get(x, neg_scores.get(x, 0)))
        df['Complexity Score'] = df['Emotional Complexity'].map(complexity_scores)
        df['Behavioral Impact Score'] = df['Behavioral Impact'].apply(lambda x: pos_scores.get(x, neg_scores.get(x, 0)))

        # intensity ve complexe gore degisen skorlarin adjusti
        df['Adj. Theme Score'] = df.apply(lambda row: row['Theme Score'] * (row['Intensity Score'] + row['Complexity Score']), axis=1)
        df['Adj. Impact Score'] = df.apply(lambda row: row['Behavioral Impact Score'] * (row['Intensity Score'] + row['Complexity Score']), axis=1)

        # total weighted skor hesabı
        df['Total Weighted Score'] = (
            df['Intensity Score'] * weight_factors['Emotional Intensity'] +
            df['Adj. Theme Score'] * weight_factors['Emotional Theme'] +
            df['Complexity Score'] * weight_factors['Emotional Complexity'] +
            df['Adj. Impact Score'] * weight_factors['Behavioral Impact']
        )

        self._show_results_popup(df)

    def _show_results_popup(self, df):
        # popup sonuc ekrani
        popup = tk.Toplevel(self.root)
        popup.title("Calculation Results")

        text = tk.Text(popup, height=20, width=80)
        text.pack(padx=10, pady=10)

        # total ve averaj skor
        total_score = df['Total Weighted Score'].sum()
        avg_score = df['Total Weighted Score'].mean()
        summary = (
            f"Total Score: {total_score:.2f}\n"
            f"Average Score: {avg_score:.2f}\n\n"
            f"{df.to_string(index=False)}"
        )
        text.insert(tk.END, summary)

        close_button = tk.Button(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=10)

    def _save_to_excel(self):
        # excele kaydet
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")])
        
        if file_path:
            df = pd.DataFrame(self.data)

            # tekrar haritala excel icin
            df['Intensity Score'] = df['Emotional Intensity'].map({'Low': 1, 'Medium': 2, 'High': 3})
            df['Theme Score'] = df['Emotional Theme'].apply(lambda x: {
                'Happiness': 2, 'Excitement': 2, 'Empathy': 2, 'Gratitude': 2,
                'Kindness': 1, 'Cooperation': 1
            }.get(x, {
                'Anger': -3, 'Aggression': -3, 'Fear': -3, 'Sadness': -2,
                'Insecurity': -3, 'Defiance': -3, 'Jealousy': -3
            }.get(x, 0)))
            df['Complexity Score'] = df['Emotional Complexity'].map({'Simple': 1, 'Complex': 2})
            df['Behavioral Impact Score'] = df['Behavioral Impact'].apply(lambda x: {
                'Empathy': 2, 'Kindness': 1, 'Cooperation': 1, 'Gratitude': 2,
                'Aggression': -3, 'Insecurity': -3, 'Defiance': -3, 'Jealousy': -3,
                'Indifference': 0
            }.get(x, 0))

            df['Adj. Theme Score'] = df.apply(lambda row: row['Theme Score'] * (row['Intensity Score'] + row['Complexity Score']), axis=1)
            df['Adj. Impact Score'] = df.apply(lambda row: row['Behavioral Impact Score'] * (row['Intensity Score'] + row['Complexity Score']), axis=1)

            df['Total Weighted Score'] = (
                df['Intensity Score'] * 0.35 +
                df['Adj. Theme Score'] * 0.30 +
                df['Complexity Score'] * 0.10 +
                df['Adj. Impact Score'] * 0.25
            )

            with pd.ExcelWriter(file_path) as writer:
                df.to_excel(writer, index=False, sheet_name='Cartoon Indexing')

            messagebox.showinfo("Save to Excel", "Data saved successfully.")

# tum bunlarin birlesimi, calistirmaya yarayan kod
root = tk.Tk()
app = IndexingApp(root)
root.mainloop()
