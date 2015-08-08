## windows环境下配置python脚本的开机启动
测试环境：windows Server 2003 R2
    
### 一、开始菜单启动项实现
用户必须登录才可执行。

测试脚本（python代码）：

	import time
	fout = open('e:\\1.txt','w')
	while True:
		tmp = '%d-%02d-%02d %02d:%02d:%02d \r\n' % time.localtime()[0:6]
		print tmp
		fout.write(tmp)
		fout.flush()
		time.sleep(5)

1、常规操作

1.1 创建快捷方式；

![创建快捷方式](images/20130204.1.1.PNG)

1.2 将创建的快捷方式放入开始菜单启动项；

![加入菜单启动项](images/20130204.1.2.PNG)

1.3、开机验证；

![运行效果](images/20130204.1.3.PNG)

2、隐藏命令行窗口启动

上述操作方法有命令行窗口，有些场合感觉不太实用，我们可以通过以下两种方式去掉命令行窗口。

2.1 将python脚本的文件扩展名改为".pyw"

![扩展名为pyw的快捷方式](images/20130204.1.4.PNG)

其它操作和上述过程类似，这里不再赘述。

2.2 通过vbs之类的脚本启动

vbs代码如下：

	Set ws = CreateObject("Wscript.Shell") 
	ws.run "cmd /c E:\test1.py",vbhide

路径根据具体情况进行配置,其它的和之前的操作类似，这里不再赘述。

如果不想用快捷方式的话，把脚本直接放入启动项也可以。

附：

配置账户自动登录

通过开始菜单启动项来实现的话，必须进行相应保证用户登录系统，这里介绍一种账户自动登录的方法。

	a、 在运行框中键入“Rundll32 netplwiz.dll,UsersRunDll”；
	
![配置自动登录1](images/20130204.1.5.PNG)
	
	b、 打开用户账户界面，将“要使用本机，用户必须输入用户名和密码”前面的勾去掉，按”确定“后输入需要自动登录的用户名和密码；
	
![配置自动登录2](images/20130204.1.6.PNG)
	

二、开机脚本

	不能用循环，最好配置超时时间。
	测试代码（python）：

	import time
	fout = open('e:\\1.txt','w')
	tmp = '%d-%02d-%02d %02d:%02d:%02d \r\n' % time.localtime()[0:6]
	print tmp
	fout.write(tmp)
	fout.close()

	

	步骤如下：	
	a、运行中输入gpedit.msc打开组策略编辑器；
	b、选择“计算机配置”=>“Windows 设置”=>“脚本”=>“启动”选项；

![选择启动脚本](images/20130204.1.7.PNG)	
	c、选择脚本；

![选择脚本](images/20130204.1.8.PNG)		
	d、配置脚本最长等待时间，路径为“计算机配置”=>“管理模版”=>“系统”=>“脚本”=>“组策略脚本的最长等待时间”；

![脚本最长等待时间](images/20130204.1.9.PNG)			


三、通过一个服务调用该脚本

a、编写脚本启动服务serviceStartShell，代码如下：

	#include <windows.h>
	#include <stdio.h>
	#include <tchar.h>
	#include <shellapi.h>

	#include <string>

	using std::string;

	#pragma comment (lib, "advapi32.lib")
	#pragma comment (lib, "user32.lib")
	#pragma comment (lib, "Shell32.lib")

	HKEY hKeyRoot = HKEY_LOCAL_MACHINE;
	LPCTSTR data_Set = "SYSTEM\\CurrentControlSet\\Services\\ServiceStartShell";
	const char *strValueName = "strFilePath";
	const char *strValueName2 = "strParams";
	const char *taskkillPath = "C:\\Windows\\System32\\taskkill.exe";

	TCHAR szServiceName[] = _T("ServiceStartShell");
	BOOL bInstall;
	SERVICE_STATUS_HANDLE hServiceStatus;
	SERVICE_STATUS status;
	DWORD dwThreadID;

	BOOL writeReg(const char* filePath,const char* strParams)
	{
		HKEY hKEY;

		long ret0=(RegOpenKeyEx(hKeyRoot,data_Set,0,KEY_ALL_ACCESS,&hKEY));
		if(ret0!=ERROR_SUCCESS)
			return FALSE;
		
		DWORD type_1=REG_SZ;	
		long ret = RegSetValueEx(hKEY,strValueName,NULL,type_1,(BYTE*)filePath,string(filePath).length()+1);
		if(ret != ERROR_SUCCESS)
			return FALSE;

		ret = RegSetValueEx(hKEY,strValueName2,NULL,type_1,(BYTE*)strParams,string(strParams).length()+1);
		if(ret != ERROR_SUCCESS)
			return FALSE;
		
		RegCloseKey(hKEY);
	}

	BOOL readReg(const char* filePath,const char* strParams)
	{
		HKEY hKEY;

		long ret = RegOpenKeyEx(hKeyRoot,data_Set,0,KEY_READ,&hKEY);
		if(ret != ERROR_SUCCESS)
			return FALSE;
		
		DWORD type_1=REG_SZ;
		DWORD cbData_1=1024;

		ret = RegQueryValueEx(hKEY,strValueName,NULL,&type_1,(BYTE*)filePath,&cbData_1);
		if(ret != ERROR_SUCCESS)
			return FALSE;
		
		ret = RegQueryValueEx(hKEY,strValueName2,NULL,&type_1,(BYTE*)strParams,&cbData_1);
		if(ret != ERROR_SUCCESS)
			return FALSE;	

		RegCloseKey(hKEY);
	}

	void Init()
	{
		hServiceStatus = NULL;
		status.dwServiceType = SERVICE_WIN32_OWN_PROCESS;
		status.dwCurrentState = SERVICE_STOPPED;
		status.dwControlsAccepted = SERVICE_ACCEPT_STOP;
		status.dwWin32ExitCode = 0;
		status.dwServiceSpecificExitCode = 0;
		status.dwCheckPoint = 0;
		status.dwWaitHint = 0;
	}

	void runShell(const char *filePath,const char *strParams)
	{	
		SHELLEXECUTEINFO shExecInfo;
		shExecInfo.cbSize = sizeof(SHELLEXECUTEINFO);
		shExecInfo.fMask = NULL;
		shExecInfo.hwnd = NULL;
		shExecInfo.lpVerb = "";      
		//shExecInfo.lpFile = "c:\\python27\\python.exe";
		shExecInfo.lpFile = filePath;
		//shExecInfo.lpParameters = "e:\\test1.py";
		shExecInfo.lpParameters = strParams;
		shExecInfo.lpDirectory = NULL;
		shExecInfo.nShow = SW_NORMAL;
		shExecInfo.hInstApp = NULL;
		ShellExecuteEx(&shExecInfo);
	}

	string getProcessNameByPath(const char* filePath)
	{
		string strFilePath = filePath;	
		int lable1 = 0;
		lable1 = strFilePath.rfind('\\');	
		if ( lable1 != string::npos && lable1 != strFilePath.length())
			strFilePath = strFilePath.substr(lable1+1);	
		return strFilePath;		
	}

	void killProcess(const char* processName)
	{
		// TASKKILL  /F /IM NOTEPAD.EXE /T
		char strCmd[1024] = {0};
		sprintf(" /F /IM %s /T",processName);	
		runShell(taskkillPath,strCmd);	
	}

	void WINAPI ServiceStrl(DWORD dwOpcode)
	{
		switch (dwOpcode)
		{
		case SERVICE_CONTROL_STOP:
			status.dwCurrentState = SERVICE_STOP_PENDING;
			SetServiceStatus(hServiceStatus, &status);
			PostThreadMessage(dwThreadID, WM_CLOSE, 0, 0);
			break;
		case SERVICE_CONTROL_PAUSE:
			break;
		case SERVICE_CONTROL_CONTINUE:
			break;
		case SERVICE_CONTROL_INTERROGATE:
			break;
		case SERVICE_CONTROL_SHUTDOWN:
			break;
		default:
			//printf("Bad service request");
			;
		}
	}

	void WINAPI ServiceMain(int argc,char* argv[])
	{
		// Register the control request handler
		status.dwCurrentState = SERVICE_START_PENDING;
		status.dwControlsAccepted = SERVICE_ACCEPT_STOP;	
		hServiceStatus = RegisterServiceCtrlHandler(szServiceName, ServiceStrl);
		if (hServiceStatus == NULL)
		{
			//printf("Handler not installed");
			return;
		}
		SetServiceStatus(hServiceStatus, &status);

		status.dwWin32ExitCode = S_OK;
		status.dwCheckPoint = 0;
		status.dwWaitHint = 0;
		status.dwCurrentState = SERVICE_RUNNING;
		SetServiceStatus(hServiceStatus, &status);

		// task to do

		char filePath[128],strParams[128];
		readReg(filePath,strParams);
		runShell(filePath,strParams);
		//runShell("c:\\python27\\python.exe","e:\\test1.py");

		while(true)
		{
			if (SERVICE_STOP_PENDING == status.dwCurrentState)
			{	
				//system("TASKKILL  /F /IM python.exe /T");
				char strCmd[1024] = {0};
				sprintf(strCmd,"TASKKILL  /F /IM %s /T",getProcessNameByPath(filePath).c_str());
				system(strCmd);							
				break;
			}
			Sleep(500);
		}	

		status.dwCurrentState = SERVICE_STOPPED;
		SetServiceStatus(hServiceStatus, &status);
		//printf("Service stopped");
	}

	BOOL IsInstalled()
	{
		BOOL bResult = FALSE;		
		SC_HANDLE hSCM = OpenSCManager(NULL, NULL, SC_MANAGER_ALL_ACCESS);

		if (hSCM != NULL)
		{		
			SC_HANDLE hService = OpenService(hSCM, szServiceName, SERVICE_QUERY_CONFIG);
			if (hService != NULL)
			{
				bResult = TRUE;
				CloseServiceHandle(hService);
			}
			CloseServiceHandle(hSCM);
		}
		return bResult;
	}

	BOOL Install(const char* filePath,const char* strParams)
	{
		if (IsInstalled())
			return TRUE;
		
		SC_HANDLE hSCM = OpenSCManager(NULL, NULL, SC_MANAGER_ALL_ACCESS);
		if (hSCM == NULL)
			return FALSE;

		// Get the executable file path
		TCHAR szFilePath[MAX_PATH];
		GetModuleFileName(NULL, szFilePath, MAX_PATH);

		SC_HANDLE hService = CreateService(
			hSCM, szServiceName, szServiceName,
			SERVICE_ALL_ACCESS, SERVICE_WIN32_OWN_PROCESS,
			SERVICE_DEMAND_START, SERVICE_ERROR_NORMAL,
			szFilePath,NULL,NULL,NULL,NULL,NULL);     

		if (hService == NULL)
		{
			CloseServiceHandle(hSCM);
			return FALSE;
		}
		CloseServiceHandle(hService);
		CloseServiceHandle(hSCM);
		return TRUE;
	}

	BOOL Uninstall()
	{
		if (!IsInstalled())
			return TRUE;

		SC_HANDLE hSCM = OpenSCManager(NULL, NULL, SC_MANAGER_ALL_ACCESS);

		if (hSCM == NULL)
			return FALSE;

		SC_HANDLE hService = OpenService(hSCM, szServiceName, SERVICE_STOP | DELETE);
		if (hService == NULL)
		{
			CloseServiceHandle(hSCM);	
			return FALSE;
		}
		SERVICE_STATUS status;
		ControlService(hService, SERVICE_CONTROL_STOP, &status);
			
		BOOL bDelete = DeleteService(hService);
		CloseServiceHandle(hService);
		CloseServiceHandle(hSCM);

		if (bDelete)
			return TRUE;
		//printf("Service could not be deleted");
		return FALSE;
	}

	int main(int argc,char* argv[])
	{
		Init();
		dwThreadID = GetCurrentThreadId();
		SERVICE_TABLE_ENTRY st[] =
		{
			{ szServiceName, (LPSERVICE_MAIN_FUNCTION)ServiceMain },
			{ NULL, NULL }
		};
		//printf("argc = %d \n",argc);
		if((4 == argc) && 0 == stricmp(argv[3],"/install") )
		{
			Install(argv[1],argv[2]);
			writeReg(argv[1],argv[2]);
		}
		else if ((2 == argc) && 0 == stricmp(argv[1], "/uninstall") ) 
		{
			Uninstall();
		}
		else
		{
			if (!StartServiceCtrlDispatcher(st))
			{
				//printf("Register Service Main Function Error!");
			}
		}
		return 0;
	}

b、服务安装；

	serviceStartShell.exe C:\Python27\python.exe e:\test1.py /install
	
c、服务卸载；

	serviceStartShell.exe  /uninstall
	

附：

	linux下：
	vi /etc/rc.d/rc.local
	比如：
	/usr/bin/python /tmp/test1.py &
	
	chkconfig sshd on
	chkconfig | grep sshd
	chkconfig sshd off
	 

