# multi_robot_ros2
Simulación multi-robot homogénea y heterogénea en ROS 2 con Gazebo. Contiene los archivos necesarios para lanzar tanto la simulación como la visualización de ambos sistemas multi-robot. No es necesaria compilación.

## Instrucciones
Es necesario tener instalado ROS 2 en el sistema, en este caso la distribución Humble. Se recomienda usar Docker.

Asegurarse de crear un espacio de trabajo vacío primero. Dentro de este hay que ejecutar los siguientes comandos:
```
git clone https://github.com/Alvar007/multi_robot_ros2.git .
source install/setup.bash
```
#### Lanzar sistema multi-robot homogéneo:
```
ros2 launch localization_server multi-homo.launch.py
```
#### Lanzar sistema multi-robot heterogéneo:
```
ros2 launch localization_server multi-hetero.launch.py
```
