import Fetcher

class Handler:
    string = str()
    ftc = None
    frame = {
        "name": ["Enter the name of the file", None],
        "age":["Enter the type of the file", None]
    }
    def __init__(self, request):
        self.string = request
        self.ftc = Fetcher.Fetcher(self.string)
        self.autoFill()
    def autoFill(self):
        self.frame["name"][1]=self.ftc.files()[0] # list of files but i'm fetching first value
    def fill(self):
        for key, value in self.frame.items():
            if value[1] is None:
                user_input = input(f"{value[0]}: ")
                if user_input not in ["exit","quit"]:
                    self.frame[key][1]=user_input
                else:
                    return ["The creation of payload is terminated",0] # here 0 indicates it failed to create payload
        return ["open "+self.frame["name"][1],1] # here 1 indicates is successfull in creating payload
        

