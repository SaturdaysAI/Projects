import torch
import pandas as pd

from functions_transform import fft_transform, border_transform


def getDatasetIDS(dataset, subset):
    """
     Given a dataset and a subset of the dataset return a dataframe with the IDs of the dataset and the subset.

     Args:
          dataset: list of ( inputs labels id ) tuples as returned by get_dataset
          subset: name of the subset to return. It is used to determine the order of the dataset

     Returns: 
          pandas. DataFrame with the
    """

        # for i, data in enumerate(validation_set, 0):
        #     inputs, labels, id = data
        #     ids.append(id)    
    ids = []
    # for data in dataset:
    #     inputs, labels, id = data
    #     ids.append([id, subset])
    # for i, data in enumerate(dataset, 0):
    #     inputs, labels, id = data
    #     ids.append(id)        
    # ids=np.array(ids)
    for i in range(len(dataset)):  
        inputs, labels, id = dataset[i]
        ids.append([id, subset])  
    return pd.DataFrame(ids, columns=['ID', 'SUBSET'])


class CustomTransform(object):
    def __init__(self, split_percent=0.5):
        """
         Initialize the class. This is called by __init__ and should not be called directly. The split_percent determines how much to split the data into two parts before passing it to _split_by_part ().

         Args:
              split_percent: The percentage of data to split the dataset by
        """
        self.split_percent = split_percent

    # Defining the transform method
    def __call__(self, image):
        """
         Transforms the image returns the result. This is a wrapper around the fft_transform and border_transform functions

         Args:
              image: torch. Tensor of shape [ height width  ]

         Returns: 
              torch. Tensor of shape [channels height width  ] where channels is the channels of the input image
        """
        # Splitting the image into two parts

        image1 = fft_transform(image)
        image2 = border_transform(image)

        # Returning the two parts of the image
        return torch.tensor(image, dtype=torch.float32), torch.tensor(image1, dtype=torch.float32), torch.tensor(image2, dtype=torch.float32)


# aqui habra que utilizar de lista de tipos de imgagen
class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, data, transform=None, image_type='FSL_SEG', image_number=1, BCE=True):
        """
         Initialize the object with data. This is the entry point for the class. It should be called by the user to initialize the object

         Args:
              data: Data that will be used to create the image
              transform: Transformation to apply to the image before it is saved
              image_type: Type of the image ( FSL_SEG RAW etc. )
              image_number: Number of the image ( 1 for all except RAW )
              BCE: Whether or not to use BCE ( True)
        """
        self.data = data
        self.transform = transform
        self.image_type = image_type
        self.image_number = image_number
        self.BCE = BCE
        # self.img_labels = image_dict_orig

    def __len__(self):
        """
         Returns the number of elements in the array. This is a wrapper around len ( self. data )


         Returns: 
              The number of elements
        """
        return len(self.data)

    def __getitem__(self, idx):
        """
         Returns the image at the given index. This is a PyTorch function and should not be used directly

         Args:
              idx: Index of the image to return

         Returns: 
              A tuple of the image and the label for the given index ( if BCE is True ) or None
        """
        # print(self.data['0001'])
        # image_array = self.data[idx]['i'][1]['image']
        # print(self.data.keys())
        image_array = self.data[idx]['1'][f'{self.image_type}'][self.image_number]['original']
        # Convert the 2D array to a PyTorch tensor
        tensor_image = torch.tensor(image_array, dtype=torch.float32)
        if self.BCE:
            # logits require a list
            label = torch.tensor([self.data[idx]['1']["Dementia"]])
        else:
            label = torch.tensor(self.data[idx]['1']["Dementia"])

        id = self.data[idx]['1']["ID"]

        # Applying the transform
        if self.transform:
            tensor_image1, tensor_image2, tensor_image3 = self.transform(
                image_array)
            tensor_image = torch.stack(
                (tensor_image1, tensor_image2, tensor_image3))
        return tensor_image, label, id
