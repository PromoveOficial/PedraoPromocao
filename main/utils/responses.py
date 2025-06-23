class Response(Exception):
    def __init__(self, code, status):
        self.code = code
        self.status = status
    
    def __str__(self):
        return f"{self.code}: {self.status}"
   
# Response for succeffully completed request 
class RequestComplete(Response):
    def __init__(self, response_data=None):
        code = 200
        status = "Ok"
        self.content = ({"Code": code, "Status": status}, code)
        if response_data is not None:
            self.content[0]["Content"] = response_data
            
        super().__init__(code, status)


# Error response requisites
class RequestError(Response):
    def __init__(self, code, message, status):
        self.message = message
        self.content = ({"Code": code, "Status:": status, "Message": message}, code)

        super().__init__(code, status)   
        
    def __str__(self):
        return  f"[{self.code}: {self.status}] {self.message}"
      
class MethodNotAllowed(RequestError):
    def __init__(self, parameters):
        code = 400
        status = "Bad Request"
        message = f"The server don't proccess that type of request."
        super().__init__(code, message, status)
        
class NoParameter(RequestError):
    def __init__(self, parameters):
        code = 400
        status = "Bad Request"
        message = f"Parameter(s): {parameters} missing."
        super().__init__(code, message, status)
        
class ExceptionalError(RequestError):
    def __init__(self):
        code = 500
        status = "Internal Server Error"
        message = "Server encontered an uncaught error, please contact the administrator"
        super().__init__(code, message, status)