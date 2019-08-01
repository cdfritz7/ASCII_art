# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 17:43:55 2018

@author: Connor
"""
import numpy as np
import cv2


class AsciiArtTransformer(object):

    """
    class for tranforming images and videos into black and white versions made
    only of ascii values
    ---------------------------------------------------------------------------
    Methods:
        __init__(self):
            Initializes necessary variables
            
        transform(self, media_dir, save_dir, file_type='img', fine=False)
            transforms image or video into ascii art and saves the new
            representation
            
        convert_ascii(self, frame, fine=False):
            transforms the frame (single image or video frame) into a
            representation consisting of ascii values
            
        gcf(self, num1, num2)
            returns the greatest common factor between num1 and num2, used in
            __init__
    ---------------------------------------------------------------------------
    """
    def __init__(self):
        """
        initializes variables
        Parameters:
            None
        Returns:
            None
        """
        letter_img = cv2.imread('tektite.png', 0)
        # in order of decreasing darkness @ # % *  | 1 ] + = - : .
        # longer list for future reference
        # @$#B%8&WM*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'.
        
        self.bw_vals = np.array([letter_img[31:43, 271:279], 
                                    letter_img[31:43, 307:315], 
                                    letter_img[31:43, 136:144], 
                                    letter_img[31:43, 163:171], 
                                    letter_img[31:43, 199:207], 
                                    letter_img[31:43, 217:225], 
                                    letter_img[31:43, 208:216], 
                                    letter_img[31:43, 262:270], 
                                    letter_img[31:43, 352:360]])
        self.dict_len = len(self.bw_vals)
        self.lwidth = self.bw_vals[0].shape[1]
        self.lheight = self.bw_vals[0].shape[0]
        self.m = self.gcf(self.lheight, self.lwidth)
                                                 
    def transform(self, media_dir, save_dir, file_type='image', fine=False):
        """            
            transforms image or video into ascii art and saves the new
            representation
            
            example call:
                asciiArtTransformerInstance.transform('./test.mp4', 
                                                      './test_out.mp4', 
                                                      file_type='video', 
                                                      fine=True)
                
            Parameters:
                media_dir: string, file path to the media file to be transformed
                save_dir: string, save directory where ascii version should be 
                            placed
                file_type: one of 'image' or 'video', what type of media is 
                           being transformed
                fine: boolean, if False, media is scaled at a 1:1 ratio, ie, the
                      output will have the same width and height as the original
                      if True, the media will be scaled at a 1:4 ratio, ie, the
                      output will have 4x the width and height of the input, and
                      will be more detailed
            Returns:
                None
                
            Throws:
                ValueError
        """
        try:
            if(file_type=='video'):
                vid = cv2.VideoCapture(media_dir)
                
                
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
                if(fine):
                    width, height = width*self.m, height*self.m
                frame_rate = vid.get(cv2.CAP_PROP_FPS)
                out = cv2.VideoWriter(save_dir, fourcc, frame_rate,
                                      (width, height), isColor=0)
                
                
                #if width is not 0, treat it as a video
                print("Video Conversion Started")
                while(vid.isOpened()):
                    ret, frame = vid.read()
                    if(ret == True):
                        #convert frame to text bits
                        frame = self.convert_ascii(frame, fine)
                        
                        #write converted frame
                        out.write(frame)
                    else:
                        break
                
                vid.release()
                out.release()
                print("Video Conversion Completed")
                
            elif(file_type=='image'):
                #if width is 0 treat it as an image
                img = cv2.imread(media_dir)
                img = self.convert_ascii(img, fine)
                img = cv2.cvtColor(img,  cv2.COLOR_GRAY2BGR); 
                cv2.imwrite(save_dir, img)
            else:
                raise ValueError
        except Exception:
            raise ValueError("""Invalid Arguments for 
AsciiArtTransformer.transform()""")
        
    def convert_ascii(self, frame, fine=False):
        """
        helper function to convert media into ascii versions
        
        example call:
            img = asciiTransformerInstance.convert_ascii(cv2.imread('./test1'),
                                                         fine=True)
            
        parameters:
            frame: ndarray of shape (n, m, 3) representing an rbg image or frame
            fine: boolean, fine = True makes a larger, relatively more detailed 
                  return image
        
        returns:
            holder: (n,m) representing a grayscale image composed of 'ascii 
                    characters'
        """
        
        #convert to grayscale
        grayscale = cv2.cvtColor(frame,  cv2.COLOR_BGR2GRAY); 
        
        #normalize grayscale matrix
        grayscale = (grayscale-np.min(grayscale))/(np.max(grayscale)-np.min(grayscale))-.01
        grayscale *= self.dict_len
        grayscale = grayscale.astype('uint8')
        
        #m is a scaling value
        if(fine):
            m=self.m
        else:
            m=1
            
        #calculate offset and create matrix to be returned
        row_offset = int(self.lheight/m)
        col_offset = int(self.lwidth/m)
        holder = np.zeros((grayscale.shape[0]*m, grayscale.shape[1]*m), 
                          dtype='uint8')
        
        #cycle through grayscale and transfer letter pics into holder based
        #on the values in grayscale
        i2 = 0
        for i in range(0, grayscale.shape[0]-row_offset, row_offset):
            j2 = 0
            for j in range(0, grayscale.shape[1]-col_offset, col_offset):
                idx = int(np.average(grayscale[i:i+row_offset, 
                                               j:j+col_offset]))
                letter_m = self.bw_vals[idx]
                if(i2 < holder.shape[0] and j2 < holder.shape[1]):
                    holder[i2:i2+self.lheight, j2:j2+self.lwidth] = letter_m
                else:
                    break
                j2+=self.lwidth
            i2+=self.lheight

        return holder
    
    def gcf(self, num1, num2):
        """
        returns the greatest common factor of parameters num1 and num2
        """
        if(num1 > num2):
            i = num2
        else:
            i = num1
        while(i > 1):
            if(num1%i == 0 and num2 % i == 0):
                return i
            i-=1
        return i
    
if(__name__ == '__main__'):
    a = AsciiArtTransformer()
    a.transform('./av.mp4', './av_out2.mp4', 
                file_type='video', fine=True)
            