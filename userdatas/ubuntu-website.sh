#!/bin/bash

sudo apt -y update && sudo apt -y upgrade
sudo apt -y install apache2
cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html>
<body>
<h1>discro kangaroo.com</h1>
</body>
</html>
EOF
sudo systemctl enable apache2
systemctl start apache2

