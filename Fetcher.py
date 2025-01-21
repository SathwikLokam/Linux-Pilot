import re
import json

class Fetch:
    def __init__(self, string):
        self.string = string
        
        # Private Regex patterns for different types of data
        self.__email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        self.__ip_patternV4 = r"\d+\.\d+\.\d+\.\d+"
        self.__ip_patternV6 = r"(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|\b(?:[0-9a-fA-F]{1,4}:){1,7}:|\b::(?:[0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4}"
        self.__phone_pattern = r'\d{10}'
        self.__port_pattern = r'(6553[0-5]|655[0-2]\d|64[0-9]{3}|[1-5]?[0-9]{1,4})'
        self.__domain_pattern = r"(?<=\s)(?!\S+@)(?!\d+\.\d+\.\d+\.\d+)(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}(?=\s|[^\w\d])"
        self.__port_name_pattern = r'\b(?:FTP|HTTP|HTTPS|SSH|SMTP|IMAP|POP3|ICMP|DNS|Telnet|SFTP|SNMP|RDP)\b'
        self.__files_pattern = r"\b[A-Za-z0-9_-]+\.(?:txt|md|cfg|conf|tar(?:\.gz|\.bz2|\.xz|\.lzma)?|zip|rar|gz|xz|7z|out|bin|elf|run|sh|bash|zsh|fish|log|ini|png|jpg|jpeg|gif|bmp|svg|py|cpp|c|h|js|css|rb|php|java|iso|img|deb|rpm)\b"
    
    # Methods to fetch different types of data
    
    def ipv4s(self):
        return re.findall(self.__ip_patternV4, self.string)
    
    def ipv6s(self):
        return re.findall(self.__ip_patternV6, self.string)
    
    def phone_ns(self):
        return re.findall(self.__phone_pattern, self.string)
    
    def port_ns(self):
        return re.findall(self.__port_pattern, self.string)
    
    def port_names(self):
        return re.findall(self.__port_name_pattern, self.string)
    
    def files(self):
        return re.findall(self.__files_pattern, self.string)
    
    def web(self):
        return re.findall(self.__domain_pattern, self.string)
    
    # New method to return the extracted data in JSON format
    def get_all(self):
        # Prepare a dictionary with the results
        fetched_arguments = {
            "emails": self.web(),
            "ipv4_addresses": self.ipv4s(),
            "ipv6_addresses": self.ipv6s(),
            "phone_numbers": self.phone_ns(),
            "port_numbers": self.port_ns(),
            "port_names": self.port_names(),
            "files": self.files()
        }
        
        # Return the data as a JSON string
        return fetched_arguments
