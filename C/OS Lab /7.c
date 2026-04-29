#include<stdio.h>
#include<unistd.h>
int main(){
int x = fork();
if(x==0){
printf(" Hello: I am child process\n");
}
else if(x >0){
printf(" Hello: I am parent process\n");
}
}