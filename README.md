# Individual Masters Project: Photo2Depth

A small application that takes as input, an image of a room interior 
and tries to segment out the furniture in the room and based on the
segmentation, generate a similar looking 3D scene, in terms of the
relative position of those furniture items. This means its trying
to estimate the depth and displacement of the objects, from the
viewing camera in the 3D scene, based only on one image input. 
**NOTE**: It assumes that all items lie on the same floor level. 
This project only supports the following furniture items when it 
comes to detectable furniture in an image: dining tables, chairs, 
couches, beds, ovens and refrigerators. It allows the user to 
input their desired image through a basic GUI.

## Usage

Set up a Python virtual environment by following this [guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
Then you can clone this repo and change directory into the main
level directory with:
```shell
cd individual-masters-project
```
After that, you need to import all the necessary packages. This 
can be done with:
```shell
pip install -r requirements.txt
```
This will install all the required packages. If for some reason, 
detectron2 fails to install, try to install it independently with 
the following command:
```shell
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
```

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)