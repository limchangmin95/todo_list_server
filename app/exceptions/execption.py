##
## 検索結果が取得できない場合に発生させるException
##
class RecordNotFoundError(Exception):
    def __init__(self, msg:str = None):
        self.msg = msg

##
## バリデーションチェックにてエラーの場合に発生させるException
##
class ValidateError(Exception):
    def __init__(self, msg:str = None):
        return_msg = msg
        if type(msg) is list:
            return_msg = ", ".join([str(m) for m in msg])
        self.msg = return_msg

##
## 認証エラー場合に発生させるException
##
class AuthenticationError(Exception):
    def __init__(self, msg:str = None):
        self.msg = msg

##
## ファイル操作エラーの場合に発生させるException
##
class FileError(Exception):
    def __init__(self, msg:str = None):
        self.msg = msg

##
## SQL操作エラーの場合に発生させるException
##
class SqlError(Exception):
    def __init__(self, msg:str = None):
        self.msg = msg