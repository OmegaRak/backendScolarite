-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : ven. 12 déc. 2025 à 20:52
-- Version du serveur : 10.4.24-MariaDB
-- Version de PHP : 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `scolarite`
--

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 3, 'add_permission'),
(6, 'Can change permission', 3, 'change_permission'),
(7, 'Can delete permission', 3, 'delete_permission'),
(8, 'Can view permission', 3, 'view_permission'),
(9, 'Can add group', 2, 'add_group'),
(10, 'Can change group', 2, 'change_group'),
(11, 'Can delete group', 2, 'delete_group'),
(12, 'Can view group', 2, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_utilisateur'),
(22, 'Can change user', 6, 'change_utilisateur'),
(23, 'Can delete user', 6, 'delete_utilisateur'),
(24, 'Can view user', 6, 'view_utilisateur'),
(25, 'Can add concours', 8, 'add_concours'),
(26, 'Can change concours', 8, 'change_concours'),
(27, 'Can delete concours', 8, 'delete_concours'),
(28, 'Can view concours', 8, 'view_concours'),
(29, 'Can add candidat', 7, 'add_candidat'),
(30, 'Can change candidat', 7, 'change_candidat'),
(31, 'Can delete candidat', 7, 'delete_candidat'),
(32, 'Can view candidat', 7, 'view_candidat'),
(33, 'Can add etudiant', 9, 'add_etudiant'),
(34, 'Can change etudiant', 9, 'change_etudiant'),
(35, 'Can delete etudiant', 9, 'delete_etudiant'),
(36, 'Can view etudiant', 9, 'view_etudiant'),
(37, 'Can add formulaire', 10, 'add_formulaire'),
(38, 'Can change formulaire', 10, 'change_formulaire'),
(39, 'Can delete formulaire', 10, 'delete_formulaire'),
(40, 'Can view formulaire', 10, 'view_formulaire'),
(41, 'Can add inscription concours', 11, 'add_inscriptionconcours'),
(42, 'Can change inscription concours', 11, 'change_inscriptionconcours'),
(43, 'Can delete inscription concours', 11, 'delete_inscriptionconcours'),
(44, 'Can view inscription concours', 11, 'view_inscriptionconcours'),
(45, 'Can add resultat concours', 12, 'add_resultatconcours'),
(46, 'Can change resultat concours', 12, 'change_resultatconcours'),
(47, 'Can delete resultat concours', 12, 'delete_resultatconcours'),
(48, 'Can view resultat concours', 12, 'view_resultatconcours'),
(49, 'Can add annee scolaire', 13, 'add_anneescolaire'),
(50, 'Can change annee scolaire', 13, 'change_anneescolaire'),
(51, 'Can delete annee scolaire', 13, 'delete_anneescolaire'),
(52, 'Can view annee scolaire', 13, 'view_anneescolaire'),
(53, 'Can add reinscription', 14, 'add_reinscription'),
(54, 'Can change reinscription', 14, 'change_reinscription'),
(55, 'Can delete reinscription', 14, 'delete_reinscription'),
(56, 'Can view reinscription', 14, 'view_reinscription'),
(57, 'Can add resultat niveau', 16, 'add_resultatniveau'),
(58, 'Can change resultat niveau', 16, 'change_resultatniveau'),
(59, 'Can delete resultat niveau', 16, 'delete_resultatniveau'),
(60, 'Can view resultat niveau', 16, 'view_resultatniveau'),
(61, 'Can add niveau', 15, 'add_niveau'),
(62, 'Can change niveau', 15, 'change_niveau'),
(63, 'Can delete niveau', 15, 'delete_niveau'),
(64, 'Can view niveau', 15, 'view_niveau');

-- --------------------------------------------------------

--
-- Structure de la table `auth_users_utilisateur`
--

CREATE TABLE `auth_users_utilisateur` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(50) NOT NULL,
  `email` varchar(254) NOT NULL,
  `etudiant_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `auth_users_utilisateur`
--

INSERT INTO `auth_users_utilisateur` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `role`, `email`, `etudiant_id`) VALUES
(1, 'pbkdf2_sha256$1200000$aKc3qZpTuj4K9pkkyEvdml$HD4ZMYL3sze/jQe57Pd0owKN1Dnn8dT4R7sa9xtYaLY=', NULL, 0, 'omega', 'Heritina Oméga', 'RAKOTONIRINA', 0, 1, '2025-12-11 20:20:42.766965', 'CANDIDAT', 'omegaraher@gmail.com', NULL),
(2, 'pbkdf2_sha256$1200000$7I551hyjDtZpHk0JYr17YG$aoMttJWgpbaPejGtGEi7FFIGotyVg0smjs4Bz4qtFy0=', NULL, 0, 'andry', 'Andrianatoavina Jean Modeste', 'RAFANOMEZANTSOA', 0, 1, '2025-12-11 20:22:06.688959', 'ETUDIANT', 'modeste.p11.ceres@gmail.com', NULL),
(3, 'pbkdf2_sha256$1200000$oAVqiQwVVeQ5XBWADxKqqT$fWqEW1UFyEIe5Mj+zanCxAoAxOyzUN1CCmIeApv5dqw=', NULL, 0, 'admin', 'De l\'Apllication', 'ADMINISTRATEUR', 0, 1, '2025-12-11 20:24:45.736496', 'ADMIN', 'niritianaarlinah@gmail.com', NULL);

-- --------------------------------------------------------

--
-- Structure de la table `auth_users_utilisateur_groups`
--

CREATE TABLE `auth_users_utilisateur_groups` (
  `id` bigint(20) NOT NULL,
  `utilisateur_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `auth_users_utilisateur_user_permissions`
--

CREATE TABLE `auth_users_utilisateur_user_permissions` (
  `id` bigint(20) NOT NULL,
  `utilisateur_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'group'),
(3, 'auth', 'permission'),
(6, 'auth_users', 'utilisateur'),
(4, 'contenttypes', 'contenttype'),
(7, 'inscription', 'candidat'),
(8, 'inscription', 'concours'),
(9, 'inscription', 'etudiant'),
(10, 'inscription', 'formulaire'),
(11, 'inscription', 'inscriptionconcours'),
(12, 'inscription', 'resultatconcours'),
(13, 'reinscription', 'anneescolaire'),
(15, 'reinscription', 'niveau'),
(14, 'reinscription', 'reinscription'),
(16, 'reinscription', 'resultatniveau'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-12-11 20:18:53.529369'),
(2, 'auth_users', '0001_initial', '2025-12-11 20:18:53.945728'),
(3, 'admin', '0001_initial', '2025-12-11 20:18:56.082509'),
(4, 'admin', '0002_logentry_remove_auto_add', '2025-12-11 20:18:56.125140'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2025-12-11 20:18:56.163878'),
(6, 'contenttypes', '0002_remove_content_type_name', '2025-12-11 20:18:57.440166'),
(7, 'auth', '0001_initial', '2025-12-11 20:19:02.331121'),
(8, 'auth', '0002_alter_permission_name_max_length', '2025-12-11 20:19:03.050718'),
(9, 'auth', '0003_alter_user_email_max_length', '2025-12-11 20:19:03.095371'),
(10, 'auth', '0004_alter_user_username_opts', '2025-12-11 20:19:03.123881'),
(11, 'auth', '0005_alter_user_last_login_null', '2025-12-11 20:19:03.168063'),
(12, 'auth', '0006_require_contenttypes_0002', '2025-12-11 20:19:03.201439'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2025-12-11 20:19:03.244806'),
(14, 'auth', '0008_alter_user_username_max_length', '2025-12-11 20:19:03.283942'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2025-12-11 20:19:03.322828'),
(16, 'auth', '0010_alter_group_name_max_length', '2025-12-11 20:19:03.446336'),
(17, 'auth', '0011_update_proxy_permissions', '2025-12-11 20:19:03.480592'),
(18, 'auth', '0012_alter_user_first_name_max_length', '2025-12-11 20:19:03.528305'),
(19, 'inscription', '0001_initial', '2025-12-11 20:19:11.934179'),
(20, 'auth_users', '0002_initial', '2025-12-11 20:19:18.842142'),
(21, 'reinscription', '0001_initial', '2025-12-11 20:19:22.590098'),
(22, 'sessions', '0001_initial', '2025-12-11 20:19:23.272204'),
(23, 'reinscription', '0002_niveau_alter_reinscription_concours_resultatniveau', '2025-12-12 15:11:16.570228');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `inscription_candidat`
--

CREATE TABLE `inscription_candidat` (
  `id` bigint(20) NOT NULL,
  `statut_candidature` varchar(50) NOT NULL,
  `date_candidature` datetime(6) NOT NULL,
  `utilisateur_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `inscription_concours`
--

CREATE TABLE `inscription_concours` (
  `id` bigint(20) NOT NULL,
  `nom` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `date_debut` date NOT NULL,
  `date_fin` date NOT NULL,
  `prix` double NOT NULL,
  `note_deliberation` double NOT NULL,
  `statut` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `inscription_concours`
--

INSERT INTO `inscription_concours` (`id`, `nom`, `description`, `date_debut`, `date_fin`, `prix`, `note_deliberation`, `statut`, `created_at`) VALUES
(1, 'concours d\'entrer en L1-Métier digital', 'metier digitale', '2025-12-06', '2025-12-20', 50000, 10, 'DISPONIBLE', '2025-12-11 20:33:04.446636');

-- --------------------------------------------------------

--
-- Structure de la table `inscription_etudiant`
--

CREATE TABLE `inscription_etudiant` (
  `id` bigint(20) NOT NULL,
  `matricule` varchar(50) NOT NULL,
  `statut_reinscription` varchar(50) NOT NULL,
  `candidat_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `inscription_formulaire`
--

CREATE TABLE `inscription_formulaire` (
  `id` bigint(20) NOT NULL,
  `niveau_requis` varchar(255) NOT NULL,
  `date_soumission` datetime(6) NOT NULL,
  `candidat_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Structure de la table `inscription_inscriptionconcours`
--

CREATE TABLE `inscription_inscriptionconcours` (
  `id` bigint(20) NOT NULL,
  `date_inscription` datetime(6) NOT NULL,
  `statut` varchar(50) NOT NULL,
  `justificatif_paiement` varchar(100) DEFAULT NULL,
  `numero_inscription` varchar(20) DEFAULT NULL,
  `concours_id` bigint(20) NOT NULL,
  `utilisateur_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `inscription_inscriptionconcours`
--

INSERT INTO `inscription_inscriptionconcours` (`id`, `date_inscription`, `statut`, `justificatif_paiement`, `numero_inscription`, `concours_id`, `utilisateur_id`) VALUES
(5, '2025-12-11 21:18:00.958045', 'VALIDÉ', 'versements/resultat_TELwUn5.PNG', '666', 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `inscription_resultatconcours`
--

CREATE TABLE `inscription_resultatconcours` (
  `id` bigint(20) NOT NULL,
  `note` double NOT NULL,
  `classement` int(11) DEFAULT NULL,
  `date_publication` datetime(6) NOT NULL,
  `admis` tinyint(1) NOT NULL,
  `concours_id` bigint(20) NOT NULL,
  `utilisateur_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `inscription_resultatconcours`
--

INSERT INTO `inscription_resultatconcours` (`id`, `note`, `classement`, `date_publication`, `admis`, `concours_id`, `utilisateur_id`) VALUES
(1, 15, 2, '2025-12-11 22:06:15.825459', 1, 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `reinscription_anneescolaire`
--

CREATE TABLE `reinscription_anneescolaire` (
  `id` bigint(20) NOT NULL,
  `libelle` varchar(20) NOT NULL,
  `actif` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `reinscription_anneescolaire`
--

INSERT INTO `reinscription_anneescolaire` (`id`, `libelle`, `actif`) VALUES
(1, '2024-2025', 1);

-- --------------------------------------------------------

--
-- Structure de la table `reinscription_niveau`
--

CREATE TABLE `reinscription_niveau` (
  `id` bigint(20) NOT NULL,
  `nom` varchar(50) NOT NULL,
  `seuil_deliberation` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `reinscription_niveau`
--

INSERT INTO `reinscription_niveau` (`id`, `nom`, `seuil_deliberation`) VALUES
(1, 'L1', 10);

-- --------------------------------------------------------

--
-- Structure de la table `reinscription_reinscription`
--

CREATE TABLE `reinscription_reinscription` (
  `id` bigint(20) NOT NULL,
  `niveau_actuel` varchar(100) NOT NULL,
  `niveau_vise` varchar(100) NOT NULL,
  `dossier_pdf` varchar(100) NOT NULL,
  `bordereau` varchar(100) DEFAULT NULL,
  `statut` varchar(20) NOT NULL,
  `date_soumission` datetime(6) NOT NULL,
  `date_modification` datetime(6) NOT NULL,
  `annee_scolaire_id` bigint(20) NOT NULL,
  `concours_id` bigint(20) DEFAULT NULL,
  `utilisateur_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `reinscription_reinscription`
--

INSERT INTO `reinscription_reinscription` (`id`, `niveau_actuel`, `niveau_vise`, `dossier_pdf`, `bordereau`, `statut`, `date_soumission`, `date_modification`, `annee_scolaire_id`, `concours_id`, `utilisateur_id`) VALUES
(1, 'Tle', 'L1', 'reinscriptions/CV_Andrianatoavina.pdf', 'versements/Lettre_de_motivation_Andrianatoavina.pdf', 'VALIDEE', '2025-12-11 22:10:28.730594', '2025-12-11 22:11:27.238254', 1, 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `reinscription_resultatniveau`
--

CREATE TABLE `reinscription_resultatniveau` (
  `id` bigint(20) NOT NULL,
  `moyenne` double NOT NULL,
  `admis` tinyint(1) NOT NULL,
  `remarque` varchar(255) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `annee_scolaire_id` bigint(20) NOT NULL,
  `niveau_id` bigint(20) NOT NULL,
  `utilisateur_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Déchargement des données de la table `reinscription_resultatniveau`
--

INSERT INTO `reinscription_resultatniveau` (`id`, `moyenne`, `admis`, `remarque`, `created_at`, `annee_scolaire_id`, `niveau_id`, `utilisateur_id`) VALUES
(2, 12, 1, 'ADMIS', '2025-12-12 17:45:20.042472', 1, 1, 2);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Index pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Index pour la table `auth_users_utilisateur`
--
ALTER TABLE `auth_users_utilisateur`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `etudiant_id` (`etudiant_id`);

--
-- Index pour la table `auth_users_utilisateur_groups`
--
ALTER TABLE `auth_users_utilisateur_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_users_utilisateur_g_utilisateur_id_group_id_453607f4_uniq` (`utilisateur_id`,`group_id`),
  ADD KEY `auth_users_utilisateur_groups_group_id_c298b728_fk_auth_group_id` (`group_id`);

--
-- Index pour la table `auth_users_utilisateur_user_permissions`
--
ALTER TABLE `auth_users_utilisateur_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_users_utilisateur_u_utilisateur_id_permissio_55839615_uniq` (`utilisateur_id`,`permission_id`),
  ADD KEY `auth_users_utilisate_permission_id_49a60e7c_fk_auth_perm` (`permission_id`);

--
-- Index pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_users_utilisateur_id` (`user_id`);

--
-- Index pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Index pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Index pour la table `inscription_candidat`
--
ALTER TABLE `inscription_candidat`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `utilisateur_id` (`utilisateur_id`);

--
-- Index pour la table `inscription_concours`
--
ALTER TABLE `inscription_concours`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `inscription_etudiant`
--
ALTER TABLE `inscription_etudiant`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `matricule` (`matricule`),
  ADD UNIQUE KEY `candidat_id` (`candidat_id`);

--
-- Index pour la table `inscription_formulaire`
--
ALTER TABLE `inscription_formulaire`
  ADD PRIMARY KEY (`id`),
  ADD KEY `inscription_formulai_candidat_id_7bb8708e_fk_inscripti` (`candidat_id`);

--
-- Index pour la table `inscription_inscriptionconcours`
--
ALTER TABLE `inscription_inscriptionconcours`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `inscription_inscriptionc_utilisateur_id_concours__ff023d9f_uniq` (`utilisateur_id`,`concours_id`),
  ADD KEY `inscription_inscript_concours_id_8d9415c7_fk_inscripti` (`concours_id`);

--
-- Index pour la table `inscription_resultatconcours`
--
ALTER TABLE `inscription_resultatconcours`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `inscription_resultatconc_concours_id_utilisateur__a19234a2_uniq` (`concours_id`,`utilisateur_id`),
  ADD KEY `inscription_resultat_utilisateur_id_1b1a0d7c_fk_auth_user` (`utilisateur_id`);

--
-- Index pour la table `reinscription_anneescolaire`
--
ALTER TABLE `reinscription_anneescolaire`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `reinscription_niveau`
--
ALTER TABLE `reinscription_niveau`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nom` (`nom`);

--
-- Index pour la table `reinscription_reinscription`
--
ALTER TABLE `reinscription_reinscription`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reinscription_reinscript_utilisateur_id_annee_sco_2b9fc720_uniq` (`utilisateur_id`,`annee_scolaire_id`),
  ADD KEY `reinscription_reinsc_annee_scolaire_id_ac20008f_fk_reinscrip` (`annee_scolaire_id`),
  ADD KEY `reinscription_reinsc_concours_id_fd106f0f_fk_inscripti` (`concours_id`);

--
-- Index pour la table `reinscription_resultatniveau`
--
ALTER TABLE `reinscription_resultatniveau`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `reinscription_resultatni_utilisateur_id_niveau_id_fbdacd52_uniq` (`utilisateur_id`,`niveau_id`,`annee_scolaire_id`),
  ADD KEY `reinscription_result_annee_scolaire_id_3e4b34ca_fk_reinscrip` (`annee_scolaire_id`),
  ADD KEY `reinscription_result_niveau_id_69f10d1e_fk_reinscrip` (`niveau_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT pour la table `auth_users_utilisateur`
--
ALTER TABLE `auth_users_utilisateur`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `auth_users_utilisateur_groups`
--
ALTER TABLE `auth_users_utilisateur_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `auth_users_utilisateur_user_permissions`
--
ALTER TABLE `auth_users_utilisateur_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT pour la table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT pour la table `inscription_candidat`
--
ALTER TABLE `inscription_candidat`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `inscription_concours`
--
ALTER TABLE `inscription_concours`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `inscription_etudiant`
--
ALTER TABLE `inscription_etudiant`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `inscription_formulaire`
--
ALTER TABLE `inscription_formulaire`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT pour la table `inscription_inscriptionconcours`
--
ALTER TABLE `inscription_inscriptionconcours`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT pour la table `inscription_resultatconcours`
--
ALTER TABLE `inscription_resultatconcours`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `reinscription_anneescolaire`
--
ALTER TABLE `reinscription_anneescolaire`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `reinscription_niveau`
--
ALTER TABLE `reinscription_niveau`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `reinscription_reinscription`
--
ALTER TABLE `reinscription_reinscription`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT pour la table `reinscription_resultatniveau`
--
ALTER TABLE `reinscription_resultatniveau`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Contraintes pour la table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Contraintes pour la table `auth_users_utilisateur`
--
ALTER TABLE `auth_users_utilisateur`
  ADD CONSTRAINT `auth_users_utilisate_etudiant_id_dd4230c6_fk_inscripti` FOREIGN KEY (`etudiant_id`) REFERENCES `inscription_etudiant` (`id`);

--
-- Contraintes pour la table `auth_users_utilisateur_groups`
--
ALTER TABLE `auth_users_utilisateur_groups`
  ADD CONSTRAINT `auth_users_utilisate_utilisateur_id_0c165ee9_fk_auth_user` FOREIGN KEY (`utilisateur_id`) REFERENCES `auth_users_utilisateur` (`id`),
  ADD CONSTRAINT `auth_users_utilisateur_groups_group_id_c298b728_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Contraintes pour la table `auth_users_utilisateur_user_permissions`
--
ALTER TABLE `auth_users_utilisateur_user_permissions`
  ADD CONSTRAINT `auth_users_utilisate_permission_id_49a60e7c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_users_utilisate_utilisateur_id_7cbe4b79_fk_auth_user` FOREIGN KEY (`utilisateur_id`) REFERENCES `auth_users_utilisateur` (`id`);

--
-- Contraintes pour la table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_users_utilisateur_id` FOREIGN KEY (`user_id`) REFERENCES `auth_users_utilisateur` (`id`);

--
-- Contraintes pour la table `inscription_candidat`
--
ALTER TABLE `inscription_candidat`
  ADD CONSTRAINT `inscription_candidat_utilisateur_id_84c35c9e_fk_auth_user` FOREIGN KEY (`utilisateur_id`) REFERENCES `auth_users_utilisateur` (`id`);

--
-- Contraintes pour la table `inscription_etudiant`
--
ALTER TABLE `inscription_etudiant`
  ADD CONSTRAINT `inscription_etudiant_candidat_id_a03dc518_fk_inscripti` FOREIGN KEY (`candidat_id`) REFERENCES `inscription_candidat` (`id`);

--
-- Contraintes pour la table `inscription_formulaire`
--
ALTER TABLE `inscription_formulaire`
  ADD CONSTRAINT `inscription_formulai_candidat_id_7bb8708e_fk_inscripti` FOREIGN KEY (`candidat_id`) REFERENCES `inscription_candidat` (`id`);

--
-- Contraintes pour la table `inscription_inscriptionconcours`
--
ALTER TABLE `inscription_inscriptionconcours`
  ADD CONSTRAINT `inscription_inscript_concours_id_8d9415c7_fk_inscripti` FOREIGN KEY (`concours_id`) REFERENCES `inscription_concours` (`id`),
  ADD CONSTRAINT `inscription_inscript_utilisateur_id_ea4b743f_fk_auth_user` FOREIGN KEY (`utilisateur_id`) REFERENCES `auth_users_utilisateur` (`id`);

--
-- Contraintes pour la table `inscription_resultatconcours`
--
ALTER TABLE `inscription_resultatconcours`
  ADD CONSTRAINT `inscription_resultat_concours_id_e1d08720_fk_inscripti` FOREIGN KEY (`concours_id`) REFERENCES `inscription_concours` (`id`),
  ADD CONSTRAINT `inscription_resultat_utilisateur_id_1b1a0d7c_fk_auth_user` FOREIGN KEY (`utilisateur_id`) REFERENCES `auth_users_utilisateur` (`id`);

--
-- Contraintes pour la table `reinscription_reinscription`
--
ALTER TABLE `reinscription_reinscription`
  ADD CONSTRAINT `reinscription_reinsc_annee_scolaire_id_ac20008f_fk_reinscrip` FOREIGN KEY (`annee_scolaire_id`) REFERENCES `reinscription_anneescolaire` (`id`),
  ADD CONSTRAINT `reinscription_reinsc_concours_id_fd106f0f_fk_inscripti` FOREIGN KEY (`concours_id`) REFERENCES `inscription_concours` (`id`),
  ADD CONSTRAINT `reinscription_reinsc_utilisateur_id_599f1cf3_fk_auth_user` FOREIGN KEY (`utilisateur_id`) REFERENCES `auth_users_utilisateur` (`id`);

--
-- Contraintes pour la table `reinscription_resultatniveau`
--
ALTER TABLE `reinscription_resultatniveau`
  ADD CONSTRAINT `reinscription_result_annee_scolaire_id_3e4b34ca_fk_reinscrip` FOREIGN KEY (`annee_scolaire_id`) REFERENCES `reinscription_anneescolaire` (`id`),
  ADD CONSTRAINT `reinscription_result_niveau_id_69f10d1e_fk_reinscrip` FOREIGN KEY (`niveau_id`) REFERENCES `reinscription_niveau` (`id`),
  ADD CONSTRAINT `reinscription_result_utilisateur_id_f9e86300_fk_auth_user` FOREIGN KEY (`utilisateur_id`) REFERENCES `auth_users_utilisateur` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
