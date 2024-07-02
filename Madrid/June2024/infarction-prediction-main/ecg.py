import numpy as np
from skimage.io import imread
from skimage import color
from skimage.filters import threshold_otsu, gaussian
from skimage.transform import resize
from skimage import measure
from sklearn.preprocessing import MinMaxScaler

class ECG:
    def __init__(self):
        self.leads = None

    def getImage(self, uploaded_file):
        return imread(uploaded_file)

    def GrayImage(self, img):
        return color.rgb2gray(img)

    def DividingLeads(self, img):
        leads = [
            img[300:600, 150:643], img[300:600, 646:1135], img[300:600, 1140:1625],
            img[300:600, 1630:2125], img[600:900, 150:643], img[600:900, 646:1135],
            img[600:900, 1140:1625], img[600:900, 1630:2125], img[900:1200, 150:643],
            img[900:1200, 646:1135], img[900:1200, 1140:1625], img[900:1200, 1630:2125],
            img[1250:1480, 150:2125]
        ]
        self.leads = leads
        return leads

    def PreprocessingLeads(self, leads):
        processed_leads = []
        for lead in leads:
            grayscale = color.rgb2gray(lead)
            blurred_image = gaussian(grayscale, sigma=0.9)
            global_thresh = threshold_otsu(blurred_image)
            binary_global = blurred_image < global_thresh
            binary_global = resize(binary_global, (300, 450))
            processed_leads.append(binary_global)
        return processed_leads

    def SignalExtraction_Scaling(self, leads):
        extracted_signals = []
        for lead in leads:
            contours = measure.find_contours(lead, 0.8)
            contours_shape = sorted([x.shape for x in contours])[::-1][0:1]
            for contour in contours:
                if contour.shape in contours_shape:
                    signal = resize(contour, (255, 2))
                    extracted_signals.append(signal[:, 0])
        return extracted_signals

    def CombineConvert1Dsignal(self, signals):
        scaler = MinMaxScaler()
        normalized_signals = [scaler.fit_transform(signal.reshape(-1, 1)).flatten() for signal in signals]
        return np.array(normalized_signals)

    def DimensionalReduction(self, signals):
        signals = np.transpose(signals)
        if signals.shape[1] < 12:
            while signals.shape[1] < 12:
                signals = np.c_[signals, np.zeros(signals.shape[0])]
        signals = signals[:, :12]
        if signals.shape[0] != 1000:
            signals = resize(signals, (1000, 12))
        return signals

    def ModelLoad_predict(self, signals, model):
        signals = np.expand_dims(signals, axis=0)
        prediction = model.predict(signals)
        return prediction
