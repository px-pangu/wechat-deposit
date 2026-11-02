# -*- coding: utf-8 -*-
"""ima 知识库文件上传助手（微信沉淀流程第 2 步专用）

用法: python ima_upload.py <本地文件路径>
前置: 先调 mcp__ima-mcp__create_media 拿到 media_id 和 cos_credential，
      把 credential JSON 存为同目录 cos_credential.json，本脚本读取后上传。
上传成功后(HTTP 200) 再调 mcp__ima-mcp__add_knowledge 入库。
"""
import hmac, hashlib, sys, json, os, urllib.request

def upload(file_path, cred_path=None):
    cred_path = cred_path or os.path.join(os.path.dirname(os.path.abspath(__file__)), "cos_credential.json")
    cred = json.load(open(cred_path, encoding="utf-8"))
    secret_id, secret_key, token = cred["secret_id"], cred["secret_key"], cred["token"]
    key_time = f"{cred['start_time']};{cred['expired_time']}"
    cos_key = "/" + cred["cos_key"]
    bucket, region = cred["bucket_name"], cred["region"]

    sign_key = hmac.new(secret_key.encode(), key_time.encode(), hashlib.sha1).hexdigest()
    http_string = "put\n" + cos_key + "\n\n\n"
    string_to_sign = "sha1\n" + key_time + "\n" + hashlib.sha1(http_string.encode()).hexdigest() + "\n"
    signature = hmac.new(sign_key.encode(), string_to_sign.encode(), hashlib.sha1).hexdigest()
    auth = (f"q-sign-algorithm=sha1&q-ak={secret_id}&q-sign-time={key_time}"
            f"&q-key-time={key_time}&q-header-list=&q-url-param-list=&q-signature={signature}")

    data = open(file_path, "rb").read()
    url = f"https://{bucket}.cos.{region}.myqcloud.com{cos_key}"
    req = urllib.request.Request(url, data=data, method="PUT", headers={
        "Authorization": auth,
        "x-cos-security-token": token,
        "Content-Type": "text/markdown",
    })
    try:
        r = urllib.request.urlopen(req, timeout=30)
        print("HTTP", r.status)
        return r.status == 200
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read()[:300])
        return False

if __name__ == "__main__":
    ok = upload(sys.argv[1])
    sys.exit(0 if ok else 1)
