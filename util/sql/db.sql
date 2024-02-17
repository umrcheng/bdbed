CREATE TABLE IF NOT EXISTS photo -- 图片表
(
    id          INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
    md_name     TEXT     NOT NULL UNIQUE, -- 图片md5名
    path        TEXT     NOT NULL UNIQUE, -- 图片本地相对地址
    src         TEXT     NOT NULL,        -- 图片web路径
    name        TEXT     NOT NULL,        -- 图片文件名
    suffix      TEXT     NOT NULL,        -- 文件后缀
    authority   TEXT     NOT NULL,        -- 权限
    type        TEXT,                     -- 图片类别
    create_time DATETIME NOT NULL DEFAULT current_timestamp
);

CREATE TABLE IF NOT EXISTS access_code
(
    id          INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
    user        TEXT     NOT NULL,
    code        TEXT     NOT NULL UNIQUE,
    create_time DATETIME NOT NULL DEFAULT current_timestamp
);

-- 用户表，暂时用不到
-- CREATE TABLE IF NOT EXISTS user -- 用户表
-- (
--     id            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
--     mail          TEXT    NOT NULL UNIQUE,         -- 邮箱地址
--     password      TEXT    NOT NULL UNIQUE,         -- 密码
--     nickname      TEXT    NOT NULL DEFAULT '用户', -- 昵称
--     administrator INTEGER NOT NULL DEFAULT 0,      --  是否为管理员
--     avatar        TEXT                             -- 头像地址
-- );
-- -- 管理员账户信息
-- INSERT INTO user (mail, password, nickname, administrator)
-- VALUES ('admin@admin.com', '123456', '管理员', 1);
