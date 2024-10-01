# CrazyDriver

2024대동제\_전자오락실 부스 전시 게임

REF. "Do it! 게임 10개 만들며 배우는 파이썬" 을 참조하여 만든 CrazyDriver 게임입니다.

pyinstaller 설치 후 아래의 명령을 사용하여 빌드합니다.
```
pyinstaller --onefile --add-data "GameImages;GameImages" --add-data "Dontstopme.mp3;." --add-data "score.txt;." main.py
```