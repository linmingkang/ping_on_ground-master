/*
 * 需要修改的地方为下面注释的6个地方
 * 按照示例修改
*/

#include <stdio.h>
#include <stdlib.h>
#include <time.h> 
#include <dirent.h>
#include <sys/types.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <sys/param.h>
#include <sys/stat.h>

using namespace std;

#define READ_BUF_SIZE 1024
#define pidName "ping_on_ground"//进程名

char pid[10];

void init_daemon(void);

int get_pid(void);

int main() 
{ 
	FILE *fp; 

	time_t t;
	
	init_daemon();

	while(1)
	{
		
		int i = 0;
		
		i = get_pid();

		if (i == 0 )

		{	
			if((fp=fopen("/home/chsr/log.d/daemon_ping_on_ground.log","a")) >=0)//看门狗日志路径
			{ 
		
				t=time(0); 
			
				fprintf(fp,"ping_on_ground don't exist at %s\n",asctime(localtime(&t)));//进程名

				int ret = 0;
				
				char s[500];

				const char *command = "python3 /home/chsr/bin/ping_on_ground.py";//执行进程的指令
				
				memset(s,0,sizeof(s));
				
				strcpy(s,command);

				ret = system(s);
				
				if( ret < 0)
				{
					
		
						t=time(0); 
			
						fprintf(fp,"ping_on_ground reboot failed at %s\n",asctime(localtime(&t)));//进程名

					
				}else
				{
					
		
						t=time(0); 
			
						fprintf(fp,"ping_on_ground reboot succeed at %s\n",asctime(localtime(&t)));//进程名

				}

				fclose(fp);
			}
				
			
		}

        sleep(5);
	}
		
} 


int get_pid(void)
{
	DIR *dir;
	struct dirent *next;
	int i=0;
	FILE *status;
	char buffer[READ_BUF_SIZE];
	char name[READ_BUF_SIZE];
	dir=opendir("/proc");
	if(!dir){
		printf("Can't open /proc\n");
		return 0;
		}
	while((next=readdir(dir))!=NULL){
		if((strcmp(next->d_name,"..")==0||strcmp(next->d_name,".")==0)){
			continue;
			}
		if(!isdigit(*next->d_name)){
			continue;
			}
		sprintf(buffer,"/proc/%s/status",next->d_name);
		if(!(status=fopen(buffer,"r"))){
			continue;
			}
		if(fgets(buffer,READ_BUF_SIZE,status)==NULL){
			fclose(status);
			continue;
			}
		fclose(status);
		sscanf(buffer,"%*s%s",name);
		if(strcmp(name,pidName)==0){
			//printf("%s\n",next->d_name);
			strcpy(pid,next->d_name);
			printf("%s\n",pid);
			i = 1;
			}
		}
	closedir(dir);
	return i;
}

void init_daemon(void)
{
    int pid;

    int i;

    if( (pid=fork()) )

        exit(0);

    else if(pid< 0)

        exit(1);


    setsid();


    if( (pid=fork()) )

        exit(0);

    else if(pid< 0)

        exit(1);


    for(i=0;i< NOFILE;++i)
        close(i);


    chdir("/");

    umask(0);

    return;
}
