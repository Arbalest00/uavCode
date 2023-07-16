import argparse
import os
import sys
from pathlib import Path
import torch
from models.common import DetectMultiBackend
from utils.dataloaders import  LoadImages
from utils.general import ( Profile, check_img_size, 
                         non_max_suppression, scale_boxes)
from utils.torch_utils import select_device, smart_inference_mode
import time

class yolo_det:
    FILE = Path(__file__).resolve()
    ROOT = FILE.parents[0]  # YOLOv5 root directory
    if str(ROOT) not in sys.path:
        sys.path.append(str(ROOT))  # add ROOT to PATH
    ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
    det_res = []

    @smart_inference_mode()
    def run(self,
            weights=None,  # model path or triton URL
            source=ROOT / 'data/images',  # file/dir/URL/glob/screen/0(webcam)
            data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
            imgsz=(640, 640),  # inference size (height, width)
            conf_thres=0.25,  # confidence threshold
            iou_thres=0.45,  # NMS IOU threshold
            max_det=4,  # maximum detections per image
            device='cpu',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
            classes=None,  # filter by class: --class 0, or --class 0 2 3
            agnostic_nms=False,  # class-agnostic NMS
            augment=False,  # augmented inference
            visualize=False,  # visualize features
            line_thickness=3,  # bounding box thickness (pixels)
            half=False,  # use FP16 half-precision inference
            dnn=False,  # use OpenCV DNN for ONNX inference
            vid_stride=1,  # video frame-rate stride
    ):
        source = str(source)
        # Load model
        device = select_device(device)
        model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
        stride, names, pt = model.stride, model.names, model.pt
        imgsz = check_img_size(imgsz, s=stride)  # check image size
        # Dataloader
        bs = 1  # batch_size
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
        # Run inference
        model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
        dt = (Profile(), Profile(), Profile())
        for path, im, im0s, vid_cap, s in dataset:
            with dt[0]:
                im = torch.from_numpy(im).to(model.device)
                im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
                im /= 255  # 0 - 255 to 0.0 - 1.0
                if len(im.shape) == 3:
                    im = im[None]  # expand for batch dim
            # Inference
            with dt[1]:
                pred = model(im, augment, visualize)
            # NMS
            with dt[2]:
                pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
            # Process predictions
            res_tmp = []
            for i, det in enumerate(pred):  # per image
                im0 = im0s.copy()
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()
                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        c = int(cls)  # integer class
                        conf = float(str(conf).replace('tensor(','').replace(')',''))
                        name = str(names[c])
                        if(name == 'red_pole'):
                            name = 1
                        elif(name == 'green_pole'):
                            name = 2
                        else:
                            name = 0
                        xyxy=str(xyxy).replace('tensor(','').replace('.)','').replace('[','').replace(']','').replace(' ','').split(',')
                        x_aver = (int(xyxy[0])+int(xyxy[2]))/2
                        y_aver = (int(xyxy[1])+int(xyxy[3]))/2
                        res_tmp.append([name,conf,x_aver,y_aver])
        self.det_res = res_tmp
        return self.det_res

    def parse_opt(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--weights', nargs='+', type=str, default=self.ROOT / 'best.onnx', help='model path or triton URL')
        parser.add_argument('--source', type=str, default=self.ROOT / 'test', help='file/dir/URL/glob/screen/0(webcam)')
        parser.add_argument('--data', type=str, default=self.ROOT / 'data/target.yaml', help='(optional) dataset.yaml path')
        parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
        parser.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
        parser.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
        opt = parser.parse_args()
        opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
        return opt

    def runtime(self):
        """
        其他函数不要管\n
        img保存到self.ROOT / 'test'文件夹下\n
        会自动读取的\n
        返回值: [[name,conf,x_aver,y_aver]]\n
        其中,name: 0-无杆,1-红杆,2-绿杆
        """
        opt = self.parse_opt()
        res = self.run(**vars(opt))
        return res


if __name__ == '__main__':
    ts = time.time()
    for i in range(1):
        res = yolo_det().runtime()
    print(res)
    te = time.time()-ts
    print(f'runtime: {te:.3f}s')
    fps = 1/te
    print(f'fps: {fps:.3f}')