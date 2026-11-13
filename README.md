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

## Banco de dados (MySQL em outra instância EC2)

Os formulários de **Vestibular** e **Contato** gravam na tabela `envios` do banco `desenv_web`,
e a página **Painel de Admin** (`/admin`) lista todos os registros.

| Instância | IP público | IP privado |
|-----------|------------|------------|
| Aplicação (`webServer-isaac`) | 54.174.129.182 (Elastic IP) | 172.31.33.144 |
| Banco de dados (MySQL 8.4)    | muda a cada reinício        | 172.31.20.56 |

A aplicação conecta no banco pelo **IP privado**, que não muda quando a instância reinicia
(só o IP público muda). As duas estão na mesma VPC, então o tráfego fica dentro da AWS.

### 1. Na instância do banco

No `/etc/mysql/mysql.conf.d/mysqld.cnf`, deixe `bind-address = 0.0.0.0` e reinicie o MySQL.
Depois crie a tabela e o usuário da aplicação (só com SELECT e INSERT, aceito apenas da rede interna):

```bash
sudo mysql < schema.sql
sudo mysql -e "CREATE USER 'fatech'@'172.31.%' IDENTIFIED BY '<senha>';
               GRANT SELECT, INSERT ON desenv_web.* TO 'fatech'@'172.31.%';"
```

No Security Group do banco, libere **MySQL/Aurora (3306/tcp)** para a instância da aplicação.

### 2. Na instância da aplicação

```bash
cd ~/desenvolvimento_web
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # e preencha DB_PASSWORD
chmod 600 .env
python app.py
```

**Opcional:** para o site continuar no ar depois de fechar o SSH ou reiniciar a instância,
crie o serviço `/etc/systemd/system/fatech.service`:

```ini
[Unit]
Description=Site FaTech (Flask)
After=network-online.target
Wants=network-online.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/desenvolvimento_web
ExecStart=/home/ubuntu/desenvolvimento_web/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now fatech     # liga agora e a cada boot
sudo systemctl restart fatech          # depois de um git pull
journalctl -u fatech -f                # ver os logs
```
