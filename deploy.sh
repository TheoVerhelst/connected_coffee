mkdir -p /var/www/www.connectedcoffee.com/
cp frontend/* /var/www/www.connectedcoffee.com/
cp lighttpd.conf /etc/lighttpd/
/etc/init.d/lighttpd start
