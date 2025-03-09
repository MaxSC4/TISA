import numpy as np
import os
from skimage import segmentation
from skimage.color import color_dict, label2rgb
import tensorflow as tf
from keras import layers, models, optimizers, losses
from sklearn.cluster import KMeans
from skimage.segmentation import find_boundaries


tf.config.threading.set_intra_op_parallelism_threads(2)
tf.config.threading.set_inter_op_parallelism_threads(2)


def perform_custom_segmentation(image, params):
    class Args(object):
        def __init__(self, params):
            self.train_epoch = params.get('train_epoch', 2 ** 3)
            self.mod_dim1 = params.get('mod_dim1', 64)
            self.mod_dim2 = params.get('mod_dim2', 32)
            self.gpu_id = params.get('gpu_id', 0)
            self.min_label_num = params.get('min_label_num', 6)
            self.max_label_num = params.get('max_label_num', 256)
            self.segmentation_method = params.get('segmentation_method', 'felzenszwalb')

    args = Args(params)

    def MyNet(inp_dim, mod_dim1, mod_dim2, seed=42):
        tf.random.set_seed(seed)
        
        inputs = layers.Input(shape=(None, None, inp_dim))
        
        print("1")
        # First convolutional block
        x = layers.Conv2D(mod_dim1, (3, 3), padding='same')(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)
        skip1 = x  # Skip connection 1
        
        
        print("2")
        # Second convolutional block
        x = layers.Conv2D(mod_dim2, (1, 1))(x)
        x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)

        print("3")        
        # Third convolutional block
        x = layers.Conv2D(mod_dim1, (3, 3), padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)
        skip2 = x  # Skip connection 2
        
        print("4")        
        # Fourth convolutional block
        x = layers.Conv2D(mod_dim2, (1, 1))(x)
        x = layers.BatchNormalization()(x)
        
        print("5")        
        # Adding skip connection 2
        skip2 = layers.Conv2D(mod_dim2, (1, 1))(skip2)
        skip2 = layers.BatchNormalization()(skip2)
        
        x = layers.Add()([x, skip2])
        x = layers.ReLU()(x)
        
        print("6")
        # Adding skip connection 1
        skip1 = layers.Conv2D(mod_dim2, (1, 1))(skip1)
        skip1 = layers.BatchNormalization()(skip1)
        
        x = layers.Add()([x, skip1])
        x = layers.ReLU()(x)
        
        model = models.Model(inputs=inputs, outputs=x)
        return model

    np.random.seed(1943)
    tf.random.set_seed(1943)
    os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu_id)

    print("ML")
    '''segmentation ML'''
    if args.segmentation_method == 'felzenszwalb':
        # Perform Felzenszwalb segmentation
        seg_map = segmentation.felzenszwalb(image, scale=15, sigma=0.06, min_size=14)
        seg_map = seg_map.flatten()
        seg_lab = [np.where(seg_map == u_label)[0]
                for u_label in np.unique(seg_map)]

        print("Felzen done")

        # Convert segmentation map to RGB image with boundaries
        segmented_image = label2rgb(seg_map.reshape(image.shape[:2]), image, kind='avg')
        boundaries = find_boundaries(seg_map.reshape(image.shape[:2]), mode='thick')
        segmented_image[boundaries] = [1, 0, 0]  # Red color for boundaries
        segmented_image = (segmented_image - segmented_image.min()) / (segmented_image.max() - segmented_image.min())
        
    elif args.segmentation_method == 'kmeans':
        # Perform KMeans clustering
        image_flatten = image.reshape((-1, 3))
        kmeans = KMeans(n_clusters=args.max_label_num, random_state=0).fit(image_flatten)
        seg_map = kmeans.labels_
        seg_lab = [np.where(seg_map == u_label)[0] for u_label in np.unique(seg_map)]


    # Set device to GPU if available, otherwise CPU
    device = '/GPU:0' if tf.config.list_physical_devices('GPU') else '/CPU:0'
    tensor = image.astype(np.float32) / 255.0
    tensor = np.expand_dims(tensor, axis=0)

    segmented_images = []


    with tf.device(device):
        # Initialize the model
        model = MyNet(inp_dim=3, mod_dim1=args.mod_dim1, mod_dim2=args.mod_dim2)
        criterion = losses.SparseCategoricalCrossentropy(from_logits=True)
        optimizer = optimizers.SGD(learning_rate=5e-2, momentum=0.9)

        image_flatten = image.reshape((-1, 3))
        color_avg = np.random.randint(255, size=(args.max_label_num, 3))
        show = image

        for batch_idx in range(args.train_epoch):
            with tf.GradientTape() as tape:
                output = model(tensor, training=True)[0]
                output = tf.reshape(output, (-1, args.mod_dim2))
                target = tf.argmax(output, axis=1)
                im_target = target.numpy()

                # Update target labels based on segmentation
                for inds in seg_lab:
                    u_labels, hist = np.unique(im_target[inds], return_counts=True)
                    im_target[inds] = u_labels[np.argmax(hist)]

                target = tf.convert_to_tensor(im_target)
                loss = criterion(target, output)

            # Backward pass and optimization
            grads = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))

            # Update segmented image
            un_label, lab_inverse = np.unique(im_target, return_inverse=True)
            if un_label.shape[0] < args.max_label_num:
                img_flatten = image_flatten.copy()
                if len(color_avg) != un_label.shape[0]:
                    color_avg = [np.mean(img_flatten[im_target == label], axis=0, dtype=int) for label in un_label]
                for lab_id, color in enumerate(color_avg):
                    img_flatten[lab_inverse == lab_id] = color
                show = img_flatten.reshape(image.shape)


            segmented_images.append(show.copy())


    return segmented_images