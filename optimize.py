import tensorflow as tf
converter = tf.lite.TFLiteConverter.from_saved_model('/home/damo/PycharmProjects/APC/custom_model_david_2/model.tflite')
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_quant_model = converter.convert()