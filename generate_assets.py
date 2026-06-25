import os
from PIL import Image

def create_favicon(logo_path, favicon_ico_path, favicon_png_path):
    print("Criando favicons...")
    # Abre o logo original
    img = Image.open(logo_path)
    
    # Bounding box do ícone detectado: (2, 343, 166, 517)
    # Vamos recortar com uma pequena margem de segurança
    icon = img.crop((0, 330, 170, 530))
    
    # Encontra a bounding box real do ícone recortado para remover excesso de transparência
    bbox = icon.getbbox()
    if bbox:
        icon = icon.crop(bbox)
        
    # Torna o ícone quadrado adicionando preenchimento transparente
    w, h = icon.size
    max_dim = max(w, h)
    
    # Cria uma nova imagem quadrada transparente
    square_icon = Image.new("RGBA", (max_dim, max_dim), (0, 0, 0, 0))
    # Cola o ícone centralizado
    square_icon.paste(icon, ((max_dim - w) // 2, (max_dim - h) // 2))
    
    # Salva como PNG em tamanho padrão (32x32 e 192x192 para web/android)
    square_icon.resize((32, 32), Image.Resampling.LANCZOS).save(favicon_png_path)
    
    # Salva como ICO com múltiplos tamanhos
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    icon_imgs = [square_icon.resize(size, Image.Resampling.LANCZOS) for size in sizes]
    icon_imgs[0].save(favicon_ico_path, format="ICO", append_images=icon_imgs[1:])
    print(f"Favicons gerados: {favicon_ico_path} e {favicon_png_path}")

def create_og_image(logo_path, og_image_path):
    print("Criando imagem OG...")
    # Abre o logo original e recorta para o bounding box do conteúdo real
    img = Image.open(logo_path)
    bbox = img.getbbox()
    if bbox:
        img_cropped = img.crop(bbox)
    else:
        img_cropped = img
        
    # Redimensiona o logo cropped para caber de forma elegante na imagem OG (1200x630)
    # Vamos dar uma margem de segurança (ex: largura máxima de 800px, altura máxima de 350px)
    max_w, max_h = 800, 350
    w, h = img_cropped.size
    
    # Calcula proporção para manter aspect ratio
    ratio = min(max_w / w, max_h / h)
    new_size = (int(w * ratio), int(h * ratio))
    img_resized = img_cropped.resize(new_size, Image.Resampling.LANCZOS)
    
    # Cria fundo azul marinho (#0a1437) correspondente ao menu da Stilotech
    bg_color = (10, 20, 55, 255) # rgba(10, 20, 55, 1)
    og_canvas = Image.new("RGBA", (1200, 630), bg_color)
    
    # Centraliza o logo redimensionado no canvas
    paste_x = (1200 - new_size[0]) // 2
    paste_y = (630 - new_size[1]) // 2
    
    # Cola usando o próprio canal alpha como máscara para manter a transparência do logo
    og_canvas.paste(img_resized, (paste_x, paste_y), img_resized)
    
    # Converte para RGB antes de salvar como JPEG ou salva como PNG
    # PNG é ótimo para preservar transparência/qualidade, mas o ideal para OG é PNG ou JPEG
    og_canvas.convert("RGB").save(og_image_path, "JPEG", quality=95)
    print(f"Imagem OG gerada: {og_image_path}")

if __name__ == "__main__":
    logo = "logo.png"
    favicon_ico = "favicon.ico"
    favicon_png = "favicon.png"
    og_image = "og-image.jpg"
    
    if os.path.exists(logo):
        create_favicon(logo, favicon_ico, favicon_png)
        create_og_image(logo, og_image)
    else:
        print("Erro: logo.png não encontrado!")
