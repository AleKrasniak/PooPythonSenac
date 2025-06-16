-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 16/06/2025 às 21:33
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `busquestudios2`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `administrador`
--

CREATE TABLE `administrador` (
  `id_administrador` int(11) NOT NULL,
  `id_perfil` int(11) NOT NULL,
  `nome` varchar(70) NOT NULL,
  `email` varchar(70) NOT NULL,
  `login` varchar(20) NOT NULL,
  `senha` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `administrador`
--

INSERT INTO `administrador` (`id_administrador`, `id_perfil`, `nome`, `email`, `login`, `senha`) VALUES
(4, 1, 'Admin', 'admin@teste.com', 'admin', '123'),
(5, 1, 'Adm 1', 'admin@busquestudios.com', '', '123');

-- --------------------------------------------------------

--
-- Estrutura para tabela `agendamento`
--

CREATE TABLE `agendamento` (
  `id_agendamento` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_estudio` int(11) NOT NULL,
  `id_profissional` int(11) NOT NULL,
  `data_hora` datetime NOT NULL,
  `valor` decimal(10,2) DEFAULT NULL,
  `status` enum('Agendado','Confirmado','Cancelado','Atendido','Concluído') DEFAULT 'Agendado'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `alvara`
--

CREATE TABLE `alvara` (
  `id_alvara` int(11) NOT NULL,
  `id_estudio` int(11) NOT NULL,
  `numero_alvara` varchar(20) NOT NULL,
  `tipo_alvara` varchar(50) NOT NULL,
  `data_emissao` date NOT NULL,
  `data_validade` date NOT NULL,
  `status` enum('ativo','vencido','suspenso','cancelado') DEFAULT 'ativo',
  `descricao` text DEFAULT NULL,
  `documento_anexo` longblob DEFAULT NULL,
  `criado_em` timestamp NOT NULL DEFAULT current_timestamp(),
  `atualizado_em` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `alvara`
--

INSERT INTO `alvara` (`id_alvara`, `id_estudio`, `numero_alvara`, `tipo_alvara`, `data_emissao`, `data_validade`, `status`, `descricao`, `documento_anexo`, `criado_em`, `atualizado_em`) VALUES
(1, 4, '0247/2025', 'Alvará de Funcionamento', '2025-02-06', '2027-02-06', 'ativo', 'Alvará de Funcionamento do Estúdio', NULL, '2025-06-16 17:09:10', '2025-06-16 17:09:10'),
(2, 4, '1198/2025', 'Licença Sanitária', '2025-06-14', '2027-06-14', 'ativo', 'Licença Sanitária do Estúdio', NULL, '2025-06-16 17:09:10', '2025-06-16 17:09:10');

-- --------------------------------------------------------

--
-- Estrutura para tabela `avaliacao`
--

CREATE TABLE `avaliacao` (
  `id_avaliacao` int(11) NOT NULL,
  `id_agendamento` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_estudio` int(11) NOT NULL,
  `nota` decimal(2,1) NOT NULL CHECK (`nota` between 0 and 5),
  `comentario` text DEFAULT NULL,
  `data_avaliacao` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `chat`
--

CREATE TABLE `chat` (
  `id_chat` int(11) NOT NULL,
  `data_inicio` datetime DEFAULT current_timestamp(),
  `id_cliente` int(11) DEFAULT NULL,
  `id_estudio` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `cliente`
--

CREATE TABLE `cliente` (
  `id_cliente` int(11) NOT NULL,
  `id_perfil` int(11) NOT NULL,
  `id_endereco` int(11) NOT NULL,
  `nome` varchar(70) NOT NULL,
  `dt_nasc` date NOT NULL,
  `genero` enum('Masculino','Feminino') NOT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `cpf` char(11) NOT NULL,
  `email` varchar(150) NOT NULL,
  `login` varchar(20) NOT NULL,
  `senha` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `cliente`
--

INSERT INTO `cliente` (`id_cliente`, `id_perfil`, `id_endereco`, `nome`, `dt_nasc`, `genero`, `telefone`, `cpf`, `email`, `login`, `senha`) VALUES
(1, 2, 1, 'João Silva', '1990-05-15', 'Masculino', '11987654321', '12345678901', 'joao@email.com', 'joaosilva', 'senha123'),
(3, 2, 10, 'Gilson Carvalho', '1990-01-02', 'Masculino', '(42) 99806-4748', '222.222.222', 'GilsonCarvalho1@gmail.com', 'Gilson', 'Gilson123'),
(6, 3, 1, 'Administrador Geral', '1990-01-01', '', '(41) 99999-9999', '000.000.000', 'admin@busquestudios.com', 'admale', '123'),
(9, 2, 16, 'Alex Leal', '2005-06-19', 'Masculino', '429999966622', '88888888877', 'Alex@gmail.com', 'Alex', 'Alex'),
(10, 2, 17, 'André Afonso', '2005-03-04', 'Masculino', '4298887766', '77777777799', 'André@gmail.com', 'Andre', 'Andre'),
(11, 2, 19, 'FernandoGois@gmail.com', '1990-02-19', 'Masculino', '4299992266', '12378945621', 'FernandoGois@gmail.com', 'Nando', 'Nando');

-- --------------------------------------------------------

--
-- Estrutura para tabela `denuncia`
--

CREATE TABLE `denuncia` (
  `id_denuncia` int(11) NOT NULL,
  `id_cliente` int(11) DEFAULT NULL,
  `id_estudio` int(11) DEFAULT NULL,
  `motivo` varchar(250) DEFAULT NULL,
  `status` enum('Pendente','Em análise','Aceita','Rejeitado','Resolvida') DEFAULT 'Pendente',
  `data_criacao` timestamp NOT NULL DEFAULT current_timestamp(),
  `foto_caminho` varchar(255) DEFAULT NULL COMMENT 'Caminho URL da foto',
  `foto_nome_arquivo` varchar(100) DEFAULT NULL COMMENT 'Nome do arquivo',
  `data_atualizacao` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `endereco`
--

CREATE TABLE `endereco` (
  `id_endereco` int(11) NOT NULL,
  `rua` varchar(100) DEFAULT NULL,
  `numero` int(11) DEFAULT NULL,
  `bairro` varchar(50) DEFAULT NULL,
  `cidade` varchar(70) DEFAULT NULL,
  `complemento` varchar(150) DEFAULT NULL,
  `uf` varchar(2) NOT NULL,
  `cep` varchar(9) NOT NULL COMMENT 'Formato: XXXXX-XXX' CHECK (`cep` regexp '^[0-9]{5}-[0-9]{3}$'),
  `data_cadastro` timestamp NOT NULL DEFAULT current_timestamp(),
  `data_atualizacao` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `endereco`
--

INSERT INTO `endereco` (`id_endereco`, `rua`, `numero`, `bairro`, `cidade`, `complemento`, `uf`, `cep`, `data_cadastro`, `data_atualizacao`) VALUES
(1, 'Rua das Flores', 123, 'Centro', 'São Paulo', NULL, 'SP', '01234-567', '2025-06-13 22:35:06', '2025-06-13 22:35:06'),
(2, 'Rua não informada', 1, 'Bairro não informado', 'Ponta Grossa', 'Não informado', 'PR', '12345-678', '2025-06-14 00:36:44', '2025-06-14 00:36:44'),
(3, 'Rua não informada', 1, 'Bairro não informado', 'Ponta Grossa', 'Não informado', 'PR', '12345-678', '2025-06-14 00:36:49', '2025-06-14 00:36:49'),
(4, 'Rua não informada', 1, 'Bairro não informado', 'Ponta Grossa', 'Não informado', 'PR', '12345-678', '2025-06-14 00:40:39', '2025-06-14 00:40:39'),
(5, 'Belmiro Braga', 147, 'Ns. Graças', 'Ponta Grossa', 'Casa', 'PR', '12345-678', '2025-06-14 00:42:13', '2025-06-14 00:42:13'),
(6, 'studio', 154, 'studio', 'Ponta Grossa', 'studio', 'PR', '12345-678', '2025-06-14 03:02:46', '2025-06-14 03:02:46'),
(7, 'studio', 154, 'studio', 'Ponta Grossa', 'studio', 'PR', '12345-678', '2025-06-14 03:02:51', '2025-06-14 03:02:51'),
(8, 'busque', 51, 'busque', 'Ponta Grossa', 'busque', 'PR', '12345-678', '2025-06-14 03:30:06', '2025-06-14 03:30:06'),
(9, 'teste2', 2, 'teste2', 'Ponta Grossa', 'teste2', 'PR', '12345-789', '2025-06-14 03:40:31', '2025-06-14 03:40:31'),
(10, 'Bonifácio Vilela', 456, 'Centro', 'Ponta Grossa', 'Apartamento', 'PR', '12345-678', '2025-06-14 18:47:58', '2025-06-14 18:47:58'),
(11, 'Bonifácio Vilela', 456, 'Centro', 'Ponta Grossa', 'Apartamento', 'PR', '12345-678', '2025-06-14 18:48:03', '2025-06-14 18:48:03'),
(12, 'Bonifácio Vilela', 456, 'Centro', 'Ponta Grossa', 'Apartamento', 'PR', '12345-678', '2025-06-14 18:48:41', '2025-06-14 18:48:41'),
(15, 'Bahia', 658, 'Õrfans', 'Ponta Grossa', 'Casa', 'PR', '12345-678', '2025-06-15 21:09:20', '2025-06-15 21:09:20'),
(16, 'Bahia', 658, 'Órfãs', 'Ponta Grossa', 'casa', 'PR', '12345-678', '2025-06-15 23:16:14', '2025-06-15 23:16:14'),
(17, 'Rua Octávio Carvalho', 456, 'Jardim Carvalho', 'Ponta Grossa', 'Casa', 'PR', '12345-678', '2025-06-15 23:23:20', '2025-06-15 23:23:20'),
(18, 'Comendador Miró', 762, 'Centro', 'Santa Fé', 'Casa', 'PR', '12345-678', '2025-06-15 23:52:41', '2025-06-15 23:52:41'),
(19, 'Comendador Miró', 789, 'Centro', 'Ponta Grossa', 'Casa', 'PR', '12345-678', '2025-06-15 23:55:04', '2025-06-15 23:55:04'),
(20, 'Comendador Miró', 457, 'Centro', 'Ponta Grossa', 'Prédio Teixira Flores', 'PR', '12345-678', '2025-06-16 17:09:10', '2025-06-16 17:09:10');

-- --------------------------------------------------------

--
-- Estrutura para tabela `estudio`
--

CREATE TABLE `estudio` (
  `id_estudio` int(11) NOT NULL,
  `id_perfil` int(11) NOT NULL,
  `id_endereco` int(11) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `cnpj` char(14) NOT NULL,
  `descricao` varchar(250) NOT NULL,
  `login` varchar(20) NOT NULL,
  `senha` varchar(150) NOT NULL,
  `tipo` varchar(50) DEFAULT NULL,
  `foto_perfil` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `estudio`
--

INSERT INTO `estudio` (`id_estudio`, `id_perfil`, `id_endereco`, `nome`, `cnpj`, `descricao`, `login`, `senha`, `tipo`, `foto_perfil`) VALUES
(1, 3, 1, 'Studio Arte & Tattoo', '12345678000190', 'Estúdio especializado em tatuagens artísticas', 'studioarte', 'senha123', 'Tatuagem', 'uploads/studios/studio_arte_perfil.jpg'),
(2, 3, 8, 'Ricardo Tatoos', '11111111111111', 'busque', 'busque', 'busque', 'Tatuagem', 'busque'),
(4, 3, 20, 'Estúdio Arte Mais', '89185808000102', 'Estúdio especializado em Old School', 'ArteMais', 'ArteMais', 'Tatuagem', 'https://img.freepik.com/vetores-premium/logotipo-de-maquinas-de-estudio-de-tatuagem-com-rosa_18591-64922.jpg');

-- --------------------------------------------------------

--
-- Estrutura para tabela `mensagem`
--

CREATE TABLE `mensagem` (
  `id_mensagem` int(11) NOT NULL,
  `id_chat` int(11) NOT NULL,
  `texto` varchar(250) DEFAULT NULL,
  `data_envio` datetime DEFAULT current_timestamp(),
  `remetente_tipo` enum('Cliente','Estudio') NOT NULL,
  `status` enum('Enviada','Entregue','Lida') DEFAULT 'Enviada'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `mensagem_midia`
--

CREATE TABLE `mensagem_midia` (
  `id_mensagem_midia` int(11) NOT NULL,
  `id_mensagem` int(11) NOT NULL,
  `url` varchar(255) NOT NULL,
  `tipo` enum('Imagem','Video','Documento') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `perfil`
--

CREATE TABLE `perfil` (
  `id_perfil` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL COMMENT 'Administrador, Cliente, Estudio',
  `descricao` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `perfil`
--

INSERT INTO `perfil` (`id_perfil`, `nome`, `descricao`) VALUES
(1, 'Administrador', 'Perfil com acesso total ao sistema'),
(2, 'Cliente', 'Perfil para clientes que agendam serviços'),
(3, 'Estudio', 'Perfil para estúdios que oferecem serviços');

-- --------------------------------------------------------

--
-- Estrutura para tabela `perfil_permissao`
--

CREATE TABLE `perfil_permissao` (
  `id_perfil_permissao` int(11) NOT NULL,
  `id_perfil` int(11) NOT NULL,
  `id_permissao` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `perfil_permissao`
--

INSERT INTO `perfil_permissao` (`id_perfil_permissao`, `id_perfil`, `id_permissao`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 4),
(5, 1, 5),
(6, 1, 6),
(7, 1, 7),
(8, 1, 8),
(9, 1, 9),
(10, 2, 4),
(11, 2, 5),
(12, 3, 6),
(13, 3, 7),
(14, 3, 8),
(15, 3, 9);

-- --------------------------------------------------------

--
-- Estrutura para tabela `permissao`
--

CREATE TABLE `permissao` (
  `id_permissao` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `descricao` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Despejando dados para a tabela `permissao`
--

INSERT INTO `permissao` (`id_permissao`, `nome`, `descricao`) VALUES
(1, 'GERENCIAR_USUARIOS', 'Permissão para criar, editar e excluir usuários'),
(2, 'GERENCIAR_ESTUDIOS', 'Permissão para aprovar e gerenciar estúdios'),
(3, 'VISUALIZAR_RELATORIOS', 'Permissão para visualizar relatórios do sistema'),
(4, 'AGENDAR_SERVICOS', 'Permissão para agendar serviços'),
(5, 'AVALIAR_SERVICOS', 'Permissão para avaliar serviços recebidos'),
(6, 'GERENCIAR_AGENDAMENTOS', 'Permissão para gerenciar agendamentos do estúdio'),
(7, 'GERENCIAR_PORTFOLIO', 'Permissão para gerenciar portfólio do estúdio'),
(8, 'CHAT_CLIENTES', 'Permissão para conversar com clientes'),
(9, 'GERENCIAR_ALVARAS', 'Permissão para gerenciar alvarás do estúdio');

-- --------------------------------------------------------

--
-- Estrutura para tabela `portfolio`
--

CREATE TABLE `portfolio` (
  `id_portfolio` int(11) NOT NULL,
  `id_estudio` int(11) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `descricao` text DEFAULT NULL,
  `url_foto` varchar(255) NOT NULL,
  `ordem_exibicao` int(11) DEFAULT 1,
  `ativo` tinyint(1) DEFAULT 1,
  `criado_em` timestamp NOT NULL DEFAULT current_timestamp(),
  `atualizado_em` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `profissional`
--

CREATE TABLE `profissional` (
  `id_profissional` int(11) NOT NULL,
  `id_estudio` int(11) NOT NULL,
  `nome` varchar(70) NOT NULL,
  `cpf` char(11) NOT NULL,
  `especialidade` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `administrador`
--
ALTER TABLE `administrador`
  ADD PRIMARY KEY (`id_administrador`),
  ADD KEY `id_perfil` (`id_perfil`);

--
-- Índices de tabela `agendamento`
--
ALTER TABLE `agendamento`
  ADD PRIMARY KEY (`id_agendamento`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_estudio` (`id_estudio`),
  ADD KEY `id_profissional` (`id_profissional`);

--
-- Índices de tabela `alvara`
--
ALTER TABLE `alvara`
  ADD PRIMARY KEY (`id_alvara`),
  ADD UNIQUE KEY `numero_alvara` (`numero_alvara`),
  ADD KEY `id_estudio` (`id_estudio`);

--
-- Índices de tabela `avaliacao`
--
ALTER TABLE `avaliacao`
  ADD PRIMARY KEY (`id_avaliacao`),
  ADD KEY `id_agendamento` (`id_agendamento`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_estudio` (`id_estudio`);

--
-- Índices de tabela `chat`
--
ALTER TABLE `chat`
  ADD PRIMARY KEY (`id_chat`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_estudio` (`id_estudio`);

--
-- Índices de tabela `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `cpf` (`cpf`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `login` (`login`),
  ADD KEY `id_perfil` (`id_perfil`),
  ADD KEY `id_endereco` (`id_endereco`);

--
-- Índices de tabela `denuncia`
--
ALTER TABLE `denuncia`
  ADD PRIMARY KEY (`id_denuncia`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_estudio` (`id_estudio`);

--
-- Índices de tabela `endereco`
--
ALTER TABLE `endereco`
  ADD PRIMARY KEY (`id_endereco`),
  ADD KEY `idx_cep` (`cep`);

--
-- Índices de tabela `estudio`
--
ALTER TABLE `estudio`
  ADD PRIMARY KEY (`id_estudio`),
  ADD UNIQUE KEY `cnpj` (`cnpj`),
  ADD UNIQUE KEY `login` (`login`),
  ADD KEY `id_perfil` (`id_perfil`),
  ADD KEY `id_endereco` (`id_endereco`);

--
-- Índices de tabela `mensagem`
--
ALTER TABLE `mensagem`
  ADD PRIMARY KEY (`id_mensagem`),
  ADD KEY `id_chat` (`id_chat`);

--
-- Índices de tabela `mensagem_midia`
--
ALTER TABLE `mensagem_midia`
  ADD PRIMARY KEY (`id_mensagem_midia`),
  ADD KEY `id_mensagem` (`id_mensagem`);

--
-- Índices de tabela `perfil`
--
ALTER TABLE `perfil`
  ADD PRIMARY KEY (`id_perfil`);

--
-- Índices de tabela `perfil_permissao`
--
ALTER TABLE `perfil_permissao`
  ADD PRIMARY KEY (`id_perfil_permissao`),
  ADD UNIQUE KEY `uk_perfil_permissao` (`id_perfil`,`id_permissao`),
  ADD KEY `id_permissao` (`id_permissao`);

--
-- Índices de tabela `permissao`
--
ALTER TABLE `permissao`
  ADD PRIMARY KEY (`id_permissao`),
  ADD UNIQUE KEY `nome` (`nome`);

--
-- Índices de tabela `portfolio`
--
ALTER TABLE `portfolio`
  ADD PRIMARY KEY (`id_portfolio`),
  ADD KEY `id_estudio` (`id_estudio`);

--
-- Índices de tabela `profissional`
--
ALTER TABLE `profissional`
  ADD PRIMARY KEY (`id_profissional`),
  ADD UNIQUE KEY `cpf` (`cpf`),
  ADD KEY `id_estudio` (`id_estudio`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `administrador`
--
ALTER TABLE `administrador`
  MODIFY `id_administrador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de tabela `agendamento`
--
ALTER TABLE `agendamento`
  MODIFY `id_agendamento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `alvara`
--
ALTER TABLE `alvara`
  MODIFY `id_alvara` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de tabela `avaliacao`
--
ALTER TABLE `avaliacao`
  MODIFY `id_avaliacao` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `chat`
--
ALTER TABLE `chat`
  MODIFY `id_chat` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de tabela `denuncia`
--
ALTER TABLE `denuncia`
  MODIFY `id_denuncia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `endereco`
--
ALTER TABLE `endereco`
  MODIFY `id_endereco` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de tabela `estudio`
--
ALTER TABLE `estudio`
  MODIFY `id_estudio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de tabela `mensagem`
--
ALTER TABLE `mensagem`
  MODIFY `id_mensagem` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `mensagem_midia`
--
ALTER TABLE `mensagem_midia`
  MODIFY `id_mensagem_midia` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `perfil`
--
ALTER TABLE `perfil`
  MODIFY `id_perfil` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de tabela `perfil_permissao`
--
ALTER TABLE `perfil_permissao`
  MODIFY `id_perfil_permissao` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de tabela `permissao`
--
ALTER TABLE `permissao`
  MODIFY `id_permissao` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de tabela `portfolio`
--
ALTER TABLE `portfolio`
  MODIFY `id_portfolio` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `profissional`
--
ALTER TABLE `profissional`
  MODIFY `id_profissional` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `administrador`
--
ALTER TABLE `administrador`
  ADD CONSTRAINT `administrador_ibfk_1` FOREIGN KEY (`id_perfil`) REFERENCES `perfil` (`id_perfil`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `agendamento`
--
ALTER TABLE `agendamento`
  ADD CONSTRAINT `agendamento_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  ADD CONSTRAINT `agendamento_ibfk_2` FOREIGN KEY (`id_estudio`) REFERENCES `estudio` (`id_estudio`),
  ADD CONSTRAINT `agendamento_ibfk_3` FOREIGN KEY (`id_profissional`) REFERENCES `profissional` (`id_profissional`);

--
-- Restrições para tabelas `alvara`
--
ALTER TABLE `alvara`
  ADD CONSTRAINT `alvara_ibfk_1` FOREIGN KEY (`id_estudio`) REFERENCES `estudio` (`id_estudio`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `avaliacao`
--
ALTER TABLE `avaliacao`
  ADD CONSTRAINT `avaliacao_ibfk_1` FOREIGN KEY (`id_agendamento`) REFERENCES `agendamento` (`id_agendamento`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `avaliacao_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `avaliacao_ibfk_3` FOREIGN KEY (`id_estudio`) REFERENCES `estudio` (`id_estudio`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `chat`
--
ALTER TABLE `chat`
  ADD CONSTRAINT `chat_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `chat_ibfk_2` FOREIGN KEY (`id_estudio`) REFERENCES `estudio` (`id_estudio`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Restrições para tabelas `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`id_perfil`) REFERENCES `perfil` (`id_perfil`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `cliente_ibfk_2` FOREIGN KEY (`id_endereco`) REFERENCES `endereco` (`id_endereco`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `denuncia`
--
ALTER TABLE `denuncia`
  ADD CONSTRAINT `denuncia_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `denuncia_ibfk_2` FOREIGN KEY (`id_estudio`) REFERENCES `estudio` (`id_estudio`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Restrições para tabelas `estudio`
--
ALTER TABLE `estudio`
  ADD CONSTRAINT `estudio_ibfk_1` FOREIGN KEY (`id_perfil`) REFERENCES `perfil` (`id_perfil`) ON UPDATE CASCADE,
  ADD CONSTRAINT `estudio_ibfk_2` FOREIGN KEY (`id_endereco`) REFERENCES `endereco` (`id_endereco`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `mensagem`
--
ALTER TABLE `mensagem`
  ADD CONSTRAINT `mensagem_ibfk_1` FOREIGN KEY (`id_chat`) REFERENCES `chat` (`id_chat`);

--
-- Restrições para tabelas `mensagem_midia`
--
ALTER TABLE `mensagem_midia`
  ADD CONSTRAINT `mensagem_midia_ibfk_1` FOREIGN KEY (`id_mensagem`) REFERENCES `mensagem` (`id_mensagem`) ON DELETE CASCADE;

--
-- Restrições para tabelas `perfil_permissao`
--
ALTER TABLE `perfil_permissao`
  ADD CONSTRAINT `perfil_permissao_ibfk_1` FOREIGN KEY (`id_perfil`) REFERENCES `perfil` (`id_perfil`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `perfil_permissao_ibfk_2` FOREIGN KEY (`id_permissao`) REFERENCES `permissao` (`id_permissao`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `portfolio`
--
ALTER TABLE `portfolio`
  ADD CONSTRAINT `portfolio_ibfk_1` FOREIGN KEY (`id_estudio`) REFERENCES `estudio` (`id_estudio`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Restrições para tabelas `profissional`
--
ALTER TABLE `profissional`
  ADD CONSTRAINT `profissional_ibfk_1` FOREIGN KEY (`id_estudio`) REFERENCES `estudio` (`id_estudio`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;