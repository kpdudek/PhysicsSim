# PhysicsSim
Simulating 2D physics with Python.

## Toolchain
To run the game you need python3, pip3, numpy, and PyQt5.

#### *Ubuntu 18.04:*
```
sudo apt-get install git
git clone https://github.com/kpdudek/PhysicsSim.git
sudo apt-get install python3-pip
pip3 install PyQt5 
pip3 install numpy
```

#### *Windows 10:*
Download python >3.7 from the Microsoft Store and then use pip3 to install PyQt5 and numpy from PowerShell.
Install git as described [here](https://www.computerhope.com/issues/ch001927.htm#:~:text=How%20to%20install%20and%20use%20Git%20on%20Windows,or%20fetching%20updates%20from%20the%20remote%20repository.%20)
```
git clone https://github.com/kpdudek/PhysicsSim.git
pip3 install PyQt5 
pip3 install numpy
```

### Developing
Ensure that you have the gcc compiler (MinGW if you're on windows)

To build the collision checking library run
#### *Windows:*
```
gcc -fPIC -shared -o .\CollisionChecker.dll .\CollisionChecker.c
```
#### *Linux:*
```
gcc -fPIC -shared -o .\CollisionChecker.so .\CollisionChecker.c
```