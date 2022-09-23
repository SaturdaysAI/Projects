# -*- coding: utf-8 -*-
import os
import time

class Config:
    
    def __init__(self, mode_demo = False):
        self.mode_demo = mode_demo
        self.reset_timestamp()
        
        if (mode_demo):
            self.NFolds = 2
            self.epochs = 2
            self.epoch_loop = 1
            self.segment = 1
            self.data_demo = 100
            self.tta_cycles= 1


    #######################################################################
    #   1.  GENERAL  FLOW  CONTROL                                             
    #######################################################################
    verbose             = 1             # Verbose Level (0-7)

    process_datatrain   = True          # Load Train Dataset from Global Dataset
    process_datatest    = False         # Load Test Dataset from Global Dataset
    
    segmentation        = False         # Train Dataset Segmentation
    data_segment        = 1             # Number of segments on Train Dataset

    check_integrity     = False         # Performe Check Data Integrity

    loop_reset          = True          # Reset IA Model after loops
    
    #######################################################################
    #   2.  DATA  PROCESS
    #######################################################################
    
    # PROJECT SPECIFIC PARAMETERS
    data_SIZEGLOBAL     = 2049
    data_SIZELOCAL      = 257
    
    # DATA SOURCE PARAMETERS
    data_SIZE_X         = 224
    data_SIZE_Y         = 224
    data_CHANNELS       = 3
    data_shape          = (data_SIZE_X, data_SIZE_Y, data_CHANNELS)         # Shape of the Train/Test Original Data
    data_target_id_size = 0
    data_target_select  = 0                               
    
    # PREPROCESSING DATA PARAMETERS
    data_preprocess     = True
    data_normal         = 'local'       # None, 'local', 'global'
    data_space          = 'channel'     # 'channel', 'spatial', 'plane'
    data_space_channels = 3             # 3 o 6

    # DATA TRANSFORMATION
    data_resampling     = None          # Data Resampling
                                        # OPTIONS: None 'FalseNegative', 'FalseNegative_drop', 'Target_1'
    data_augment        = False          # Data Augmentation    
    data_augment_p      = 1.0           
    
    data_mixup          = False         # Data Mixup
    data_mixup_p        = 0.1
    data_mixup_count    = 0
    mixup_alpha         = 1.0
    
    data_resize         = None         
    data_cutout         = None
        
    #######################################################################
    #  3.  IA MODEL
    #######################################################################
    
    # MODEL SELECTION
    MODEL_TYPE          = ['custom', 'pretrained', 'generic']
    
    CUSTOM              = ['exoplanet', 'exoplanet_2D']
    
    PRETRAINED          = ['EfficientNetB0', 'EfficientNetB1','EfficientNetB2', 'EfficientNetB3','EfficientNetB4', 'EfficientNetB5',
                           'InceptionV3','InceptionResNetV2',
                           'ResNet50', 'ResNet50V2','ResNet101','ResNet101V2', 'ResNet152', 'ResNet152V2',
                           'Xception', 'VGG16', 'DenseNet121',
                           'MobileNet','MobileNetV2']
    
    GENERIC             = ['Bidireccional', 'AutoEncoder']
        
    model_type          = MODEL_TYPE[2]
    model_id            = GENERIC[1]
    
    if (model_type == MODEL_TYPE[2]) and (model_id == GENERIC[1]):
        unsupervised        = True
    else:
        unsupervised        = False
        
    first_layer         = None    #'Conv2D'
    conv2D_outchannels  = 3
    
    base_trainable      = 'last_block'              # None, 'full', 'last_block'
    layertrain          = 50
    dim_input           = 1                 # Input Branch of the IA Model
    loadweight          = False             # Load previous stored weight
    
    # DATA INPUT
    if (data_space == 'channel'):
        stride_x = 1
        img_size_X = data_shape[0]
        img_size_Y = data_shape[1]
        img_channels = data_shape[2]
            
    if (data_space  == 'spatial' or data_space  == 'plane'):
        stride_x = 3
        if (data_space  == 'spatial'):
            img_size_X = data_shape[2] * data_shape[0]
        else:
            img_size_X = data_shape[0]
        img_size_Y = data_shape[1]
        img_channels = 1
        
    input_shape        = (img_size_X, img_size_Y, img_channels)
    
    # MODEL OPTIONS
    dropout         = 0.0                    # Dropout Reference
    ACTIVATION      = ['sigmoid', 'softmax', 'relu', 'linear']
    activation      = ACTIVATION[3]          # Last Layer Activation
                                             # OPTIONS: 'softmax', 'sigmoid'
                                             # 'softmax' need a Crossentropy() loss function
    classes         = 1                      # Category Number
        
    # COMPILER OPTIONS
    OPTIMIZER      = ['Adam', 'AdamW']
    optimizer       = OPTIMIZER[0]
    
    LOSSFUNCTION    = ['Binary_CE', 'SigmoidFocal_CE', 'Categorical_CE',
                       'MeanSquaredError']
    from_logits     = False
    loss            = LOSSFUNCTION[3]
    
    METRIC         = ['Accuracy', 'AUC','Mean',
                      'CategoricalAccuracy','CategoricalCrossentropy',
                      'BinaryAccuracy','BinaryCrossentropy',
                      'CosineSimilarity']
    
    metric          = METRIC[7]
    
    #######################################################################
    #   4.  TRAININIG  PROCESS
    #######################################################################
    valid_split     = 0.1
    test_split      = 0.20                   
         
    folding         = False
    NFolds          = 5                     # Number of stratified Folds
    epochs          = 20
    batch           = 64
    epoch_loop      = 1                     # Training loops with same epochs
    class_weight    = None         # None, 'balanced', 'exponential'

    # CALLBACKS
    logging         = None                  # Logging path for Tensorboard

    lr_factor       = 0.00002
    learning_rate   = lr_factor * 10        # Learning Rate 
    lr_max          = lr_factor * 50        # Learning Rate 
    lr_min          = lr_factor * 3         # Learning Rate 
    lr_callback     = 'Experimental_01'     # Learning Rate Function
                                            # OPTIONS: None, 'Constant', 'Experimental_01'
                                            #          'ReduceLROnPlateau'
    lr_optimizer    = None                  # OPTIONS:  'Constant', 'CosineDecayRestarts', 'ExponentialDecay'
    early_stop      = 10                    # Early Stopping Patience
                                            # OPTIONS: None, INT with the value of Patience Early Stopping
    
   #######################################################################
    #   5.  TEST  AND  EVALUATION
    #######################################################################
    
    tta             = False              # Test-Time Augmentation
    tta_p           = 0.5               # TTA Percentage
    tta_cycles      = 4                 # Number of TTA Cycles
        
    #######################################################################
    #   6.  FILE  AND  STATISTICS
    #######################################################################    
    datapath        = 'D:/06.Datasets/ExoPlanet/'    # Data Source Base Path
    results     = './results'    # Results Path
    
    train_folder           = os.path.join(datapath, 'Train')
    target_folder          = os.path.join(datapath, 'Target')
    target_file            = os.path.join(target_folder, 'exodata_target.csv')   
    
    false_negative  = os.path.join(results, ''.join(['False_Negative.csv']))
    false_positive  = os.path.join(results, ''.join(['False_Positive.csv']))

    #######################################################################
    #   7.  UPDATE  PARAMETERS  FUNCTIONS
    #######################################################################

    def update_timestamp(self, fold = 0):
        if (self.model_id == 'pretrained'):
            self.model_name  = ''.join([self.pretrained, '_', self.timestamp])
        else:
            self.model_name  = ''.join([self.model_id, '_', self.timestamp])
        self.submission_FN   = os.path.join(self.resultspath, ''.join(['False_Negative',str(fold),'_', self.timestamp,'.csv']))  
        self.submission_FP   = os.path.join(self.resultspath, ''.join(['False_Positive',str(fold),'_', self.timestamp,'.csv']))  
        self.model_net       = os.path.join(self.resultspath, ''.join([self.model_name,'.json']))   # Structure Network Model File
        self.model_weight    = os.path.join(self.resultspath, ''.join([self.model_name,'.h5']))     # Weight File
        self.submission_fold = os.path.join(self.resultspath, ''.join(['submission_', self.model_name, '_',  str(fold), '.csv']))
    
        self.checkpoint      = os.path.join(self.resultspath, ''.join([self.model_name,'_check_',str(fold),'.h5']))  # Checkpoint Callback file
        
    def reset_timestamp(self):
        self.timestamp       = str(int(time.time()))
        self.resultspath = os.path.join(self.results, self.timestamp)
        if (self.model_id == 'pretrained'):
            self.model_name  = ''.join([self.pretrained, '_', self.timestamp])
        else:
            self.model_name  = ''.join([self.model_id, '_', self.timestamp])
            
        self.model_net       = os.path.join(self.resultspath, ''.join([self.model_name,'.json']))   # Structure Network Model File
        self.model_weight    = os.path.join(self.resultspath, ''.join([self.model_name,'.h5']))     # Weight File
        self.model_graph     = os.path.join(self.resultspath, ''.join([self.model_name,'.png']))    # Network Graph File
        self.model_cfg       = os.path.join(self.resultspath, ''.join([self.model_name,'.cfg']))    # Network Graph File
        self.submission      = os.path.join(self.resultspath, ''.join(['submission_', self.timestamp, '.csv']))
        
        self.update_timestamp()
        