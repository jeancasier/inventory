file {'helloworld':
  ensure  => present,
  path    => '/tmp/helloworld',
  mode    => '0640',
  content => 'Helloworld via puppet ! '
}
