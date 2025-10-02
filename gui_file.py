import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

try:
    from model_classes import TextClassifierModel, ImageClassifierModel
    got_models = True
except:
    got_models = False
    print("cant find model file")

class MyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WTH")
        self.root.geometry("850x700")
        
        #variables needed
        self.current_model = None
        self.text_model = None
        self.image_model = None
        self.image_file = ""
        
        self.setup_ui()
        print("app ready")
    
    def setup_ui(self):
        #main title
        title = tk.Label(self.root, text="What The Hell", font=("Arial", 14))
        title.pack(pady=10)

        #main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        #controls
        left_side = tk.Frame(main_frame)
        left_side.pack(side="left", fill="both", expand=True, padx=5)
        
        #info
        right_side = tk.Frame(main_frame)
        right_side.pack(side="right", fill="both", expand=True, padx=5)

        # model selection
        model_frame = tk.LabelFrame(left_side, text=" Choose Model", padx=10, pady=10)
        model_frame.pack(fill="x", pady=5)
        self.model_type = tk.StringVar(value="none")
        
        tk.Radiobutton(model_frame, text="Text Classification", 
                      variable=self.model_type, value="text").pack(anchor="w", pady=2)
        tk.Radiobutton(model_frame, text="Image Classification", 
                      variable=self.model_type, value="image").pack(anchor="w", pady=2)
        
        #buttons
        btn_frame = tk.Frame(model_frame)
        btn_frame.pack(pady=8)
        
        tk.Button(btn_frame, text="Load Model", command=self.load_model, 
                 bg="lightgreen", width=12).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Run Model", command=self.run_model,
                 bg="lightblue", width=12).pack(side="left", padx=4)
        
        self.status_text = tk.Label(model_frame, text="No model loaded", fg="red")
        self.status_text.pack()
        
        input_frame = tk.LabelFrame(left_side, text=" Input Data", padx=10, pady=10)
        input_frame.pack(fill="x", pady=5)
        
        #text input
        tk.Label(input_frame, text="Text to classify:").pack(anchor="w")
        self.text_box = tk.Text(input_frame, height=4, width=65)
        self.text_box.pack(pady=5)
        self.text_box.insert("1.0", "")
        
        tk.Label(input_frame, text="Categories (separate with commas):").pack(anchor="w")
        self.categories_entry = tk.Entry(input_frame, width=65)
        self.categories_entry.pack(pady=5)
        self.categories_entry.insert(0, "")
        
        #image input
        tk.Label(input_frame, text="Or choose image file:").pack(anchor="w", pady=(10,0))
        img_frame = tk.Frame(input_frame)
        img_frame.pack(fill="x", pady=5)
        
        tk.Button(img_frame, text="Browse Image", command=self.pick_image).pack(side="left")
        self.image_label = tk.Label(img_frame, text="no image selected", fg="gray")
        self.image_label.pack(side="left", padx=10)
        
        #output area
        output_frame = tk.LabelFrame(left_side, text=" Results", padx=10, pady=10)
        output_frame.pack(fill="both", expand=True, pady=5)
        
        self.output_display = tk.Text(output_frame, height=12, width=65)
        self.output_display.pack(fill="both", expand=True, padx=5, pady=5)
        
        #output scrollbar
        scroll = tk.Scrollbar(self.output_display)
        scroll.pack(side="right", fill="y")
        self.output_display.config(yscrollcommand=scroll.set)
        scroll.config(command=self.output_display.yview)
        self.output_display.insert("1.0", "")
        
        #side notebook
        notebook = ttk.Notebook(right_side)
        notebook.pack(fill="both", expand=True)
        
        #model info tab
        tab1 = tk.Frame(notebook)
        notebook.add(tab1, text="Model Info")
        
        model_info = """Models We're Using:

Text Model:
- facebook/bart-large-mnli
- Zero-shot text classification
- You provide text and categories
- It finds the best match

Image Model:
- google/vit-base-patch16-224
- Image classification
- You provide an image
- It identifies what's in it"""
        
        info_text = tk.Text(tab1, wrap="word", height=20, width=35)
        info_text.pack(fill="both", expand=True, padx=10, pady=10)
        info_text.insert("1.0", model_info)
        info_text.config(state="disabled")
        
        #oop concepts tab
        tab2 = tk.Frame(notebook)
        notebook.add(tab2, text="OOP Concepts")
        oop_info = """Object Oriented Programming
concepts in this app:

CLASSES:
- MyApp (main application)
- TextClassifierModel
- ImageClassifierModel 

ENCAPSULATION:
- Using self.variables to store state
- Methods to control what happens
- Keeping things organized

METHODS:
- load_model()
- run_model() 
- pick_image()
- setup_ui()

GUI:
- Frames for organization
- Buttons with commands
- Text areas for input/output
- Labels for information

FILE ORGANIZATION:
- main.py (starter)
- gui_file (gui design)
- model_classes.py (models)"""
        
        oop_text = tk.Text(tab2, wrap="word", height=20, width=35)
        oop_text.pack(fill="both", expand=True, padx=10, pady=10)
        oop_text.insert("1.0", oop_info)
        oop_text.config(state="disabled")
        
        #help tab
        tab3 = tk.Frame(notebook)
        notebook.add(tab3, text="Help")
        
        usage_info = """How to use this app:

1. SELECT MODEL TYPE
   - Pick text or image

2. LOAD THE MODEL
   - Click Load Model button
   - Wait for it to load

3. PROVIDE INPUT
   For text:
   - Type some text
   - Enter categories
   
   For image:
   - Click Browse Image
   - Select a picture

4. RUN THE MODEL
   - Click Run Model
   - See the results"""
        
        usage_text = tk.Text(tab3, wrap="word", height=20, width=35)
        usage_text.pack(fill="both", expand=True, padx=10, pady=10)
        usage_text.insert("1.0", usage_info)
        usage_text.config(state="disabled")
    
    def load_model(self):
        if not got_models:
            messagebox.showerror("Error", "Can't find the model file!")
            return
        
        which_model = self.model_type.get()
        
        try:
            if which_model == "text":
                if self.text_model is None:
                    self.text_model = TextClassifierModel()
                self.current_model = self.text_model
                name = "Text Model"
            else:
                if self.image_model is None:
                    self.image_model = ImageClassifierModel()
                self.current_model = self.image_model
                name = "Image Model"
            
            self.status_text.config(text=f"Loaded: {name}", fg="green")
            messagebox.showinfo("Done", f"{name} is ready!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Problem: {e}")
            self.status_text.config(text="Load failed", fg="red")
    
    def pick_image(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Images", "*.jpg *.jpeg *.png")]
        )
        if filepath:
            self.image_file = filepath
            filename = os.path.basename(filepath)
            self.image_label.config(text=filename)
    
    def run_model(self):
        if self.current_model is None:
            messagebox.showwarning( "Load a model first!")
            return
        
        #loading
        self.output_display.delete("1.0", tk.END)
        self.output_display.insert("1.0", "processing... please wait")
        self.root.update()
        
        try:
            model_kind = self.model_type.get()
            
            if model_kind == "text":
                #get inputs
                text = self.text_box.get("1.0", "end-1c").strip()
                cats_text = self.categories_entry.get().strip()
                
                if not text:
                    messagebox.showwarning( "Need some text!")
                    return
                
                if not cats_text:
                    messagebox.showwarning( "Need some categories!")
                    return
                
                #make category list
                categories = [c.strip() for c in cats_text.split(",") if c.strip()]
                
                #run model
                result = self.current_model.classify(text, categories)
                
                #show output
                if 'error' in result:
                    output = f"Error: {result['error']}"
                else:
                    output = f"TEXT: {text}\n\n"
                    output += f"CATEGORIES: {', '.join(categories)}\n\n"
                    output += f"BEST MATCH: {result['label']}\n"
                    output += f"CONFIDENCE: {result['score']}%"
                
            else:  #image model
                if not self.image_file:
                    messagebox.showwarning( "Choose an image first!")
                    return
                
                #run image model
                result = self.current_model.classify(self.image_file)
                
                if 'error' in result:
                    output = f"Error: {result['error']}"
                else:
                    output = f"IMAGE: {os.path.basename(self.image_file)}\n\n"
                    output += f"PREDICTION: {result['label']}\n"
                    output += f"CONFIDENCE: {result['score']}%"
            
            #display results
            self.output_display.delete("1.0", tk.END)
            self.output_display.insert("1.0", output)
            
        except Exception as e:
            error_msg = f"Something went wrong:\n{str(e)}"
            self.output_display.delete("1.0", tk.END)
            self.output_display.insert("1.0", error_msg)
            print(f"error: {e}")
    
    def run_app(self):
        self.root.mainloop()
#run the app
if __name__ == "__main__":
    app = MyApp()
    app.run_app()