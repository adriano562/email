import requests
import tkinter as tk
from tkinter import messagebox

BASE_URL = "https://api.mail.tm"

email = ""
senha = ""
token = ""

def criar_email():
    global email, senha

    try:
        dominios = requests.get(f"{BASE_URL}/domains").json()
        dominio = dominios["hydra:member"][0]["domain"]

        email = f"user{len(dominio)}@{dominio}"
        senha = "123456"

        requests.post(f"{BASE_URL}/accounts", json={
            "address": email,
            "password": senha
        })

        label_email.config(text=f"Email: {email}")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

def login():
    global token

    try:
        r = requests.post(f"{BASE_URL}/token", json={
            "address": email,
            "password": senha
        })

        token = r.json().get("token")

    except Exception as e:
        messagebox.showerror("Erro", str(e))


def buscar_mensagens():
    if not email:
        messagebox.showwarning("Aviso", "Crie um email primeiro")
        return

    try:
        login()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        r = requests.get(f"{BASE_URL}/messages", headers=headers)
        mensagens = r.json()["hydra:member"]

        lista.delete(0, tk.END)

        if not mensagens:
            lista.insert(tk.END, "Nenhuma mensagem ainda...")
        else:
            for msg in mensagens:
                texto = f"{msg['from']['address']} - {msg['subject']}"
                lista.insert(tk.END, texto)

    except Exception as e:
        messagebox.showerror("Erro", str(e))
def copiar_email():
    if not email:
        messagebox.showwarning("Aviso", "Nenhum email gerado")
        return

    janela.clipboard_clear()
    janela.clipboard_append(email)
    janela.update()

    messagebox.showinfo("Copiado", "Email copiado!")


janela = tk.Tk()
janela.title("Email Temporário")
janela.geometry("400x400")
janela.config(bg="#121212")

titulo = tk.Label(janela, text="Email Temporário", font=("Arial", 18, "bold"),
                  bg="#121212", fg="#00aaff")
titulo.pack(pady=10)

btn_criar = tk.Button(janela, text="Gerar Email",
                      command=criar_email,
                      bg="#1f6feb", fg="white")
btn_criar.pack(pady=5)

label_email = tk.Label(janela, text="Email: ---",
                       bg="#121212", fg="white")
label_email.pack(pady=5)

btn_buscar = tk.Button(janela, text="Ver Mensagens",
                       command=buscar_mensagens,
                       bg="#1f6feb", fg="white")
btn_buscar.pack(pady=5)
btn_copiar = tk.Button(janela, text="Copiar Email",
                       command=copiar_email,
                       bg="#1f6feb", fg="white",
                       relief="flat")
btn_copiar.pack(pady=5)


lista = tk.Listbox(janela, width=50, height=15,
                   bg="#1e1e1e", fg="white")
lista.pack(pady=10)

janela.mainloop()