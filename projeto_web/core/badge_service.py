import os
import io
from typing import Optional
from PIL import Image, ImageDraw, ImageFont


class BadgeService:
    """Serviço gerador de carteirinhas e crachás digitais em imagem oficial de alta resolução."""

    @staticmethod
    def _create_circular_image(
        img: Image.Image,
        size: int,
        border_color=(0, 229, 255),
        border_width: int = 3,
    ) -> Image.Image:
        """Recorta imagem em círculo com suavização e borda destacada."""
        img_rgba = img.convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0, size - 1, size - 1), fill=255)

        circular = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        circular.paste(img_rgba, (0, 0), mask)

        draw_circ = ImageDraw.Draw(circular)
        for w in range(border_width):
            draw_circ.ellipse(
                (w, w, size - 1 - w, size - 1 - w),
                outline=border_color,
            )
        return circular

    @classmethod
    def gerar_imagem_carteirinha(
        cls,
        nome: str,
        email: str,
        instituicao: str = "Universidade Federal do Cariri (UFCA)",
        modalidade: str = "Presencial",
        role: str = "participante",
        codigo: str = "ASTRO-001",
        email_confirmado: bool = True,
        foto_url: Optional[str] = None,
        base_assets_path: str = "assets",
    ) -> bytes:
        """Gera imagem PNG da carteirinha oficial do IV EFAC usando estritamente as 3 imagens autorizadas:

        1. assets/logo_ivefac.jpeg
        2. assets/favicon.png (Soldadinho-do-Araripe)
        3. assets/cariri_cosmico_banner.jpeg (Cariri Cósmico)
        """
        W, H = 960, 520
        base = Image.new("RGBA", (W, H), (6, 11, 23, 255))

        # 1. Textura de fundo: Cariri Cósmico com overlay escuro cósmico
        banner_path = os.path.join(base_assets_path, "cariri_cosmico_banner.jpeg")
        if os.path.exists(banner_path):
            try:
                bg = Image.open(banner_path).convert("RGBA")
                bg = bg.resize((W, H), Image.Resampling.LANCZOS)
                overlay = Image.new("RGBA", (W, H), (6, 11, 23, 215))
                base = Image.alpha_composite(bg, overlay)
            except Exception:
                pass

        draw = ImageDraw.Draw(base)

        # 2. Resolução de fontes do sistema com fallback
        def get_font(size: int, bold: bool = False):
            font_candidates = [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf" if bold else "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
            ]
            for fc in font_candidates:
                if os.path.exists(fc):
                    try:
                        return ImageFont.truetype(fc, size)
                    except Exception:
                        pass
            return ImageFont.load_default()

        font_title = get_font(22, bold=True)
        font_sub = get_font(13, bold=False)
        font_badge_head = get_font(12, bold=True)
        font_name = get_font(26, bold=True)
        font_email = get_font(15, bold=False)
        font_inst = get_font(15, bold=False)
        font_pill = get_font(12, bold=True)
        font_footer = get_font(14, bold=True)

        card_margin = 16
        card_rect = [card_margin, card_margin, W - card_margin, H - card_margin]

        # Moldura externa em ciano com brilho
        draw.rounded_rectangle(card_rect, radius=22, outline=(0, 173, 181, 190), width=2)

        # 3. Cabeçalho: Logo Oficial do IV EFAC
        logo_path = os.path.join(base_assets_path, "logo_ivefac.jpeg")
        if os.path.exists(logo_path):
            try:
                logo_raw = Image.open(logo_path)
                logo_circ = cls._create_circular_image(logo_raw, size=48, border_color=(0, 173, 181), border_width=2)
                base.paste(logo_circ, (card_margin + 24, card_margin + 20), logo_circ)
            except Exception:
                pass

        # Textos do cabeçalho
        draw.text((card_margin + 84, card_margin + 20), "IV EFAC 2026", fill=(255, 255, 255), font=font_title)
        draw.text((card_margin + 84, card_margin + 48), "Universidade Federal do Cariri • Campus Brejo Santo", fill=(148, 163, 184), font=font_sub)

        # Badge "CARTEIRINHA OFICIAL"
        badge_txt = "CARTEIRINHA OFICIAL"
        bbox = font_badge_head.getbbox(badge_txt)
        bw, bh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        px, py = 16, 7
        bx2 = W - card_margin - 24
        bx1 = bx2 - bw - (px * 2)
        by1 = card_margin + 26
        by2 = by1 + bh + (py * 2)
        draw.rounded_rectangle([bx1, by1, bx2, by2], radius=12, fill=(0, 173, 181, 255))
        draw.text((bx1 + px, by1 + py - 1), badge_txt, fill=(255, 255, 255), font=font_badge_head)

        # Linha divisória
        draw.line([(card_margin + 20, card_margin + 82), (W - card_margin - 20, card_margin + 82)], fill=(0, 173, 181, 70), width=1)

        # 4. Corpo Central: Avatar
        avatar_size = 136
        avatar_x = card_margin + 28
        avatar_y = card_margin + 110

        fav_path = os.path.join(base_assets_path, "favicon.png")
        avatar_source_path = fav_path if os.path.exists(fav_path) else logo_path

        # Se houver foto_url válida no disco
        if foto_url and os.path.exists(foto_url):
            avatar_source_path = foto_url

        try:
            raw_av = Image.open(avatar_source_path)
            # Anéis de brilho orbital ciano
            for glow in range(4):
                draw.ellipse(
                    [avatar_x - glow, avatar_y - glow, avatar_x + avatar_size + glow, avatar_y + avatar_size + glow],
                    outline=(0, 173, 181, 75),
                )
            circ_av = cls._create_circular_image(raw_av, size=avatar_size, border_color=(0, 229, 255), border_width=3)
            base.paste(circ_av, (avatar_x, avatar_y), circ_av)
        except Exception:
            pass

        # Textos do participante
        text_x = avatar_x + avatar_size + 28
        nome_display = (nome[:34] + "...") if len(nome) > 37 else nome
        inst_display = (instituicao[:46] + "...") if len(instituicao) > 49 else instituicao

        draw.text((text_x, avatar_y + 4), nome_display, fill=(255, 255, 255), font=font_name)
        draw.text((text_x, avatar_y + 44), email, fill=(203, 213, 225), font=font_email)
        draw.text((text_x, avatar_y + 69), inst_display, fill=(148, 163, 184), font=font_inst)

        # Badges / Pills
        role_label = "ADMIN" if role.lower() == "admin" else ("SUPERVISOR" if role.lower() == "supervisor" else "PARTICIPANTE")
        pills = [
            (modalidade, (30, 58, 138), (147, 197, 253)),
            (role_label, (88, 28, 135), (216, 180, 254)),
            (codigo, (8, 47, 73), (56, 189, 248)),
        ]
        if email_confirmado:
            pills.append(("E-MAIL CONFIRMADO", (6, 78, 59), (110, 231, 183)))
        else:
            pills.append(("E-MAIL PENDENTE", (120, 53, 15), (253, 230, 138)))

        pill_x = text_x
        pill_y = avatar_y + 102
        for ptext, bg_col, text_col in pills:
            pbox = font_pill.getbbox(ptext)
            pw = pbox[2] - pbox[0]
            p_w = pw + 20
            p_h = 28
            draw.rounded_rectangle([pill_x, pill_y, pill_x + p_w, pill_y + p_h], radius=8, fill=bg_col, outline=text_col, width=1)
            draw.text((pill_x + 10, pill_y + 6), ptext, fill=text_col, font=font_pill)
            pill_x += p_w + 10

        # 5. Rodapé Informativo Oficial
        foot_y1 = H - card_margin - 75
        foot_y2 = H - card_margin - 20
        draw.rounded_rectangle([card_margin + 20, foot_y1, W - card_margin - 20, foot_y2], radius=12, fill=(0, 0, 0, 160), outline=(255, 255, 255, 30), width=1)

        draw.text((card_margin + 42, foot_y1 + 18), "11 e 12 Nov 2026", fill=(255, 255, 255), font=font_footer)
        draw.text((card_margin + 215, foot_y1 + 18), "•   08h00 Abertura", fill=(245, 158, 11), font=font_footer)

        # Emblema do Soldadinho-do-Araripe no rodapé
        if os.path.exists(fav_path):
            try:
                fav_icon = Image.open(fav_path).convert("RGBA").resize((28, 28), Image.Resampling.LANCZOS)
                base.paste(fav_icon, (W - card_margin - 230, foot_y1 + 14), fav_icon)
            except Exception:
                pass

        draw.text((W - card_margin - 190, foot_y1 + 18), "Fomento FUNCAP", fill=(56, 189, 248), font=font_footer)

        # Exporta buffer em PNG
        buffer = io.BytesIO()
        base.save(buffer, format="PNG", optimize=True)
        return buffer.getvalue()
