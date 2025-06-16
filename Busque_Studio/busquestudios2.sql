-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 16/06/2025 às 21:41
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
  `foto_caminho` varchar(255) DEFAULT NULL,
  `foto_nome_arquivo` varchar(100) DEFAULT NULL,
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
  `cep` varchar(9) NOT NULL CHECK (`cep` regexp '^[0-9]{5}-[0-9]{3}$'),
  `data_cadastro` timestamp NOT NULL DEFAULT current_timestamp(),
  `data_atualizacao` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  `nome` varchar(50) NOT NULL,
  `descricao` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `perfil_permissao`
--

CREATE TABLE `perfil_permissao` (
  `id_perfil_permissao` int(11) NOT NULL,
  `id_perfil` int(11) NOT NULL,
  `id_permissao` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `permissao`
--

CREATE TABLE `permissao` (
  `id_permissao` int(11) NOT NULL,
  `nome` varchar(50) NOT NULL,
  `descricao` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
