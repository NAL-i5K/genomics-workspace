Apache (for production server)
------------------------------

Please note:
It is essential that tcp port 80 be open in your system. Sometimes the firewall may deny access to it.
Check if iptables will drop input packets in the output of this command::

    sudo iptables -L

If you see "INPUT" and "DROP" on the same line and no specific ACCEPT rule for tcp port 80
chances are web traffic will be blocked. Ask your sysadmin to open tcp ports 80 and 443 for http and https. Alternatively, check this `iptables guide`_.

.. _iptables guide: https://www.digitalocean.com/community/tutorials/how-to-set-up-a-basic-iptables-firewall-on-centos-6

Install Apache and related modules::

    sudo yum -y install httpd httpd-devel mod_ssl

Give the system a fully qualified domain name (FQDN) if needed::

    # Find out the system IP addres with 'ifconfig'.
    # Assuming it is a VM created by Vagrant, this could be 10.0.2.15.
    # Sudo edit '/etc/hosts' and add an address and domain name entry.
    # For example:
    10.0.2.15  virtualCentOS.local virtualCentOS

    # Sudo edit the file /etc/httpd/conf/httpd.conf,
    # and set the ServerName, for example:
    ServerName virtualCentOS.local:80

    # Set to start httpd at boot:
    sudo chkconfig httpd on

    # Check this setting if you wish, with:
    sudo chkconfig --list httpd

    # Control:
    #    sudo apachectl <command>
    # Where <command> can be:
    #     start         : Start httpd daemon.
    #     stop          : Stop httpd daemon.
    #     restart       : Restart httpd daemon, start it if not running.
    #     status        : Brief status report.
    #     graceful      : Restart without aborting open connections.
    #     graceful-stop : stop without aborting open connections.
    #
    # Start httpd daemon:
    sudo apachectl start

    # Test Apache:
    # If all is well. This command should produce copious
    # HTML output and in the first few lines you should see:
    #   '<title>Apache HTTP Server Test Page powered by CentOS</title>'
    curl localhost

    # You can also view the formatted Apache test page in your
    # browser, e.g., firefox http://<setup-machine-ip-address>
