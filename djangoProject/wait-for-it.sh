#!/bin/bash

# 使用Python脚本检查MySQL连接
check_db() {
python3 << END
import sys
import time
import MySQLdb

try:
    MySQLdb.connect(
        host="mysql",
        user="root",
        passwd="123717",
        db="commodity_system"
    )
    print("Database connection successful!")
    sys.exit(0)
except Exception as e:
    print(f"Database connection failed: {e}")
    sys.exit(1)
END
}

# 尝试连接数据库
echo "Waiting for MySQL to be available..."
until check_db; do
    echo "MySQL is unavailable - sleeping"
    sleep 1
done

# 执行数据库迁移
python manage.py makemigrations -v 0
python manage.py migrate -v 0

# 启动应用 - 关键修改在这里
if [ $# -eq 0 ]; then
    echo "No command provided, starting Django server..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "Executing provided command..."
    exec "$@"
fi
