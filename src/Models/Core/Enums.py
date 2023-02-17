from enum import Enum

class StatusCode(Enum):    
    PROCESSING = 102
    OK = 200    
    BAD_REQUEST = 400
    FORBIDDEN = 403
    NOT_FOUND = 404
    MULTIPLE_CHOICES = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    SERVICE_UNAVAILABLE = 503
    UNKNOWN = 600


    


    
