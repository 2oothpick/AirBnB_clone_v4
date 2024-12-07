from fabric import Connection, task

@task
def connect(c):
    conn = Connection('ubuntu@52.87.233.58')
    conn.put('100-hbnb.sql', remote='/home/ubuntu')
    conn.run('ls -la')
