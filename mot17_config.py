# Configuración de entrenamiento optimizada para RTX 4060
# MOT17-13-SDP (entrenamiento) y MOT17-14-SDP (test)

TRAINING_CONFIG = {
    # Optimizado para 8GB VRAM
    'batch_size': 4,          # Reducido para RTX 4060
    'num_workers': 6,         # i9-13900HX puede manejar esto
    'fp16': True,             # Half precision para ahorrar memoria
    'gradient_accumulation': 2, # Simular batch size mayor
    
    # Específico para MOT17
    'input_size': (800, 1440),
    'test_size': (800, 1440),
    'num_classes': 1,         # Solo personas
    'max_epoch': 80,
    'eval_interval': 5,
    
    # Learning rate optimizado
    'basic_lr_per_img': 0.001 / 64.0,
    'warmup_epochs': 5,
    'no_aug_epochs': 10,
}

TRACKING_CONFIG = {
    # Parámetros para MOT17 secuencias de intersección
    'track_thresh': 0.6,
    'track_buffer': 30,
    'match_thresh': 0.8,
    'min_box_area': 100,      # Aumentado para intersecciones
    
    # Camera motion compensation (importante para video desde bus)
    'cmc_method': 'orb',      # ORB funciona bien para movimiento de cámara
    
    # ReID para escenas complejas
    'with_reid': True,
    'proximity_thresh': 0.5,
    'appearance_thresh': 0.25,
}

# Comandos específicos para tu setup:
COMMANDS = {
    'train_detector': '''
python tools/train.py -f yolox/exps/example/mot/yolox_x_mix_det.py \\
    -d 1 -b 4 --fp16 \\
    -c pretrained/bytetrack_x_mot17.pth.tar \\
    --data_dir datasets/MOT17
    ''',
    
    'train_reid': '''
python fast_reid/tools/train_net.py \\
    --config-file fast_reid/configs/MOT17/sbs_S50.yml \\
    MODEL.DEVICE "cuda:0" \\
    SOLVER.IMS_PER_BATCH 32 \\
    SOLVER.MAX_ITER 20000
    ''',
    
    'test_mot17_14': '''
python tools/track.py datasets/MOT17 \\
    --default-parameters \\
    --with-reid \\
    --benchmark "MOT17" \\
    --eval "test" \\
    --fp16 --fuse \\
    --track_thresh 0.6 \\
    --cmc-method orb
    '''
}

print("Configuración lista para MOT17-13 (train) y MOT17-14 (test)")
print("RTX 4060 optimizado con 8GB VRAM")