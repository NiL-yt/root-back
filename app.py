import pymysql
from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def first():
    return render_template('index.html')


@app.route('/data', methods=['GET'])
def get_data():
    # 建立数据库连接
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Root1234!',
        db='student'
    )
    try:
        with connection.cursor() as cursor:
            # 执行 SQL 查询
            sql = "SELECT college, COUNT(*) as number FROM stu GROUP BY college"
            cursor.execute(sql)
            # 获取查询结果
            result = cursor.fetchall()
            # 将结果转为字典
            data = [{"name": row[0], "value": row[1]} for row in result]
    finally:
        # 关闭数据库连接
        connection.close()

    # 以 JSON 格式返回数据
    return jsonify(data)


@app.route('/student')
def student():
    # 建立数据库连接
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Root1234!',
        db='student'
    )
    try:
        with connection.cursor() as cursor:
            # 获取表结构信息
            table_name = 'stu'
            cursor.execute(f"DESCRIBE {table_name}")
            table_info = cursor.fetchall()
            field_names = [row[0] for row in table_info]

            # 获取查询参数
            search_fields = [field for field in field_names if request.args.get(field, '')]
            query_params = []
            query_values = []
            print(search_fields, query_values, query_params)
            if search_fields:
                query_params = [f"{field} LIKE %s" for field in search_fields]
                query_values = ['%' + request.args.get(field, '') + '%' for field in search_fields]
                print(search_fields, query_values, query_params)

            # 构建SQL查询语句
            select_sql = f"SELECT * FROM {table_name}"
            if query_params:
                where_conditions = " AND ".join(query_params)
                select_sql += f" WHERE {where_conditions}"

            # 执行SQL查询
            try:
                if query_params:
                    cursor.execute(select_sql, query_values)
                else:
                    cursor.execute(select_sql)
            except Exception as e:
                print(f"执行 SQL 语句时发生错误: {e}")

            # 获取查询结果
            table_data = cursor.fetchall()

            # 分页处理
            page = request.args.get('page', 1, type=int)
            per_page = 10
            num_pages = len(table_data) // per_page + (len(table_data) % per_page > 0)
            start_idx = (page - 1) * per_page
            end_idx = min(start_idx + per_page, len(table_data))
            current_page_data = table_data[start_idx:end_idx]

    finally:
        cursor.close()
        connection.close()

    return render_template(
        'student.html',
        field_names=field_names,
        table_data=current_page_data,
        page=page,
        num_pages=num_pages,
        search_fields=search_fields,
    )


@app.route('/teacher')
def teacher():
    # 建立数据库连接
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Root1234!',
        db='teacher'
    )
    try:
        with connection.cursor() as cursor:
            # 获取表结构信息
            table_name = 'tch'
            cursor.execute(f"DESCRIBE {table_name}")
            table_info = cursor.fetchall()
            field_names = [row[0] for row in table_info]

            # 获取查询参数
            search_fields = [field for field in field_names if request.args.get(field, '')]
            query_params = []
            query_values = []
            print(search_fields, query_values, query_params)
            if search_fields:
                query_params = [f"{field} LIKE %s" for field in search_fields]
                query_values = ['%' + request.args.get(field, '') + '%' for field in search_fields]
                print(search_fields, query_values, query_params)

            # 构建SQL查询语句
            select_sql = f"SELECT * FROM {table_name}"
            if query_params:
                where_conditions = " AND ".join(query_params)
                select_sql += f" WHERE {where_conditions}"

            # 执行SQL查询
            try:
                if query_params:
                    cursor.execute(select_sql, query_values)
                else:
                    cursor.execute(select_sql)
            except Exception as e:
                print(f"执行 SQL 语句时发生错误: {e}")

            # 获取查询结果
            table_data = cursor.fetchall()

            # 分页处理
            page = request.args.get('page', 1, type=int)
            per_page = 10
            num_pages = len(table_data) // per_page + (len(table_data) % per_page > 0)
            start_idx = (page - 1) * per_page
            end_idx = min(start_idx + per_page, len(table_data))
            current_page_data = table_data[start_idx:end_idx]

    finally:
        cursor.close()
        connection.close()

    return render_template(
        'teacher.html',
        field_names=field_names,
        table_data=current_page_data,
        page=page,
        num_pages=num_pages,
        search_fields=search_fields,
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
