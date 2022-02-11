from pan_identification import clear_data as cl

cl.xml2csv('./docs/05-01/file.xml','train.csv','./docs/05-01/pan12-sexual-predator-identification-training-corpus-predators-2012-05-01.txt')
cl.xml2csv('./docs/05-21/pan12-sexual-predator-identification-test-corpus-2012-05-17.xml','test.csv','./docs/05-21/pan12-sexual-predator-identification-groundtruth-problem1.txt')




