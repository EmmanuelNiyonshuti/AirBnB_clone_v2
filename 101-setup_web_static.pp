# This Puppet manifest sets up web servers for the deployment of web_static

# Install Nginx if not already installed
package { 'nginx':
  ensure          => 'installed',
  provider        => 'apt',
  install_options => ['-y'],
}

# Ensure the directories are created
file { '/data/':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
  recurse => true,
}

file { '/data/web_static':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/shared':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create a test HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}
#remove symbolic link if it already exists
file {'/data/web_static/current':
    ensure => 'absent',
}

file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  require => File['/data/web_static/releases/test'],
}

# Update Nginx configuration
file_line { 'nginx_hbnb_static':
  path  => '/etc/nginx/sites-available/default',
  line  => 'location /hbnb_static { alias /data/web_static/current; }',
  after => 'server_name _;',
}

# Ensure Nginx config test and reload
exec { 'nginx_reload':
  command     => '/usr/sbin/nginx -t && /usr/sbin/service nginx reload',
  refreshonly => true,
  subscribe   => File['/etc/nginx/sites-available/default'],
}
