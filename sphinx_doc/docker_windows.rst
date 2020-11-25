Docker set up for Windows
==========================

This setup guide is for docker project.

What to know before you install
------------------------------
System Requirements:

- Windows 10 64bit: Pro, Enterprise or Education (1607 Anniversary Update, Build 14393 or later).

- Virtualization is enabled in BIOS. Typically, virtualization is enabled by default. This is different from having Hyper-V enabled. For more detail see `Virtualization must be enabled <https://docs.docker.com/docker-for-windows/troubleshoot/#virtualization-must-be-enabled>`_. in Troubleshooting.

- CPU SLAT-capable feature.

- At least 4GB of RAM.

Note: If your system does not meet the requirements to run Docker Desktop for Windows, you can install Docker Toolbox `for windows <https://docs.docker.com/toolbox/toolbox_install_windows/>`_. , which uses Oracle Virtual Box instead of Hyper-V.        

Install and run Docker Desktop for windows
------------------------------------------

What the Docker Desktop for Windows install includes: The installation provides Docker Engine, Docker CLI client, Docker Compose, Docker Machine, and Kitematic

Download for windows : https://www.docker.com/products/docker-desktop


Docker Desktop for Windows and Docker Toolbox already include Compose along with other Docker apps, so most Windows users do not need to install Compose separately. 

Docker install instructions for these are here:

1.Double-click Docker Desktop for Windows Installer.exe to run the installer.

If you haven’t already downloaded the installer (Docker Desktop Installer.exe), you can get it from `download.docker.com <https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe>`_. It typically downloads to your Downloads folder, or you can run it from the recent downloads bar at the bottom of your web browser.

2.Follow the install wizard to accept the license, authorize the installer, and proceed with the install.

3.Click Finish on the setup complete dialog to launch Docker

official tutorial : https://docs.docker.com/docker-for-windows/

Project Application
-------------------

Clone or refresh the genomics-workspace::

    git clone -b genomics_docker  --single-branch https://github.com/NAL-i5k/genomics-workspace   
    
    cd genomics-workspace 
    
    docker-compose up 
 
    note : if it fail to connect postgrest use ctrl+c and then docker-compose up again.
