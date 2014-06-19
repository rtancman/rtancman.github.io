<?php
/** 
 * As configurações básicas do WordPress.
 *
 * Esse arquivo contém as seguintes configurações: configurações de MySQL, Prefixo de Tabelas,
 * Chaves secretas, Idioma do WordPress, e ABSPATH. Você pode encontrar mais informações
 * visitando {@link http://codex.wordpress.org/Editing_wp-config.php Editing
 * wp-config.php} Codex page. Você pode obter as configurações de MySQL de seu servidor de hospedagem.
 *
 * Esse arquivo é usado pelo script ed criação wp-config.php durante a
 * instalação. Você não precisa usar o site, você pode apenas salvar esse arquivo
 * como "wp-config.php" e preencher os valores.
 *
 * @package WordPress
 */

// ** Configurações do MySQL - Você pode pegar essas informações com o serviço de hospedagem ** //
/** O nome do banco de dados do WordPress */
define('DB_NAME', 'rtancman_blog');

/** Usuário do banco de dados MySQL */
define('DB_USER', 'rtancman');

/** Senha do banco de dados MySQL */
define('DB_PASSWORD', 'r4t4ncm4n@99');

/** nome do host do MySQL */
define('DB_HOST', '192.168.1.100');

/** Conjunto de caracteres do banco de dados a ser usado na criação das tabelas. */
define('DB_CHARSET', 'utf8');

/** O tipo de collate do banco de dados. Não altere isso se tiver dúvidas. */
define('DB_COLLATE', '');

/**#@+
 * Chaves únicas de autenticação e salts.
 *
 * Altere cada chave para um frase única!
 * Você pode gerá-las usando o {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * Você pode alterá-las a qualquer momento para desvalidar quaisquer cookies existentes. Isto irá forçar todos os usuários a fazerem login novamente.
 *
 * @since 2.6.0
 */
define('AUTH_KEY',         'b_>A,-C1Z]H2c928ObHi{4mJppkthz)R#0~8A4PZ,hV3g|I#8Ck^|Eiy+J{Ip-yL');
define('SECURE_AUTH_KEY',  'fX__j}5^.?,_*cSk+,E7aC$a]X;$v;=Z=32Tg~/euGh/6f*s7R@[&L+ %.COkG>[');
define('LOGGED_IN_KEY',    'VD)j-gk,CPTG+-?X_x/-sUPC.td-Ji1ob)1D=//Is .l>Lnr3Pp4X4[k_Xk0tT8+');
define('NONCE_KEY',        'ck3S2+Hh+E,)[gF$?8[{xU)v8[1Lce8k-v`U 6 6&/}Bj22IF[m+]X}`uYX]]5A+');
define('AUTH_SALT',        '?vnMc@S)FncDANP8{;QWz=TseAQX|x%A;U$|,_wCrR(kz0(WTWpH1{m+AS_UT|l ');
define('SECURE_AUTH_SALT', '1TGEBqJ}ChuGH1/p)z:^|kqV!  7Y-mEXUlL.=/{|kbW5+P{&XQ}6?)`EF,a%<eX');
define('LOGGED_IN_SALT',   '##l$Ml#EZn^Bb|OI|(=BY^uJQ*_5V-T9:P&V=?vyRl1vHTr.Qb`lj{aRj^DHFEsg');
define('NONCE_SALT',       'A*L}svY+@C7P[dn3blQZ[{mUzad,Sl*!- ]2?Y0MX_[*pk7_YG|~T9m-O++i5+.v');

/**#@-*/

/**
 * Prefixo da tabela do banco de dados do WordPress.
 *
 * Você pode ter várias instalações em um único banco de dados se você der para cada um um único
 * prefixo. Somente números, letras e sublinhados!
 */
$table_prefix  = 'wp_';

/**
 * O idioma localizado do WordPress é o inglês por padrão.
 *
 * Altere esta definição para localizar o WordPress. Um arquivo MO correspondente ao
 * idioma escolhido deve ser instalado em wp-content/languages. Por exemplo, instale
 * pt_BR.mo em wp-content/languages e altere WPLANG para 'pt_BR' para habilitar o suporte
 * ao português do Brasil.
 */
define('WPLANG', 'pt_BR');

/**
 * Para desenvolvedores: Modo debugging WordPress.
 *
 * altere isto para true para ativar a exibição de avisos durante o desenvolvimento.
 * é altamente recomendável que os desenvolvedores de plugins e temas usem o WP_DEBUG
 * em seus ambientes de desenvolvimento.
 */
define('WP_DEBUG', false);

/* Isto é tudo, pode parar de editar! :) */

/** Caminho absoluto para o diretório WordPress. */
if ( !defined('ABSPATH') )
	define('ABSPATH', dirname(__FILE__) . '/');
	
/** Configura as variáveis do WordPress e arquivos inclusos. */
require_once(ABSPATH . 'wp-settings.php');
