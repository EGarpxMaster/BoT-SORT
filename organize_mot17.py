# Script para organizar secuencias MOT17-13 y MOT17-14
import shutil
import os
from pathlib import Path

def organize_mot17_sequences():
    """Organizar las secuencias específicas MOT17-13-SDP y MOT17-14-SDP"""
    
    # Rutas base
    mot17_base = Path("datasets/MOT17")
    
    # Mapeo de secuencias a sus ubicaciones finales
    sequences_mapping = {
        # Entrenamiento
        "MOT17-13-SDP": "train",
        "MOT17-13-DPM": "train", 
        "MOT17-13-FRCNN": "train",
        
        # Test
        "MOT17-14-SDP": "test",
        "MOT17-14-DPM": "test",
        "MOT17-14-FRCNN": "test"
    }
    
    print("🔄 Organizando secuencias MOT17...")
    
    # Buscar secuencias en la estructura extraída
    for root, dirs, files in os.walk("datasets"):
        for dir_name in dirs:
            if any(seq in dir_name for seq in ["MOT17-13", "MOT17-14"]):
                source_path = Path(root) / dir_name
                
                # Determinar si es train o test
                if "MOT17-13" in dir_name:
                    split = "train"
                elif "MOT17-14" in dir_name:
                    split = "test"
                else:
                    continue
                
                # Crear destino
                dest_path = mot17_base / split / dir_name
                dest_path.mkdir(parents=True, exist_ok=True)
                
                print(f"📂 Copiando {dir_name} a {split}/")
                
                # Copiar contenido
                try:
                    if source_path.exists():
                        for item in source_path.iterdir():
                            dest_item = dest_path / item.name
                            if item.is_dir():
                                shutil.copytree(item, dest_item, dirs_exist_ok=True)
                            else:
                                shutil.copy2(item, dest_item)
                        print(f"✅ {dir_name} copiado exitosamente")
                    else:
                        print(f"❌ {source_path} no encontrado")
                except Exception as e:
                    print(f"❌ Error copiando {dir_name}: {e}")
    
    # Verificar estructura final
    print("\n📋 Verificando estructura final:")
    for split in ["train", "test"]:
        split_path = mot17_base / split
        if split_path.exists():
            print(f"\n{split.upper()}:")
            for seq_dir in split_path.iterdir():
                if seq_dir.is_dir():
                    img_count = len(list((seq_dir / "img1").glob("*.jpg"))) if (seq_dir / "img1").exists() else 0
                    gt_exists = (seq_dir / "gt" / "gt.txt").exists()
                    print(f"  📁 {seq_dir.name}: {img_count} imágenes, GT: {'✅' if gt_exists else '❌'}")

def create_annotation_files():
    """Crear archivos de anotación necesarios para entrenamiento"""
    
    print("\n🏷️ Creando archivos de anotación...")
    
    # Verificar que tenemos las secuencias
    train_seq = Path("datasets/MOT17/train/MOT17-13-SDP")
    test_seq = Path("datasets/MOT17/test/MOT17-14-SDP")
    
    if train_seq.exists():
        print(f"✅ Secuencia de entrenamiento encontrada: {train_seq}")
        
    if test_seq.exists():
        print(f"✅ Secuencia de test encontrada: {test_seq}")
    
    print("""
🎯 Configuración MOT17 completada:

ENTRENAMIENTO (MOT17-13-SDP):
• 750 frames @ 25 FPS (30 segundos)
• 1920x1080 resolución
• 110 peatones, 11,642 bounding boxes
• Escena: Intersección desde bus

TEST (MOT17-14-SDP):
• 750 frames @ 25 FPS (30 segundos)  
• 1920x1080 resolución
• 164 peatones, 18,483 bounding boxes
• Escena: Intersección desde bus

📌 Próximos pasos:
1. Convertir a formato COCO: python tools/datasets/convert_mot17_to_coco.py
2. Entrenar detector: python tools/train.py -f yolox/exps/example/mot/yolox_x_mix_det.py
3. Evaluar: python tools/track.py datasets/MOT17 --benchmark MOT17
    """)

if __name__ == "__main__":
    organize_mot17_sequences()
    create_annotation_files()