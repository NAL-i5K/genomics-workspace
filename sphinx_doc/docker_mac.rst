Docker setup for mac
====================

This setup guide is for docker project.

What to know before you install
-------------------------------

System Requirements: 

1.Mac hardware must be a 2010 or newer model, with Intel’s hardware support for memory management unit (MMU) virtualization, including Extended Page Tables (EPT) and Unrestricted Mode. You can check to see if your machine has this support by running the following command in a terminal: sysctl kern.hv_support

2.macOS Sierra 10.12 and newer macOS releases are supported. We recommend upgrading to the latest version of macOS.

3.At least 4GB of RAM

4.VirtualBox prior to version 4.3.30 must NOT be installed (it is incompatible with Docker Desktop for Mac). If you have a newer version of VirtualBox installed, it’s fine

Note: If your system does not satisfy these requirements, you can install `Docker Toolbox <https://docs.docker.com/toolbox/toolbox_install_mac/>`_., which uses Oracle VirtualBox instead of HyperKit.

What the install includes: The installation provides `Docker Engine <https://docs.docker.com/engine/userguide/>`_.,Docker CLI client, `Docker Compose <https://docs.docker.com/compose/overview/>`_., `Docker Machine <https://docs.docker.com/machine/overview/>`_., and `Kitematic <https://docs.docker.com/kitematic/userguide/>`_.

Install and run Docker Desktop for Mac
--------------------------------------
1.Double-click  Docker.dmg  to open the installer, then drag Moby the whale to the Applications foldert 

2.Double-click  Docker.app  in the Applications folder to start Docker.

3.Click the whale (whale menu) to get Preferences and other options.

offical tutorial : https://docs.docker.com/docker-for-mac/

Project Applications
--------------------

Clone or refresh the genomics-workspace::

    git clone -b genomics_docker  --single-branch https://github.com/NAL-i5k/genomics-workspace   
    
    cd genomics-workspace 
    
    docker-compose up 

    note : if it fail to connect postgrest use ctrl+c and then docker-compose up again. 
