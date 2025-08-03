import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES

def scan_and_delete_dot_files(folder_path):
    """Quét và xóa các file bắt đầu bằng '._' trong thư mục."""
    deleted_files = []
    try:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.startswith('._'):
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        deleted_files.append(file_path)
                    except Exception as e:
                        print(f"Lỗi khi xóa {file_path}: {e}")
        return deleted_files
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể quét thư mục: {e}")
        return []

def drop(event):
    """Xử lý sự kiện kéo thả thư mục."""
    folder_path = event.data
    if folder_path.startswith('{'):
        folder_path = folder_path.strip('{}').split('} {')[0]
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder_path)
    drop_frame.config(bg="#e0e0e0")  # Trở về màu gốc sau khi thả

def drag_enter(event):
    """Hiệu ứng khi kéo file vào khu vực drop."""
    drop_frame.config(bg="#d0d0d0")  # Tăng độ sáng khi kéo vào

def drag_leave(event):
    """Hiệu ứng khi kéo file ra khỏi khu vực drop."""
    drop_frame.config(bg="#e0e0e0")  # Trở về màu gốc

def browse_folder():
    """Mở hộp thoại chọn thư mục."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_path)

def dot_clean():
    """Xử lý khi nhấn nút Dot Clean."""
    folder_path = folder_entry.get()
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một thư mục hợp lệ!")
        return
    
    deleted_files = scan_and_delete_dot_files(folder_path)
    if deleted_files:
        messagebox.showinfo("Thành công", f"Đã xóa {len(deleted_files)} file:\n" + "\n".join(deleted_files[:5]) + ("\n..." if len(deleted_files) > 5 else ""))
    else:
        messagebox.showinfo("Thông báo", "Không tìm thấy file '._*' nào trong thư mục.")

# Tạo cửa sổ giao diện
root = TkinterDnD.Tk()
root.title("Dot Cleaner")
root.geometry("420x420")
root.resizable(False, False)
root.configure(bg="#f0f0f0")  # Màu nền nhạt giống macOS

# Tùy chỉnh cửa sổ để có hiệu ứng trong suốt (macOS-like)
root.attributes('-alpha', 0.98)  # Độ trong suốt nhẹ

# Frame chính
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Canvas để tạo drop shadow
shadow_canvas = tk.Canvas(frame, bg="#f0f0f0", highlightthickness=0)
shadow_canvas.place(relwidth=0.95, relheight=0.75, relx=0.025, rely=0.025)
shadow_canvas.create_rectangle(8, 8, 388, 308, fill="#d0d0d0", outline="", tags="shadow")  # Bóng đổ
shadow_canvas.create_rectangle(5, 5, 385, 305, fill="#e0e0e0", outline="", tags="background")  # Nền chính

# Khu vực kéo thả
drop_frame = tk.Frame(frame, bg="#e0e0e0")
drop_frame.place(relwidth=0.95, relheight=0.75, relx=0.025, rely=0.025)

# Canvas cho border gạch
canvas = tk.Canvas(drop_frame, bg="#e0e0e0", highlightthickness=0)
canvas.place(relwidth=1.0, relheight=1.0)
canvas.create_rectangle(10, 10, 370, 280, dash=(4, 4), outline="#333333", width=2)

# Label, Entry, và Button
label = tk.Label(drop_frame, text="Kéo thả thư mục hoặc nhấn Chọn:", bg="#e0e0e0", font=("Helvetica", 12), fg="#333333")
label.place(relx=0.5, rely=0.35, anchor="center")
folder_entry = tk.Entry(drop_frame, width=30, font=("Helvetica", 10), bd=1, relief="flat", bg="#ffffff", highlightthickness=1, highlightcolor="#007aff")
folder_entry.place(relx=0.5, rely=0.5, anchor="center")
browse_button = tk.Button(drop_frame, text="Chọn thư mục", command=browse_folder, bg="#007aff", fg="white", font=("Helvetica", 10, "bold"), bd=0, relief="flat", activebackground="#005bb5")
browse_button.place(relx=0.5, rely=0.65, anchor="center")

# Bo góc cho nút Chọn thư mục
browse_button.configure(borderwidth=0, highlightthickness=0)
browse_button.bind("<Enter>", lambda e: browse_button.config(bg="#005bb5"))
browse_button.bind("<Leave>", lambda e: browse_button.config(bg="#007aff"))

# Kéo thả cho drop_frame
drop_frame.drop_target_register(DND_FILES)
drop_frame.dnd_bind('<<Drop>>', drop)
drop_frame.dnd_bind('<<DragEnter>>', drag_enter)
drop_frame.dnd_bind('<<DragLeave>>', drag_leave)

# Nút Dot Clean
clean_button = tk.Button(frame, text="Dot Clean", command=dot_clean, bg="#ff3b30", fg="white", font=("Helvetica", 12, "bold"), bd=0, relief="flat", activebackground="#cc2e26")
clean_button.place(rely=0.8, relwidth=0.95, relheight=0.15, relx=0.025)
clean_button.bind("<Enter>", lambda e: clean_button.config(bg="#cc2e26"))
clean_button.bind("<Leave>", lambda e: clean_button.config(bg="#ff3b30"))

# Chạy ứng dụng
root.mainloop()