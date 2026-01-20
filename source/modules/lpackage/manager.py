import os
import json
import brotli
import struct
from pathlib import Path
from typing import Dict, List, Any, Callable, Optional


class LPackage:    
    MAGIC_NUMBER = b'LPKG'
    VERSION = 1
    
    @staticmethod
    def compress(source_path: str, output_path: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        source = Path(source_path)
        
        if not source.exists():
            raise FileNotFoundError(f"No existe: {source_path}")
        
        files_data = []
        total_size = 0
        
        if source.is_file():
            files_to_process = [(source.name, source)]
        else:
            files_to_process = []
            for root, _, files in os.walk(source):
                for file in files:
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(source)
                    files_to_process.append((str(rel_path), file_path))
        
        for rel_path, file_path in files_to_process:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            compressed = brotli.compress(content, quality=11)
            
            files_data.append({
                'path': rel_path,
                'size': len(content),
                'compressed_size': len(compressed),
                'data': compressed
            })
            total_size += len(content)
        

        package_metadata = {
            'version': LPackage.VERSION,
            'file_count': len(files_data),
            'total_size': total_size,
            'compression_ratio': 0,
            'created_from': source_path,
            'user_metadata': metadata or {}
        }
        

        metadata_json = json.dumps(package_metadata, ensure_ascii=False).encode('utf-8')
        metadata_compressed = brotli.compress(metadata_json)
        

        index = [{
            'path': f['path'],
            'size': f['size'],
            'compressed_size': f['compressed_size']
        } for f in files_data]
        
        index_json = json.dumps(index, ensure_ascii=False).encode('utf-8')
        index_compressed = brotli.compress(index_json)
        

        with open(output_path, 'wb') as f:
            f.write(LPackage.MAGIC_NUMBER)
            f.write(struct.pack('<H', LPackage.VERSION))
            
            f.write(struct.pack('<I', len(metadata_compressed)))
            f.write(metadata_compressed)
            
            f.write(struct.pack('<I', len(index_compressed)))
            f.write(index_compressed)
            
            for file_data in files_data:
                f.write(struct.pack('<I', len(file_data['data'])))
                f.write(file_data['data'])
        

        compressed_total = sum(f['compressed_size'] for f in files_data)
        ratio = (1 - compressed_total / total_size) * 100 if total_size > 0 else 0
        package_metadata['compression_ratio'] = round(ratio, 2)
        
        return {
            'file_count': len(files_data),
            'original_size': total_size,
            'compressed_size': compressed_total,
            'compression_ratio': f"{ratio:.2f}%",
            'output_file': output_path
        }
    


    @staticmethod
    def decompress(package_path: str, output_dir: str) -> Dict[str, Any]:


        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)
        
        with open(package_path, 'rb') as f:
            magic = f.read(4)
            if magic != LPackage.MAGIC_NUMBER:
                raise ValueError("Archivo no es un .lpackage válido")
            
            version = struct.unpack('<H', f.read(2))[0]
            
            metadata_size = struct.unpack('<I', f.read(4))[0]
            metadata_compressed = f.read(metadata_size)
            metadata_json = brotli.decompress(metadata_compressed)
            metadata = json.loads(metadata_json.decode('utf-8'))
                        
            index_size = struct.unpack('<I', f.read(4))[0]
            index_compressed = f.read(index_size)
            index_json = brotli.decompress(index_compressed)
            index = json.loads(index_json.decode('utf-8'))
            
            extracted_files = []
            for i, file_info in enumerate(index):
                data_size = struct.unpack('<I', f.read(4))[0]
                compressed_data = f.read(data_size)
                
                decompressed_data = brotli.decompress(compressed_data)
                
                file_path = output / file_info['path']
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, 'wb') as out_file:
                    out_file.write(decompressed_data)
                
                extracted_files.append(str(file_path))
                        
        return {
            'metadata': metadata,
            'extracted_files': extracted_files,
            'file_count': len(extracted_files),
            'output_directory': str(output)
        }
    


    @staticmethod
    def get_metadata(package_path: str) -> Dict[str, Any]:
        with open(package_path, 'rb') as f:
            magic = f.read(4)
            if magic != LPackage.MAGIC_NUMBER:
                raise ValueError("Archivo no es un .lpackage válido")
            
            version = struct.unpack('<H', f.read(2))[0]
            
            metadata_size = struct.unpack('<I', f.read(4))[0]
            metadata_compressed = f.read(metadata_size)
            metadata_json = brotli.decompress(metadata_compressed)
            
            return json.loads(metadata_json.decode('utf-8'))