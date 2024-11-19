# ShellsPathwayMD


## Introducción  
**_ShellsPathwayMD_** es una herramienta de análisis diseñada para estudiar el comportamiento de especies químicas en simulaciones de dinámica molecular segun su distribución espacial y temporal. Permite definir capas de multiples simetrias de espesor variable alrededor de puntos de referencia espaciales, como átomos, moléculas o centros de masa, y analizar la distribución de diferentes especies químicas dentro de estas capas. Esta herramienta es particularmente útil para estudiar fenómenos como la solvatación, la formación de complejos moleculares y la dinámica interfacial en sistemas biológicos y materiales.
- **Motivación:** Desarrollamos **_ShellsPathwayMD_** con el objetivo de estudiar la hidratación de iones en sistemas biológicos. Inicialmente, nos centramos en analizar la variación de la hidratación de iones sodio en función de su distancia a una molécula de ADN. Los resultados de este estudio se encuentran disponibles en el repositorio [2BNA_SPC-E_NaCl](https://github.com/tnavarrofebre/2BNA_SPC-E_NaCl).
- **Implementación:** La herramienta utiliza el programa [`gmx mindist`](https://manual.gromacs.org/current/onlinehelp/gmx-mindist.html) de **[GROMACS](https://www.gromacs.org/)** para calcular las distancias entre los átomos de referencia y los átomos de las especies a analizar. A partir de estos datos, se generan histogramas de los intervalos temporales en los cuales cada átomo objetivo permaneció en cada una de las capas predefinidas, utilizando el script [list_times.py](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/src/utils/scripts/list_times.py).  Con estas tablas se calculan funciones de distribución radial para cada capa. Para ello, se emplea el módulo [`gmx rdf`](https://manual.gromacs.org/current/onlinehelp/gmx-rdf.html) de **[GROMACS](https://www.gromacs.org/)**, aprovechando su capacidad para seleccionar subconjuntos de datos en función del tiempo.

### Características principales:
- **Definición flexible de capas:** Las capas se definen en función de atomos o particulas de referencia. Pueden ser átomos pertenecientes a las moleculas simuladas o _Dummy Particles_ de ello dependerá la simetria de las capas. Se puede definir la distancia minima y maxima respecto de los atomos de referencia dentro de la cual definir las capas en un numero tambien requerido al usuario. 
> [!CAUTION]  
> Los atomos de referencia deben tener sus posiciones restringidas. El comportamiento de este codigo es desconocido para referencias libres. 
- ***Histograma intervalos temporales respecto a posiciones.***
- ***Integración con [GROMACS](https://www.gromacs.org/):*** Utiliza modulos de gromacs y permanentemente se incorporarán mayor cantidad de modulos de analisis GMX compatibles.
- ***Minimos requicitos de sistema:***
    - GROMACS: Versión 2022 o superior.
    - Python 3 o superior: Con las siguientes librerías instaladas:
        - NumPy
- ***Libre*** 	:water_buffalo:

## Files tree
[ShellsPathwayMD](https://github.com/tnavarrofebre/ShellsPathwayMD)/       
├── [aditionals](https://github.com/tnavarrofebre/ShellsPathwayMD/tree/main/aditionals)         # Aditionals py scripts  
│   ├──[gro2stl.py](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/aditionals/gro2stl.py) #  
│   └──[cn-2.py](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/aditionals/cn-2.py) #   
├── [config.ini](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/config.ini)         # Configuration file for input parameters       
├── [Makefile](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/Makefile)             # Compilation and execution instructions      
├── [README.md](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/README.md)           # General documentation for the project        
├── [requirements.txt](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/requirements.txt)         # Python dependencies  
├── [src](https://github.com/tnavarrofebre/ShellsPathwayMD/tree/main/src)/          # Source code directory  
│   ├── [rdf_shell.sh](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/src/rdf_shell.sh)         # Shell script for RDF calculations related to the shell pathway        
│   ├── [utils](https://github.com/tnavarrofebre/ShellsPathwayMD/tree/main/src/utils)/          # Utility functions and modules  
│   │   ├── [scripts](https://github.com/tnavarrofebre/ShellsPathwayMD/tree/main/src/utils/scripts)/            # Scripts for data  processing and calculations    
│   │   │   ├── [data.py](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/src/utils/scripts/data.py)         # Data manipulation and processing functions     
│   │   │   ├── [list_times.py](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/src/utils/scripts/list_times.py)         # Script for listing time steps for analysis    
│   │   │   ├── [mean.py](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/src/utils/scripts/mean.py)         # Script for calculating mean values from data           
│   │   ├── [modules](https://github.com/tnavarrofebre/ShellsPathwayMD/tree/main/src/utils/modules)/            # Additional utility modules      
│   │   │   └── [process_files.py](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/src/utils/modules/process_files.py)           # Module for processing files in the project             
│  
└── [tests](https://github.com/tnavarrofebre/ShellsPathwayMD/tree/main/tests)/          # Test files directory (optional)      
│    ├── [NaCl_tests_box](https://github.com/tnavarrofebre/ShellsPathwayMD/tree/main/tests/NaCl_tests_box)/           # Test files for verification   
│    │   ├── [NaCl_tests_box.ndx](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/tests/NaCl_tests_box/NaCl_test_box.ndx)            # Index file for molecule selection in simulations       
│    │   ├── [NaCl_tests_box.gro](https://github.com/tnavarrofebre/ShellsPathwayMD/blob/main/tests/NaCl_tests_box/NaCl_test_box.gro)          # GROMACS configuration file for molecular dynamics     
│    │   ├── [NaCl_tests_box.xtc](http://redi.exactas.unlpam.edu.ar/xmlui/handle/2013/388)          # GROMACS trajectory file for molecular dynamics simulation  

## Instalación
> [!IMPORTANT]    
> Antes de comenzar la instalacion debes tener GROMACS 2022 o superior instalado.    
> [Guia de instalacion de GROMACS](https://manual.gromacs.org/2024.0/install-guide/index.html)  
1. Clona el repositorio:  
    ```
    git clone https://github.com/tnavarrofebre/ShellsPathwayMD  
    ``` 
2. Si lo deseas crea un entorno virtual:  
    ```
    python3 -m venv mi-entorno  
    source mi-entorno/bin/activate  
    ```
3. Instala los _requirements_:  

    ```make setup
    ```  
Si decidiste realizar la instalacion dentro de un entorno vistual no olvides inicializarlo cada vez que vayas a utilizar el este codigo.  
    ``source mi-entorno/bin/activate``
