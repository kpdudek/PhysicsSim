# PhysicsSim
Simulating 2D physics with Python.

## Installation
To run the game you will need to install:
* git
* python3
* pip3
* numpy
* PyQt5

## Controls
Spawn Ball: left mouse click and drag
Delete Ball: right mouse click
Camera Pan: arrow keys

#### *Ubuntu 18.04:*
```
sudo apt-get install git
git clone https://github.com/kpdudek/PhysicsSim.git
sudo apt-get install python3-pip
pip3 install PyQt5 
pip3 install numpy
```

#### *Windows 10:*
Download python >3.7 from the Microsoft Store and then use pip3 (included in the Microsoft Store download) to install PyQt5 and numpy.
Install git as described [here](https://www.computerhope.com/issues/ch001927.htm#:~:text=How%20to%20install%20and%20use%20Git%20on%20Windows,or%20fetching%20updates%20from%20the%20remote%20repository.%20)
```
git clone https://github.com/kpdudek/PhysicsSim.git
pip3 install PyQt5 
pip3 install numpy
```

### Developing
Ensure that you have a gcc compiler in order to build the required libraries.

To build the required libraries, run:
#### *Windows:*
```
gcc -fPIC -shared -o CollisionChecker.dll CollisionChecker.c
```
#### *Linux:*
```
gcc -fPIC -shared -o CollisionChecker.so CollisionChecker.c
```