from tkinter import Tk
from ImageModel import ImageModel
from ImageViewModel import ImageViewModel
from ImageView import ImageView

if __name__ == "__main__":
    root = Tk()
    model = ImageModel()
    view_model = ImageViewModel(model)
    app = ImageView(root, view_model)
    root.mainloop()
