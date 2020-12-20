# GameList

```powershell
pip install -r requirements.txt # install dependency(pygame, pynput)
```

##### Menu.py에서 실행 후 버튼으로 게임 실행

게임이 실행되었을 때, menu.py는 멈추는 상태.

게임을 정상적으로 종료하면 다시 menu.py 사용 가능

menu에서 버튼을 클릭했을 때 게임이 실행이 안되고 다음과 같은 오류 메세지를 보여줄 때

```powershell
[Errno 2] No such file or directory 
#Path 경로 수정
#print(os.getcwd())를 통해서 현재 path를 알아보고, 
#subprocess.call('python', './pang.py') 에서 현재 path에서부터 .py을 실행할 수 있게 두번째 부분을 수정한다.
```



