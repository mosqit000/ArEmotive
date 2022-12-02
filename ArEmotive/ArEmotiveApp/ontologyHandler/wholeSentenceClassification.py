import ArEmotiveApp.ontologyHandler.huggingFace as hf

sentence = "يقال أن الاحتباس  الحراري مؤذي و مو منيح ذو سيطرة"
myLabels = ['متعة', 'غضب', 'خوف', 'حب', 'تفهم', 'رضا', 'تطلع', 'اهتمام', 'مفاجآة', 'اشمئزاز', 'محايد', 'لا_مبالاة',
            'حزن']
hf.classifyMultiClass(sentence,myLabels,4)