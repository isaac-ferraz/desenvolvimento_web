-- Estrutura do banco usado pelo site FaTech (MySQL 8)
-- Rodar na instância do banco:  sudo mysql < schema.sql

CREATE DATABASE IF NOT EXISTS desenv_web
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_0900_ai_ci;

USE desenv_web;

-- Cada envio dos formulários de Vestibular e Contato vira uma linha aqui
CREATE TABLE IF NOT EXISTS envios (
  id        INT UNSIGNED NOT NULL AUTO_INCREMENT,
  origem    VARCHAR(20)  NOT NULL,          -- 'vestibular' ou 'contato'
  nome      VARCHAR(150) NOT NULL,
  email     VARCHAR(150) NOT NULL,
  curso     VARCHAR(150) NULL,              -- só no vestibular
  mensagem  TEXT         NULL,              -- só no contato
  criado_em TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
) ENGINE=InnoDB;
