import Fetcher

class Handler:
    string = str()
    ftc = None

    #here the frame is semantical unit that need to be filled to return the command 
    # for opening the file it's need only filen name
    frame = {
        "name": ["Enter the name of the file", None], #None represents no value given
        "age":["Enter the type of the file", None]
    }
    def __init__(self, request):
        self.string = request     #input from the trandformer
        self.ftc = Fetcher.Fetch(self.string)  #passing the text of input given by user
        self.autoFill() #fills the slots in frame if there exits arguments in it
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
        

