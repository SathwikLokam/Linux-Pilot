import Fetcher as ft

# Test text
text = """
Contact me at john.doe@example.com or visit my website at www.example.com. 
My server IP is 192.168.1.1, and my backup server is 2001:0db8:85a3:0000:0000:8a2e:0370:7334.
You can reach me at +1 5551234567 or (123) 456-7890.
I use port 80 for HTTP, 443 for HTTPS, and 21 for FTP. Use alpha.txt and beta.jpg
"""

fetcher=ft.Fetcher(text)

# Test the method
print(fetcher.st)