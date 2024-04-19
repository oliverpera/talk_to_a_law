class UserConfiguration:
    def __init__(self, temperature, select, modelpath,textinput):
        self.temperature = temperature
        self.select = select
        self.modelpath = modelpath
        self.textinput = textinput
        
    def get_temperature(self):
        return self.temperature

    def set_temperature(self, temperature):
        self.temperature = temperature

    def get_select(self):
        return self.select

    def set_select(self, select):
        self.select = select
        
    def get_modelpath(self):
        return self.modelpath
    
    def set_modelpath(self, modelpath):
        self.modelpath = modelpath

    def get_textinput(self):
        return self.textinput

    def set_textinput(self, textinput):
        self.textinput = textinput
            


