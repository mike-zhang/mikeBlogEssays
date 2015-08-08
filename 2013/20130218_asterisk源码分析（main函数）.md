
文件：main目录下的asterisk.c文件

1、代码片段：

	/* if the progname is rasterisk consider it a remote console */
	if (argv[0] && (strstr(argv[0], "rasterisk")) != NULL) {
		ast_set_flag(&ast_options, AST_OPT_FLAG_NO_FORK | AST_OPT_FLAG_REMOTE);
	}
	...
	
	case 'r':
		ast_set_flag(&ast_options, AST_OPT_FLAG_NO_FORK | AST_OPT_FLAG_REMOTE);
		break;
			
说明：
	
	在终端运行rasterisk命令，相当于运行asterisk -r，即asterisk的远程连接。
	
	
	
2、代码片段:

	if (getenv("HOME")) 
		snprintf(filename, sizeof(filename), "%s/.asterisk_history", getenv("HOME"));
	

说明：
	rasterisk（或者asterisk -r）中运行的命令会记录在用户的home目录下的.asterisk_history文件中（比如：/root/.asterisk_history）
	
##asterisk启动参数

代码片段：

	case 'B': /* Force black background */
		ast_set_flag(&ast_options, AST_OPT_FLAG_FORCE_BLACK_BACKGROUND);
		ast_clear_flag(&ast_options, AST_OPT_FLAG_LIGHT_BACKGROUND);
		break;	

说明：
	-B
	强制以黑色背景运行，相当于将文件/etc/asterisk/asterisk.conf中的forceblackbackground设置为yes

	
代码片段：

	case 'X':
		ast_set_flag(&ast_options, AST_OPT_FLAG_EXEC_INCLUDES);
		break;

说明：
	-X
	可以在配置文件中配置"#exec "之类的指令（比如：#exec /tmp/shellTest.sh），相当于将在文件/etc/asterisk/asterisk.conf中配置execincludes = yes 
	
代码片段：
	
	case 'C':
		ast_copy_string(cfg_paths.config_file, optarg, sizeof(cfg_paths.config_file));
		ast_set_flag(&ast_options, AST_OPT_FLAG_OVERRIDE_CONFIG);
		break;
			
说明：
	-C file
	使用file替代/etc/asterisk/asterisk.conf文件初始化程序，这里的file应为绝对路径。
	
代码片段：
	
	case 'c':
		ast_set_flag(&ast_options, AST_OPT_FLAG_NO_FORK | AST_OPT_FLAG_CONSOLE);
		break;
			
说明：
	-c
	以console方式运行，相当于将在文件/etc/asterisk/asterisk.conf中配置console = yes
	
代码片段：

	case 'd':
		option_debug++;
		ast_set_flag(&ast_options, AST_OPT_FLAG_NO_FORK);
		break;

说明：		
	
	-d 或者 -ddd
	调试模式，d的个数即为调试级别，比如"-ddd"相当于在文件/etc/asterisk/asterisk.conf中配置debug = 3
	
代码片段：

	case 'e':
		if ((sscanf(&optarg[1], "%30ld", &option_minmemfree) != 1) || (option_minmemfree < 0)) {
			option_minmemfree = 0;
			}
		break;	

说明：
	
	-e memory
	相当于文件/etc/asterisk/asterisk.conf中配置 minmemfree = memory
	当系统中可用内存低于设定的memory值时，asterisk停止接收新的呼叫
	
代码片段：

	case 'F':
		ast_set_flag(&ast_options, AST_OPT_FLAG_ALWAYS_FORK);
		break;
	
说明：
	
	-F
	相当于在文件/etc/asterisk/asterisk.conf中配alwaysfork = yes
	
代码片段：
	
	case 'f':
			ast_set_flag(&ast_options, AST_OPT_FLAG_NO_FORK);
			break;
	
说明：
	
	-f
	相当于在文件/etc/asterisk/asterisk.conf中配nofork = yes
	
	
代码片段：

	case 'G':
		rungroup = ast_strdupa(optarg);
		break;

说明：
	
	-G group
	调用指定组运行
	

代码片段：

	case 'g':
		ast_set_flag(&ast_options, AST_OPT_FLAG_DUMP_CORE);
		break;
		
说明：

	-g
	故障转储相关
	
代码片段：

	case 'h':
		show_cli_help();
		exit(0);

说明：
	
	-h
	显示帮助信息

代码片段：

	case 'I':
		ast_set_flag(&ast_options, AST_OPT_FLAG_INTERNAL_TIMING);
		break;

说明：
	-I
	如果DAHDI计时器是可用则使内部定时
	
	
代码片段：

	case 'i':
		ast_set_flag(&ast_options, AST_OPT_FLAG_INIT_KEYS);
		break;
	
说明：

	-i
	在启动时初始化加密密钥
	
代码片段：

	case 'L':
		if ((sscanf(optarg, "%30lf", &option_maxload) != 1) || (option_maxload < 0.0)) {
			option_maxload = 0.0;
		}
		break;

说明：

	 -L <load>
	在拒绝新的电话之前限制最大平均负载

代码片段：

	case 'M':
		if ((sscanf(optarg, "%30d", &option_maxcalls) != 1) || (option_maxcalls < 0)) {
			option_maxcalls = 0;
		}
		break;

说明：	

	-M <value> 
	限制电话的最大数量为指定的值
	
代码片段：

	case 'm':
		ast_set_flag(&ast_options, AST_OPT_FLAG_MUTE);
		break;

说明：
	
	-m
	屏蔽在控制台输出
	

代码片段：

	case 'n':
		ast_set_flag(&ast_options, AST_OPT_FLAG_NO_COLOR);
		break;

说明：
	-n
	关闭彩色输出功能，比如：asterisk -n
	

代码片段：
	
	case 'p':
		ast_set_flag(&ast_options, AST_OPT_FLAG_HIGH_PRIORITY);
		break;
		
说明：
	
	-p
	作为伪实时线程运行
	
代码片段：
	
	case 'q':
		ast_set_flag(&ast_options, AST_OPT_FLAG_QUIET);
		break;

说明：
	
	-q
	安静模式(抑制输出)
	
代码片段：

	case 'R':
		ast_set_flag(&ast_options, AST_OPT_FLAG_NO_FORK | AST_OPT_FLAG_REMOTE | AST_OPT_FLAG_RECONNECT);
		break;
	
说明：
	
	 -R  
	 连接本机的asterisk服务器,断开后会重新连接
	 
	 
代码片段：
	
	case 'r':
		ast_set_flag(&ast_options, AST_OPT_FLAG_NO_FORK | AST_OPT_FLAG_REMOTE);
		break;
		
说明：
	
	-r
	连接本机的asterisk服务器
	
代码片段：

	case 's':
		remotesock = ast_strdupa(optarg);
		break;

说明：
	
	 -s <socket-file>
	 通过socket连接到asterisk，和r参数一起使用时有效
	 
代码片段：

	case 'T':
		ast_set_flag(&ast_options, AST_OPT_FLAG_TIMESTAMP);
		break;	

说明：

	-T
	在CLI输出中显示时间
	

代码片段：

	case 't':
		ast_set_flag(&ast_options, AST_OPT_FLAG_CACHE_RECORD_FILES);
		break;

说明：
	-t
	Record soundfiles in /var/tmp and move them where they belong after they are done
	
代码片段：

	case 'U':
		runuser = ast_strdupa(optarg);
		break;
	
说明：
	
	-U <user>
	以用户<user>方式运行
	
	
代码片段：

	case 'V':
		show_version();
		exit(0);

说明：
	
	-V 
	显示版本信息
	
代码片段：

		case 'v':
			option_verbose++;
			ast_set_flag(&ast_options, AST_OPT_FLAG_NO_FORK);
			break;

说明：
	
	-v
	多个v，显示更多信息
	


代码片段：

	case 'W': /* White background */
		ast_set_flag(&ast_options, AST_OPT_FLAG_LIGHT_BACKGROUND);
		ast_clear_flag(&ast_options, AST_OPT_FLAG_FORCE_BLACK_BACKGROUND);
		break;

说明：
	
	-W
	调整终端颜色
	
	
代码片段：

	case 'x':
		ast_set_flag(&ast_options, AST_OPT_FLAG_EXEC | AST_OPT_FLAG_NO_COLOR);
		xarg = ast_strdupa(optarg);
		break;	

说明：
	
	-x <cmd>
	执行CLI指令，和r参数一起使用，比如：asterisk -rx 'core show channels'
			
			
			
			
			
			
			
			
附：

enum ast_option_flags {
	/*! Allow \#exec in config files */
	AST_OPT_FLAG_EXEC_INCLUDES = (1 << 0),
	/*! Do not fork() */
	AST_OPT_FLAG_NO_FORK = (1 << 1),
	/*! Keep quiet */
	AST_OPT_FLAG_QUIET = (1 << 2),
	/*! Console mode */
	AST_OPT_FLAG_CONSOLE = (1 << 3),
	/*! Run in realtime Linux priority */
	AST_OPT_FLAG_HIGH_PRIORITY = (1 << 4),
	/*! Initialize keys for RSA authentication */
	AST_OPT_FLAG_INIT_KEYS = (1 << 5),
	/*! Remote console */
	AST_OPT_FLAG_REMOTE = (1 << 6),
	/*! Execute an asterisk CLI command upon startup */
	AST_OPT_FLAG_EXEC = (1 << 7),
	/*! Don't use termcap colors */
	AST_OPT_FLAG_NO_COLOR = (1 << 8),
	/*! Are we fully started yet? */
	AST_OPT_FLAG_FULLY_BOOTED = (1 << 9),
	/*! Trascode via signed linear */
	AST_OPT_FLAG_TRANSCODE_VIA_SLIN = (1 << 10),
	/*! Dump core on a seg fault */
	AST_OPT_FLAG_DUMP_CORE = (1 << 12),
	/*! Cache sound files */
	AST_OPT_FLAG_CACHE_RECORD_FILES = (1 << 13),
	/*! Display timestamp in CLI verbose output */
	AST_OPT_FLAG_TIMESTAMP = (1 << 14),
	/*! Override config */
	AST_OPT_FLAG_OVERRIDE_CONFIG = (1 << 15),
	/*! Reconnect */
	AST_OPT_FLAG_RECONNECT = (1 << 16),
	/*! Transmit Silence during Record() and DTMF Generation */
	AST_OPT_FLAG_TRANSMIT_SILENCE = (1 << 17),
	/*! Suppress some warnings */
	AST_OPT_FLAG_DONT_WARN = (1 << 18),
	/*! End CDRs before the 'h' extension */
	AST_OPT_FLAG_END_CDR_BEFORE_H_EXTEN = (1 << 19),
	/*! Use DAHDI Timing for generators if available */
	AST_OPT_FLAG_INTERNAL_TIMING = (1 << 20),
	/*! Always fork, even if verbose or debug settings are non-zero */
	AST_OPT_FLAG_ALWAYS_FORK = (1 << 21),
	/*! Disable log/verbose output to remote consoles */
	AST_OPT_FLAG_MUTE = (1 << 22),
	/*! There is a per-file debug setting */
	AST_OPT_FLAG_DEBUG_FILE = (1 << 23),
	/*! There is a per-file verbose setting */
	AST_OPT_FLAG_VERBOSE_FILE = (1 << 24),
	/*! Terminal colors should be adjusted for a light-colored background */
	AST_OPT_FLAG_LIGHT_BACKGROUND = (1 << 25),
	/*! Count Initiated seconds in CDR's */
	AST_OPT_FLAG_INITIATED_SECONDS = (1 << 26),
	/*! Force black background */
	AST_OPT_FLAG_FORCE_BLACK_BACKGROUND = (1 << 27),
};
			
			
			


			