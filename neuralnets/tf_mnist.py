import tensorflow as tf
import data


#Preprocessing is in data.py
input_size, output_size, train_images, train_labels, test_images, test_labels, encoding = data.mnist.Preprocessed()

#Tensorflow Model (Optimizer defaults: keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False))
inputs = tf.placeholder('float', [None, input_size])

layer_one_weights = tf.Variable(tf.random_normal([input_size, input_size]))
layer_one_biases = tf.Variable(tf.random_normal([input_size]))
layer_one = tf.add(tf.matmul(inputs, layer_one_weights), layer_one_biases)

layer_two_weights = tf.Variable(tf.random_normal([input_size, input_size]))
layer_two_biases = tf.Variable(tf.random_normal([input_size]))
layer_two = tf.add(tf.matmul(layer_one, layer_two_weights), layer_two_biases)

output_weights = tf.Variable(tf.random_normal([input_size, output_size]))
output_biases = tf.Variable(tf.random_normal([output_size]))
output_layer = tf.add(tf.matmul(layer_two, output_weights), output_biases)

outputs = tf.placeholder('float', [None, output_size])

#Compiling
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=outputs, logits=output_layer))
optimizer = tf.train.AdamOptimizer()
Adam = optimizer.minimize(loss)

correct_pred = tf.equal(tf.argmax(output_layer, 1), tf.argmax(outputs, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

#Training
init = tf.global_variables_initializer()
epochs = 50
batch_size = 32

with tf.Session() as sess:
    sess.run(init)

    for epoch in range(epochs):
        for batch_images, batch_labels in data.mnist.batch_generator(train_images, train_labels, batch_size):
            sess.run(Adam, feed_dict={inputs: batch_images, outputs: batch_labels})
        train_loss, train_acc = sess.run([loss, accuracy], feed_dict={inputs: train_images, outputs: train_labels})
        test_loss, test_acc = sess.run([loss, accuracy], feed_dict={inputs: test_images, outputs: test_labels})
        print(f'Epoch: {epoch}/{epochs}; train_loss[{train_loss}], train_acc[{train_acc}]; test_loss[{test_loss}], test_acc[{test_acc}]')

##Output_________________________________________________________
'''
2019-03-22 07:22:49.656579: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2
2019-03-22 07:22:49.858819: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1432] Found device 0 with properties:
name: GeForce GTX 1060 6GB major: 6 minor: 1 memoryClockRate(GHz): 1.7715
pciBusID: 0000:01:00.0
totalMemory: 6.00GiB freeMemory: 4.97GiB
2019-03-22 07:22:49.866827: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1511] Adding visible gpu devices: 0
2019-03-22 07:22:50.950197: I tensorflow/core/common_runtime/gpu/gpu_device.cc:982] Device interconnect StreamExecutor with strength 1 edge matrix:
2019-03-22 07:22:50.955802: I tensorflow/core/common_runtime/gpu/gpu_device.cc:988]      0
2019-03-22 07:22:50.958251: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1001] 0:   N
2019-03-22 07:22:50.960904: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1115] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 4722 MB memory) -> physical GPU (device: 0, name: GeForce GTX 1060 6GB, pci bus id: 0000:01:00.0, compute capability: 6.1)
Epoch: 0/50; train_loss[679.4781494140625], train_acc[0.8414999842643738]; test_loss[698.4910888671875], test_acc[0.8445000052452087]
Epoch: 1/50; train_loss[659.043212890625], train_acc[0.8346666693687439]; test_loss[699.1253051757812], test_acc[0.8348000049591064]
Epoch: 2/50; train_loss[708.8068237304688], train_acc[0.8228499889373779]; test_loss[733.6817016601562], test_acc[0.8194000124931335]
Epoch: 3/50; train_loss[425.76409912109375], train_acc[0.8514500260353088]; test_loss[464.8275451660156], test_acc[0.8465999960899353]
Epoch: 4/50; train_loss[472.8392639160156], train_acc[0.8283166885375977]; test_loss[501.180908203125], test_acc[0.8241000175476074]
Epoch: 5/50; train_loss[345.0437927246094], train_acc[0.8464000225067139]; test_loss[372.1823425292969], test_acc[0.8410999774932861]
Epoch: 6/50; train_loss[286.31719970703125], train_acc[0.8452833294868469]; test_loss[316.90875244140625], test_acc[0.8381999731063843]
Epoch: 7/50; train_loss[242.88687133789062], train_acc[0.861383318901062]; test_loss[263.3294372558594], test_acc[0.8568000197410583]
Epoch: 8/50; train_loss[208.4999237060547], train_acc[0.8535833358764648]; test_loss[229.90687561035156], test_acc[0.8479999899864197]
Epoch: 9/50; train_loss[227.26565551757812], train_acc[0.8410500288009644]; test_loss[235.6376190185547], test_acc[0.8446999788284302]
Epoch: 10/50; train_loss[158.46636962890625], train_acc[0.8688333630561829]; test_loss[168.26573181152344], test_acc[0.8668000102043152]
Epoch: 11/50; train_loss[179.7455291748047], train_acc[0.8461833596229553]; test_loss[190.54798889160156], test_acc[0.8403000235557556]
Epoch: 12/50; train_loss[178.5465850830078], train_acc[0.8532666563987732]; test_loss[188.2456817626953], test_acc[0.8495000004768372]
Epoch: 13/50; train_loss[171.51744079589844], train_acc[0.84211665391922]; test_loss[178.66058349609375], test_acc[0.8391000032424927]
Epoch: 14/50; train_loss[160.42013549804688], train_acc[0.8518166542053223]; test_loss[168.6334228515625], test_acc[0.8453999757766724]
Epoch: 15/50; train_loss[143.6382293701172], train_acc[0.8528666496276855]; test_loss[152.89212036132812], test_acc[0.8501999974250793]
Epoch: 16/50; train_loss[141.41775512695312], train_acc[0.8427666425704956]; test_loss[145.22459411621094], test_acc[0.8446000218391418]
Epoch: 17/50; train_loss[117.1258773803711], train_acc[0.8625333309173584]; test_loss[125.75789642333984], test_acc[0.8610000014305115]
Epoch: 18/50; train_loss[134.06129455566406], train_acc[0.8517166376113892]; test_loss[144.22103881835938], test_acc[0.847100019454956]
Epoch: 19/50; train_loss[110.76831817626953], train_acc[0.85958331823349]; test_loss[114.22927856445312], test_acc[0.861299991607666]
Epoch: 20/50; train_loss[108.2426986694336], train_acc[0.8615999817848206]; test_loss[116.24250030517578], test_acc[0.8600000143051147]
Epoch: 21/50; train_loss[94.91287994384766], train_acc[0.8737833499908447]; test_loss[100.50252532958984], test_acc[0.8726999759674072]
Epoch: 22/50; train_loss[88.26387023925781], train_acc[0.87704998254776]; test_loss[92.88973999023438], test_acc[0.8751000165939331]
Epoch: 23/50; train_loss[89.8887939453125], train_acc[0.8709166646003723]; test_loss[92.58656311035156], test_acc[0.8707000017166138]
Epoch: 24/50; train_loss[81.69200134277344], train_acc[0.8762166500091553]; test_loss[91.00631713867188], test_acc[0.8686000108718872]
Epoch: 25/50; train_loss[89.0246353149414], train_acc[0.8663166761398315]; test_loss[91.1844482421875], test_acc[0.8651999831199646]
Epoch: 26/50; train_loss[86.96221923828125], train_acc[0.8723833560943604]; test_loss[91.68904876708984], test_acc[0.8725000023841858]
Epoch: 27/50; train_loss[98.75393676757812], train_acc[0.8547000288963318]; test_loss[104.7952651977539], test_acc[0.8547000288963318]
Epoch: 28/50; train_loss[75.36837005615234], train_acc[0.8778499960899353]; test_loss[80.5854721069336], test_acc[0.8755000233650208]
Epoch: 29/50; train_loss[72.58419799804688], train_acc[0.8794666528701782]; test_loss[77.1629867553711], test_acc[0.8810999989509583]
Epoch: 30/50; train_loss[69.17871856689453], train_acc[0.8777333498001099]; test_loss[75.01496124267578], test_acc[0.8733000159263611]
Epoch: 31/50; train_loss[73.73016357421875], train_acc[0.87131667137146]; test_loss[80.21397399902344], test_acc[0.8705000281333923]
Epoch: 32/50; train_loss[74.4863052368164], train_acc[0.8682666420936584]; test_loss[81.48678588867188], test_acc[0.8622000217437744]
Epoch: 33/50; train_loss[68.55094146728516], train_acc[0.8729666471481323]; test_loss[73.104736328125], test_acc[0.8658999800682068]
Epoch: 34/50; train_loss[86.61263275146484], train_acc[0.8432833552360535]; test_loss[89.23570251464844], test_acc[0.8471999764442444]
Epoch: 35/50; train_loss[65.32014465332031], train_acc[0.8744166493415833]; test_loss[68.58329010009766], test_acc[0.8737999796867371]
Epoch: 36/50; train_loss[59.27821731567383], train_acc[0.8817499876022339]; test_loss[63.25797653198242], test_acc[0.8830000162124634]
Epoch: 37/50; train_loss[58.638397216796875], train_acc[0.8803666830062866]; test_loss[63.626731872558594], test_acc[0.8781999945640564]
Epoch: 38/50; train_loss[59.5523681640625], train_acc[0.8766833543777466]; test_loss[64.62117767333984], test_acc[0.8708999752998352]
Epoch: 39/50; train_loss[60.04511260986328], train_acc[0.8793166875839233]; test_loss[66.13821411132812], test_acc[0.8730999827384949]
Epoch: 40/50; train_loss[59.71062469482422], train_acc[0.8713333606719971]; test_loss[62.47817611694336], test_acc[0.8701000213623047]
Epoch: 41/50; train_loss[56.81840515136719], train_acc[0.867733359336853]; test_loss[61.48023223876953], test_acc[0.8651999831199646]
Epoch: 42/50; train_loss[54.96495056152344], train_acc[0.878516674041748]; test_loss[57.55722427368164], test_acc[0.8799999952316284]
Epoch: 43/50; train_loss[56.74094009399414], train_acc[0.8691333532333374]; test_loss[59.197776794433594], test_acc[0.8676999807357788]
Epoch: 44/50; train_loss[50.91102981567383], train_acc[0.8769999742507935]; test_loss[54.736106872558594], test_acc[0.8720999956130981]
Epoch: 45/50; train_loss[55.615699768066406], train_acc[0.8708000183105469]; test_loss[58.032161712646484], test_acc[0.8701000213623047]
Epoch: 46/50; train_loss[60.1709098815918], train_acc[0.8488333225250244]; test_loss[62.3625373840332], test_acc[0.8468999862670898]
Epoch: 47/50; train_loss[49.65067672729492], train_acc[0.8734666705131531]; test_loss[53.47548294067383], test_acc[0.8694999814033508]
Epoch: 48/50; train_loss[51.72876739501953], train_acc[0.868066668510437]; test_loss[55.343143463134766], test_acc[0.8675000071525574]
Epoch: 49/50; train_loss[43.79388427734375], train_acc[0.881850004196167]; test_loss[47.43747329711914], test_acc[0.8813999891281128]
'''
