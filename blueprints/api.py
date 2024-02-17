from flask import Blueprint, request, session, send_from_directory
from util import util
from util.sql import Sql
from config import config

api = Blueprint("bp_api", __name__, url_prefix="/api")


@api.route('/login', methods=["post"])
def api_login():
    
    
    util.mkdir_same_day_dir()

    if util.is_login(session):
        
        return {"status": "ok", "msg": "logged in"}

    username = request.form.get("username")
    password = request.form.get("password")

    if username == config["admin"] and password == config["password"]:
        session["admin"] = config["admin"]
        return {"status": "ok", "meg": "logged in"}
    else:
        return {"status": "no", "meg": "not logged in"}, 403


@api.route('/logout', methods=["post"])
def api_logout():
    
    session.clear()
    return {"status": "ok", "mess": "You have logged out"}


@api.route('/image/<string:string>', methods=["get"])
def api_image(string):
    sql = Sql().connect("util/sql")

    if util.is_login(session):
        
        result = sql.select_photo_md_name(string)
        if result:
            return send_from_directory(result[3], result[4])
        return "404 NOT FOUND", 404

    
    code = request.args.get("code")

    if not code or code == "" or code == " ":
        
        result = sql.select_photo_md_name_auth(string, "anonymity")
        if result:
            return send_from_directory(result[3], result[4])

        return {"msg": "权限不够，Insufficient permissions", "code": 403}

    select = sql.select_access_code(code)

    if not select:
        
        return {"msg": "err"}
    if select[1] == "admin":
        
        result = sql.select_photo_md_name(string)
        if result:
            return send_from_directory(result[3], result[4])
        return "404 NOT FOUND", 404

    
    result = sql.select_photo_md_name_auth(string, select[1])
    if result:
        return send_from_directory(result[3], result[4])
    return {"msg": "权限不够，Insufficient permissions", "code": 403}


@api.route("/upload", methods=["post"])
def api_upload():
    
    if not util.is_login(session):
        
        return {"status": "ok", "meg": "not logged in"}, 403

    args = request.form.to_dict()
    files = request.files.to_dict()

    image = files.get("image")
    filename = image.filename

    md_name = util.get_random_md5(filename)
    path = util.get_same_day_dir()
    suffix = filename.split(".")[-1]

    sql = Sql().connect("util/sql")
    sql.insert_image(
        md_name, path, f"/image/{md_name}", f"{md_name}.{suffix}", suffix, args["user"], args["type"]
    )
    image.save(util.concatenated_file_name(path, f"{md_name}.{suffix}"))  
    return {"code": 200, "msg": "上传成功"}


@api.route("/image/range", methods=["post"])
def api_image_range():
    
    if not util.is_login(session):
        
        return {"status": "ok", "meg": "not logged in"}, 403

    limit = request.form.get("limit")
    offset = request.form.get("offset")

    sql = Sql().connect("util/sql")
    return sql.select_photo_range(limit, offset)


@api.route("/image/types", methods=["post"])
def api_image_types():
    
    if not util.is_login(session):
        
        return {"status": "ok", "meg": "not logged in"}, 403

    sql = Sql().connect("util/sql")
    types = sql.select_types()

    return types


@api.route("/type/image/range", methods=["post"])
def type_image_range():
    
    if not util.is_login(session):
        
        return {"status": "ok", "meg": "not logged in"}, 403

    photo_type = request.form.get("type")
    limit = request.form.get("limit")
    offset = request.form.get("offset")

    
    if photo_type == "default":
        photo_type = ""

    sql = Sql().connect("util/sql")

    if photo_type == "user" or photo_type == "anonymity" or photo_type == "admin":
        
        return sql.select_authority_photo_range(photo_type, limit, offset)

    return sql.select_type_photo_range(photo_type, limit, offset)


@api.route("/type/link/<string:photo_type>", methods=["get"])
def types_link(photo_type):
    

    sql = Sql().connect("util/sql")
    if photo_type == "default":
        select = sql.select_type_photo("")
        if select:
            return send_from_directory(select[3], select[4])
    elif photo_type == "anonymity":
        select = sql.select_authority_photo("anonymity")
        if select:
            return send_from_directory(select[3], select[4])
    elif photo_type == "user" or photo_type == "admin":
        
        code = request.args.get("code")
        if not code or code == "" or code == " ":
            return {"msg": "权限不够，Insufficient permissions", "code": 403}, 403
        select = sql.select_access_code(code)
        if not select or select[1] != photo_type:
            return {"msg": "权限不够，访问码错误Insufficient permissions", "code": 403}, 403
        select = sql.select_authority_photo(photo_type)
        if select:
            return send_from_directory(select[3], select[4])
    else:
        select = sql.select_type_photo(photo_type)
        if select:
            return send_from_directory(select[3], select[4])

        return {"status": "ok", "meg": "not type"}


@api.route("/image/length", methods=["post"])
def image_length():
    
    if not util.is_login(session):
        
        return {"status": "ok", "meg": "not logged in"}, 403

    sql = Sql().connect("util/sql")
    select = sql.get_photo_length()
    if select != 0:
        return [select]
    return [0]


@api.route("/type/image/length", methods=["post"])
def types_length():
    
    if not util.is_login(session):
        
        return {"status": "ok", "meg": "not logged in"}, 403

    photo_type = request.form.get("type")

    if photo_type == "default":
        photo_type = ""
    sql = Sql().connect("util/sql")

    
    select = sql.get_type_length(photo_type)
    if select[0][0] != 0:
        return select

    
    select = sql.get_authority_type_length(photo_type)
    if select[0][0] != 0:
        return select

    
    return [0]


@api.route("/access/code", methods=["post", "get"])
def access_code():
    

    def formats(s):
        
        res = []
        for item in s:
            temp = {"id": item[0], "user": item[1], "code": item[2]}
            res.append(temp)
        return res

    if not util.is_login(session):
        
        return {"status": "ok", "meg": "not logged in"}, 403

    sql = Sql().connect("util/sql")
    select = sql.select_access_code_all()

    if select:
        return {"code": 0, "msg": "", "count": len(select), "data": formats(select)}
    return {"code": 0, "msg": "", "count": 0, "data": []}


@api.route("/add/code", methods=["post", "get"])
def add_code():
    
    if not util.is_login(session):
        
        return {"status": "ok", "meg": "not logged in"}, 403

    user = request.form.get("user")
    if user != "user" and user != "admin":
        return {"code": 403, "msg": "参数错误"}, 403

    sql = Sql().connect("util/sql")
    if sql.insert_access_code(user, util.get_random_md5(user)):
        return {"code": 200, "msg": "ok"}
    return {"code": 200, "msg": "error"}


@api.route("/del/code", methods=["post", "get"])
def del_code():
    
    if not util.is_login(session):
        
        return {"status": "ok", "meg": "not logged in"}, 403

    auth_code = request.form.get("code")

    sql = Sql().connect("util/sql")
    status = sql.delete_access_code(auth_code)

    if status:
        return {"code": 200, "msg": "ok"}
    else:
        return {"code": 200, "msg": "error"}


@api.route("/del/photo", methods=["post", "get"])
def del_photo():
    
    if not util.is_login(session):
        
        return {"status": "ok", "meg": "not logged in"}, 403

    md_name = request.form.get("md")

    sql = Sql().connect("util/sql")
    status = sql.select_photo_md_name(md_name)
    if status:
        util.del_photo_file(status[3], status[4])
        status = sql.delete_photo(md_name)
    if status:
        return {"code": 200, "msg": "ok"}
    else:
        return {"code": 200, "msg": "error"}
