#! /usr/bin/python3

import sys
import os
import random
import string
import docker
import glob
import flask
import psutil
import jinja2
import subprocess

APP_CONTAINER_NAME = 'nginx'
APP_SSL = 'True'
FREE_PORTS = range(60001,60999)
NGINX_CONFD_DIR = '/etc/nginx/conf.d/'

argv_flag = {};
def randomStr(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_busy_ports():
  busy_ports = []
  for conn in psutil.net_connections():
    busy_ports.append(conn.laddr[1])
  return (busy_ports)

def get_free_port():
  busy_ports = get_busy_ports()
  for port in FREE_PORTS:
    if port not in busy_ports:
      return port
      break

def docker_init():
  docker_client = docker.from_env()
  return(docker_client)

docker_client = docker_init()

#def argv_parser():
#  try:
#    argv_ = {param.split('=')[0][2:]:param.split('=')[1] for param in sys.argv[1:]}
#  except:
#    print ('Example: \n\t')
#    sys.exit(101)
#  return (argv_)

# 
#argv_flag = argv_parser()

#if argv_flag['port']:
#  get_free_port()

if len( sys.argv) <= 1:
  print ('Example: \nGet free port:\n\t ./nginx2docker.py freeport \nstart-demonize mode:\n\t  ./nginx2docker.py daemon')
  sys.exit(1)

if sys.argv[1] == 'freeport':
  print(get_free_port())
  sys.exit(0)

if sys.argv[1] == 'add-to-pool':
  #if sys.argv[2]
    server_name = sys.argv[2]
    container_name = sys.argv[3]
    free_port = get_free_port()
    fp = open(os.path.dirname( sys.argv[0] ) + '/nginx-template.j2','r')
    template = jinja2.Template (fp.read())
    try:
      f_nginx_conf  = open(NGINX_CONFD_DIR + server_name + '.autopool.conf','x')
    except FileExistsError:
      print('[Error] Nginx file config exist')
      sys.exit(1)
    else:
      docker_client.containers.run( container_name, 
                                    detach = True, 
                                    auto_remove = True, 
                                    ports = { '80/tcp':('127.0.0.1', free_port) },
                                    name = randomStr() + '_autopool' )
      pass
    finally:
      fp.close()
    f_nginx_conf.write (template.render(server_name = server_name,
                                        container_port = free_port,
                                        container_addr = '127.0.0.1'))
    f_nginx_conf.close()
    if (APP_SSL == 'True'):
      subprocess.call(['sudo','/usr/bin/certbot', '-n', '-d', server_name, '--nginx', '--redirect'])
    print ('Nginx reload .... ')
    subprocess.call(['sudo',"systemctl", "restart", "nginx"])
    print ('You domain? click here: https://'+server_name)
if sys.argv[1] == 'clean':
  for file_ in glob.glob(NGINX_CONFD_DIR+'*.autopool.conf'):
    os.remove(file_)
    

if sys.argv[1] == 'daemon':
#if argv_flag['daemon'] == 'on':
  app = flask.Flask(__name__)
  @app.route('/freeport')
  def flask_freeport():
    if (__name__ == "__main__"):
      app.run(host = '0.0.0.0', port=60000, debug=true)


