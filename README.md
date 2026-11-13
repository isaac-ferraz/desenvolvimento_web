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

```
 Navegador ───► Aplicação (Flask)                ───► Banco (MySQL 8.4)
                54.174.129.182:5000                    172.31.20.56:3306
                IP público fixo (Elastic IP)           IP PRIVADO (não muda)
```

| Instância | IP público | IP privado | Chave SSH |
|-----------|------------|------------|-----------|
| Aplicação (`webServer-isaac`) | 54.174.129.182 (fixo) | 172.31.33.144 | `webServer-isaacferraz.pem` |
| Banco de dados (MySQL 8.4)    | **muda a cada reinício** | 172.31.20.56 | `database-ads.pem` |

### O IP do banco mudou. Muda alguma coisa?

**Para o site, não.** A aplicação conecta no banco pelo **IP privado** (`DB_HOST` no `.env`),
e o IP privado continua o mesmo quando a instância é parada e ligada de novo. Só o IP público muda.

| O que você quer fazer | Qual IP do banco usar | Muda quando o banco reinicia? |
|-----------------------|-----------------------|-------------------------------|
| Site e Painel de Admin funcionarem | privado `172.31.20.56` (já está no `.env`) | **Não** |
| Entrar no banco por SSH do seu PC | público (pegue no console) | **Sim** → [Tutorial 2](#tutorial-2--entrar-no-banco-por-ssh-com-o-ip-novo) |
| Abrir o banco no Workbench/DBeaver | nenhum: passa pela aplicação | **Não** → [Tutorial 4](#tutorial-4--abrir-o-banco-no-mysql-workbench) |

O IP privado só muda se a instância do banco for **encerrada** (Terminate) e você criar outra
→ [veja aqui](#se-criar-uma-instância-nova-do-banco).

### Tutorial 1 — Ligar tudo depois que as instâncias foram desligadas

1. No console do EC2, em **Instâncias**, selecione as duas e clique em **Estado da instância → Iniciar**.
   Espere as duas ficarem **Executando** com **2/2 verificações aprovadas**.
2. Entre na aplicação (o IP dela é fixo):

   ```bash
   ssh -i ~/Downloads/webServer-isaacferraz.pem ubuntu@54.174.129.182
   ```

3. Suba o site em segundo plano (continua no ar depois que você fechar o SSH):

   ```bash
   cd ~/desenvolvimento_web
   nohup venv/bin/python app.py > ~/fatech.log 2>&1 &
   ```

4. Abra http://54.174.129.182:5000/admin. Se aparecer a tabela de registros (mesmo vazia),
   a aplicação está conectada ao banco.

Para ver os logs: `tail -f ~/fatech.log`. Para parar o site: `pkill -f "python app.py"`.

### Tutorial 2 — Entrar no banco por SSH (com o IP novo)

1. No console do EC2, clique na instância do banco e copie o **Endereço IPv4 público**.
2. No seu PC:

   ```bash
   chmod 400 ~/Downloads/database-ads.pem      # só na primeira vez
   ssh -i ~/Downloads/database-ads.pem ubuntu@<IP público do banco>
   ```

3. Como o IP é novo, o SSH pergunta `Are you sure you want to continue connecting?` → digite `yes`.

> Se aparecer `REMOTE HOST IDENTIFICATION HAS CHANGED`, a AWS reaproveitou esse IP de outra máquina.
> Rode `ssh-keygen -R <IP público do banco>` e conecte de novo.

### Tutorial 3 — Ver e mexer nos dados pelo terminal

Já dentro da instância do banco (Tutorial 2):

```bash
sudo systemctl status mysql        # tem que estar "active (running)"; q para sair
free -m                            # memória e swap (o swap tem que aparecer com 2047)
sudo mysql desenv_web -e "SELECT * FROM envios ORDER BY id DESC;"
```

Para usar o MySQL de forma interativa, rode `sudo mysql` (entra como root, sem senha) e depois:

```sql
USE desenv_web;
SET time_zone = '-03:00';          -- o banco guarda em UTC; isso mostra no horário de Brasília
SHOW TABLES;
DESCRIBE envios;
SELECT id, criado_em, origem, nome, email FROM envios ORDER BY id DESC LIMIT 10;
SELECT origem, COUNT(*) AS total FROM envios GROUP BY origem;
DELETE FROM envios WHERE id = 3;   -- apaga um registro (cuidado: não tem como desfazer)
exit
```

O usuário `fatech`, usado pela aplicação, só pode **ler e inserir**. Para apagar ou alterar dados,
use o `sudo mysql` como acima.

### Tutorial 4 — Abrir o banco no MySQL Workbench

O usuário `fatech` só aceita conexões de dentro da AWS (`172.31.%`), então o Workbench conecta
**passando pela instância da aplicação**. Assim você nunca precisa do IP público do banco.

Em **Database → Manage Connections → New**, escolha o método **Standard TCP/IP over SSH**:

| Campo | Valor |
|-------|-------|
| SSH Hostname | `54.174.129.182:22` |
| SSH Username | `ubuntu` |
| SSH Key File | `webServer-isaacferraz.pem` |
| MySQL Hostname | `172.31.20.56` |
| MySQL Server Port | `3306` |
| Username | `fatech` |
| Password | o `DB_PASSWORD` do `.env` |
| Default Schema | `desenv_web` |

Sem Workbench, dá para fazer o mesmo por um túnel no terminal (deixe-o aberto enquanto usa):

```bash
ssh -i ~/Downloads/webServer-isaacferraz.pem -N -L 3310:172.31.20.56:3306 ubuntu@54.174.129.182
```

e conectar o DBeaver, ou qualquer outro cliente, em `127.0.0.1`, porta `3310`, usuário `fatech`.

### Tutorial 5 — Testar a conexão da aplicação com o banco

Dentro da instância da aplicação:

```bash
nc -zv 172.31.20.56 3306           # a porta do banco responde?
cd ~/desenvolvimento_web
venv/bin/python -c "import banco; print(len(banco.listar_envios()), 'registro(s)')"
```

Se o primeiro comando disser `succeeded` e o segundo mostrar quantos registros existem, está tudo certo.

### Problemas comuns

| O que aparece | Causa provável | Como resolver |
|---------------|----------------|---------------|
| Painel: *Não foi possível conectar ao banco de dados* | Instância do banco desligada ou MySQL parado | Ligue a instância; no banco, `sudo systemctl start mysql` |
| SSH do banco não responde (`banner exchange`) e o MySQL cai | Falta de memória: o kernel matou o MySQL (confira com `journalctl -k -b -1 \| grep -i "out of memory"`) | Reinicie a instância pelo console; confira o swap (`swapon --show`) e o `zz-memoria.cnf` |
| Log: `Can't connect to MySQL server ... (timed out)` | Security Group do banco não libera a 3306 | Regra de entrada **MySQL/Aurora (3306)** com origem na aplicação |
| Log: `Can't connect to MySQL server ... (Connection refused)` | MySQL parado ou `bind-address = 127.0.0.1` | `sudo systemctl start mysql` e confira o `bind-address` |
| Log: `Access denied for user 'fatech'` | Senha errada no `.env` | Corrija o `DB_PASSWORD` e reinicie o site |
| Log: `Table 'desenv_web.envios' doesn't exist` | Tabela não foi criada | Rode o `schema.sql` (passo 1 abaixo) |
| `ssh: connect to host ... Connection timed out` | IP público do banco mudou ou instância desligada | Pegue o IP novo ([Tutorial 2](#tutorial-2--entrar-no-banco-por-ssh-com-o-ip-novo)) |
| `UNPROTECTED PRIVATE KEY FILE!` | Permissão da chave aberta demais | `chmod 400 arquivo.pem` |
| `Address already in use` ao rodar o `app.py` | O site já está rodando | `pkill -f "python app.py"` e suba de novo |

Os erros de banco aparecem no log do site: `tail -50 ~/fatech.log`.

### Se criar uma instância nova do banco

1. Configure o MySQL nela (passo 1 de [Configuração do zero](#configuração-do-zero)).
2. No console do EC2, copie o **Endereço IPv4 privado** da instância nova.
3. Na aplicação, troque o `DB_HOST` no `.env` e reinicie o site:

   ```bash
   cd ~/desenvolvimento_web
   nano .env                          # DB_HOST=<novo IP privado>
   pkill -f "python app.py"
   nohup venv/bin/python app.py > ~/fatech.log 2>&1 &
   ```

### Configuração do zero

#### 1. Na instância do banco

A t3.micro tem só 1 GB de RAM. Sem swap, uma atualização automática do Ubuntu junto com o MySQL
estoura a memória: o kernel mata o MySQL e a instância trava. Por isso, crie 2 GB de swap e
desligue o `performance_schema` (monitoramento interno do MySQL que gasta uns 200 MB):

```bash
sudo fallocate -l 2G /swapfile && sudo chmod 600 /swapfile
sudo mkswap /swapfile && sudo swapon /swapfile
echo "/swapfile none swap sw 0 0" | sudo tee -a /etc/fstab        # mantém depois do reboot
```

```bash
sudo apt update && sudo apt install -y mysql-server
sudo sed -i 's/^bind-address.*/bind-address = 0.0.0.0/' /etc/mysql/mysql.conf.d/mysqld.cnf
printf "[mysqld]\nperformance_schema = OFF\n" | sudo tee /etc/mysql/mysql.conf.d/zz-memoria.cnf
sudo systemctl enable mysql                                        # sobe junto com a instância
sudo systemctl restart mysql
curl -fsSLO https://raw.githubusercontent.com/isaac-ferraz/desenvolvimento_web/main/schema.sql
sudo mysql < schema.sql
sudo mysql -e "CREATE USER 'fatech'@'172.31.%' IDENTIFIED BY '<senha>';
               GRANT SELECT, INSERT ON desenv_web.* TO 'fatech'@'172.31.%';"
```

No Security Group do banco, libere **MySQL/Aurora (3306/tcp)** para a instância da aplicação.

#### 2. Na instância da aplicação

```bash
cd ~/desenvolvimento_web
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # e preencha DB_PASSWORD
chmod 600 .env
python app.py
```

**Opcional:** para o site voltar sozinho quando a instância reiniciar, crie o serviço
`/etc/systemd/system/fatech.service` (aí use `systemctl` em vez do `nohup`/`pkill` dos tutoriais):

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
