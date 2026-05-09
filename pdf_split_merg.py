import os
import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfReader, PdfWriter


def add_merge_files():
    files = filedialog.askopenfilenames(
        title="Select PDF files to merge",
        filetypes=[("PDF files", "*.pdf")],
    )
    for path in files:
        if path and path not in merge_listbox.get(0, tk.END):
            merge_listbox.insert(tk.END, path)


def remove_merge_file():
    selected = merge_listbox.curselection()
    for index in reversed(selected):
        merge_listbox.delete(index)


def merge_pdfs():
    paths = merge_listbox.get(0, tk.END)
    if not paths:
        messagebox.showwarning("No Files", "Select PDF files to merge first.")
        return
    output_path = filedialog.asksaveasfilename(
        title="Save merged PDF as",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
    )
    if not output_path:
        return
    writer = PdfWriter()
    try:
        for path in paths:
            reader = PdfReader(path)
            for page in reader.pages:
                writer.add_page(page)
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
        messagebox.showinfo("Merge Complete", f"Merged PDF saved to:\n{output_path}")
    except Exception as exc:
        messagebox.showerror("Error", f"Could not merge PDFs:\n{exc}")


def choose_split_file():
    path = filedialog.askopenfilename(
        title="Select a PDF file to split",
        filetypes=[("PDF files", "*.pdf")],
    )
    if path:
        split_path_var.set(path)


def split_pdf():
    path = split_path_var.get()
    if not path:
        messagebox.showwarning("No File", "Select a PDF to split.")
        return
    try:
        reader = PdfReader(path)
    except Exception as exc:
        messagebox.showerror("Error", f"Could not open PDF:\n{exc}")
        return
    page_count = len(reader.pages)
    split_pos = split_page_var.get().strip()
    if not split_pos:
        messagebox.showwarning("No Page", "Enter a page number to split at.")
        return
    if not split_pos.isdigit():
        messagebox.showwarning("Invalid Page", "Enter a valid numeric page number.")
        return
    split_at = int(split_pos)
    if split_at < 1 or split_at >= page_count:
        messagebox.showwarning(
            "Invalid Page",
            f"Page must be between 1 and {page_count - 1}.",
        )
        return
    base_dir = os.path.dirname(path)
    base_name = os.path.splitext(os.path.basename(path))[0]
    first_output = os.path.join(base_dir, f"{base_name}_part1.pdf")
    second_output = os.path.join(base_dir, f"{base_name}_part2.pdf")
    try:
        writer1 = PdfWriter()
        writer2 = PdfWriter()
        for i in range(split_at):
            writer1.add_page(reader.pages[i])
        for i in range(split_at, page_count):
            writer2.add_page(reader.pages[i])
        with open(first_output, "wb") as out1:
            writer1.write(out1)
        with open(second_output, "wb") as out2:
            writer2.write(out2)
        messagebox.showinfo(
            "Split Complete",
            f"Saved:\n{first_output}\n{second_output}",
        )
    except Exception as exc:
        messagebox.showerror("Error", f"Could not split PDF:\n{exc}")


def create_gui():
    global merge_listbox, split_path_var, split_page_var

    root = tk.Tk()
    root.title("PDF Merge & Split Tool")
    root.geometry("640x420")
    root.resizable(False, False)

    merge_frame = tk.LabelFrame(root, text="Merge PDFs", padx=10, pady=10)
    merge_frame.pack(fill=tk.BOTH, padx=10, pady=8)

    merge_listbox = tk.Listbox(merge_frame, height=8, selectmode=tk.EXTENDED, width=72)
    merge_listbox.pack(side=tk.LEFT, padx=(0, 10), pady=4)

    merge_buttons = tk.Frame(merge_frame)
    merge_buttons.pack(side=tk.LEFT, fill=tk.Y)

    tk.Button(merge_buttons, text="Add PDFs", width=14, command=add_merge_files).pack(pady=4)
    tk.Button(merge_buttons, text="Remove Selected", width=14, command=remove_merge_file).pack(pady=4)
    tk.Button(merge_buttons, text="Merge", width=14, command=merge_pdfs).pack(pady=4)

    split_frame = tk.LabelFrame(root, text="Split PDF", padx=10, pady=10)
    split_frame.pack(fill=tk.BOTH, padx=10, pady=8)

    split_controls = tk.Frame(split_frame)
    split_controls.pack(fill=tk.X, pady=4)

    tk.Label(split_controls, text="PDF File:").grid(row=0, column=0, sticky=tk.W)
    split_path_var = tk.StringVar()
    split_path_entry = tk.Entry(split_controls, textvariable=split_path_var, width=54)
    split_path_entry.grid(row=0, column=1, padx=4, sticky=tk.W)
    tk.Button(split_controls, text="Browse", command=choose_split_file, width=10).grid(row=0, column=2, padx=4)

    tk.Label(split_controls, text="Split after page:").grid(row=1, column=0, sticky=tk.W, pady=(8, 0))
    split_page_var = tk.StringVar()
    tk.Entry(split_controls, textvariable=split_page_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=(8, 0))
    tk.Label(split_controls, text="(Creates two output files)").grid(row=1, column=2, sticky=tk.W, padx=4, pady=(8, 0))

    tk.Button(split_frame, text="Split PDF", command=split_pdf, width=14).pack(pady=8)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
