#!/usr/bin/env python

from apps import app, blueprint

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8001', debug=True)
    host='0.0.0.0'#这里使用0.0.0.0不然外面不能访问
    port='8001' #这里使用的端口号为8001 根据你自己的需求设置端口号