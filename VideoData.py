import os
from PIL import Image
import hashlib
import numpy as np

class VideoData():
    def encode(file_name):
        try:
           with open(file_name, 'rb') as f:
               file_data = f.read().hex()        
        except FileNotFoundError:
            print('File not found. Please enter a valid file name!')
            return 
        
        BUF_SIZE = 65536

        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        
        with open(file_name, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)

        print("MD5: {0}".format(md5.hexdigest()))
        print("SHA1: {0}".format(sha1.hexdigest()))

        print('ENCODING')
                
        pixel_array = [[file_data[i:i+2], file_data[i+2:i+4], file_data[i+4:i+6]] for i in range(0, len(file_data), 6)]
        
        for index, colors in enumerate(pixel_array):
            for color_index, color in enumerate(colors):
                try:
                    pixel_array[index][color_index] = int(color, 16)
                except ValueError:
                    pixel_array[index][color_index] = 0
            pixel_array[index] = (pixel_array[index][0], pixel_array[index][1],pixel_array[index][2])
        
        resolution = int(len(pixel_array)**0.5) + 1
        count = 0
        for x in range(resolution):
            for y in range(resolution):
                try:
                    _x = pixel_array[(x*resolution)+y]
                except IndexError:
                    count += 1
                    pixel_array.append((0, 0, 0))

        if count == 0:
            pixel_array.append([(0, 0, 0) for x in range(resolution)])
            
        count = hex(count).replace('0x', '')
        pixel_array.pop()
        data_length = [count[:2], count[2:4], count[4:6]]
        for index, item in enumerate(data_length):
            try:
                data_length[index] = int(item, 16)
            except ValueError:
                data_length[index] = 0        
        pixel_array.append(data_length)
        pixel_array = [pixel_array[i:i+resolution] for i in range(0, len(pixel_array), resolution)]
        
        array = np.array(pixel_array, dtype=np.uint8)
        new_image = Image.fromarray(array)
        new_image.save(file_name + '.png')
        
    def decode(image_name):
        print('DECODING')

        image_data = Image.open(image_name)
        array = np.array(image_data)
        array = np.concatenate(array, axis=0)
        index = array[-1].tolist()
        data_length = int(hex(index[2]) + hex(index[1]).replace('0x', '') + hex(index[0]).replace('0x', ''), 16)
        data_array = np.concatenate(array, axis=None).tolist()
        data = data_array[:len(data_array)-(data_length*3)-1]
        
        if not os.path.isdir('extract'):
            os.mkdir('extract')
        
        with open('extract\\\\'+image_name.replace('.png', ''), 'wb') as f:
            for x in data:
                f.write(bytes((x,)))
        
        BUF_SIZE = 65536

        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        
        with open('extract\\\\'+image_name.replace('.png', ''), 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
                sha1.update(data)
        
        print("MD5: {0}".format(md5.hexdigest()))
        print("SHA1: {0}".format(sha1.hexdigest()))