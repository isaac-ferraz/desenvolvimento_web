# desenvolvimento_web
Projeto criado para a aula de Desenvolvimento Web na Fatec SJC

## Como rodar

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Acesse http://127.0.0.1:5000

## Publicar na AWS EC2

1. No console do EC2, crie uma instância **Ubuntu Server** (t3.micro), chamada `webServer-isaac`,
   com um par de chaves novo.
2. No Security Group, libere **SSH (22/tcp)** e **5000/tcp**.
3. Conecte pelo EC2 Instance Connect (ou `ssh -i chave.pem ubuntu@<IP público>`) e rode:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git
mkdir ~/desenvolvimento_web && cd ~/desenvolvimento_web
python3 -m venv venv
source venv/bin/activate
git init && git remote add origin https://github.com/isaac-ferraz/desenvolvimento_web.git
git pull origin main
pip install -r requirements.txt
pip list
python app.py
```

O `app.py` escuta em `0.0.0.0:5000`, então o site fica em `http://<IP público>:5000`.
