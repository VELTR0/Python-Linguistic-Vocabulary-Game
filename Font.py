import pygame

# Just a class to make a custom Font
class SpriteFont:
    def __init__(self, font_path=None, *, space_width=6, trim=True):
        if font_path is None:
            font_path = r"Sprites\Font\Font.png"

        self.sheet = pygame.image.load(font_path).convert_alpha()
        self.bg = self.sheet.get_at((0, 0))
        self.space_width = space_width
        self.trim = trim
        self.symbols = {}
        self.height = 0
        row_bands = self.find_row_bands()

        # sets the symbols from font
        layout = [
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrs",
            "tuvwxyzÂÁÀÄÇÊÉÈËÎÍÌÏÑÔÓÒÕŒÛÚÙÜâáàäçêéèëîíìïñôóòö",
            "æûúùüß%&☆★+_×÷=<>0123456789,.:;?!~()",
        ]


        # searches for gaps to seperate symbols
        for band_index, (y0, y1) in enumerate(row_bands):
            chars_in_row = layout[band_index]
            symbol_rects = self.find_symbol_rects_in_band(y0, y1)

            row_height = (y1 - y0)
            self.height = max(self.height, row_height)

            for ch, rect in zip(chars_in_row, symbol_rects):
                symbol = self._extract_symbol(rect, row_height=row_height)
                self.symbols[ch] = symbol

        if " " in self.symbols:
            self.space_width = self.symbols[" "].get_width()

    def get(self, ch: str):
        return self.symbols.get(ch)

    def render(
        self,
        text: str,
        *,
        color=None,
        scale=1,
        spacing=1,
        line_spacing=2,
        bg=None,
    ) -> pygame.Surface:

        lines = text.split("\n")
        if not lines:
            lines = [""]

        line_widths = []
        for line in lines:
            w = 0
            for ch in line:
                if ch == " ":
                    w += self.space_width + spacing
                else:
                    g = self.symbols.get(ch)
                    if g is None:
                        w += self.space_width + spacing
                    else:
                        w += g.get_width() + spacing
            w = max(0, w - spacing)
            line_widths.append(w)

        width = max(line_widths) if line_widths else 0
        height = len(lines) * self.height + (len(lines) - 1) * line_spacing

        if width <= 0:
            width = 1
        if height <= 0:
            height = 1

        out_w = int(round(width * scale))
        out_h = int(round(height * scale))
        out = pygame.Surface((out_w, out_h), pygame.SRCALPHA)

        if bg is not None:
            out.fill(bg)

        y = 0
        for line in lines:
            x = 0
            for ch in line:
                if ch == " ":
                    x += self.space_width + spacing
                    continue

                symbol = self.symbols.get(ch)
                if symbol is None:
                    x += self.space_width + spacing
                    continue

                g = symbol

                if color is not None and isinstance(color, (tuple, list)) and len(color) == 2:
                    text_color, outline_color = color
                    g = self.recolor_fill_and_outline(symbol, text_color, outline_color)
                elif color is not None:
                    g = self._tint(symbol, color)


                # Lets the Symbols allign to the bottom of the line
                y_draw = y + (self.height - symbol.get_height())

                if scale == 1:
                    out.blit(g, (x, y_draw))
                else:
                    scaled = pygame.transform.scale(
                        g,
                        (
                            int(round(g.get_width() * scale)),
                            int(round(g.get_height() * scale)),
                        ),
                    )
                    out.blit(
                        scaled,
                        (int(round(x * scale)), int(round(y_draw * scale))),
                    )

                x += symbol.get_width() + spacing

            y += self.height + line_spacing

        return out

    def _is_bg(self, color):
        return color == self.bg

    def find_row_bands(self):
        w, h = self.sheet.get_size()
        bands = []
        in_band = False
        y0 = 0

        for y in range(h):
            has_pixel = False
            for x in range(w):
                if not self._is_bg(self.sheet.get_at((x, y))):
                    has_pixel = True
                    break

            if has_pixel and not in_band:
                in_band = True
                y0 = y
            elif not has_pixel and in_band:
                in_band = False
                bands.append((y0, y))
        if in_band:
            bands.append((y0, h))

        return bands

    def find_symbol_rects_in_band(self, y0, y1):
        w, _ = self.sheet.get_size()
        rects = []
        in_symbol = False
        x0 = 0

        for x in range(w):
            has_pixel = False
            for y in range(y0, y1):
                if not self._is_bg(self.sheet.get_at((x, y))):
                    has_pixel = True
                    break

            if has_pixel and not in_symbol:
                in_symbol = True
                x0 = x
            elif not has_pixel and in_symbol:
                in_symbol = False
                rects.append(pygame.Rect(x0, y0, x - x0, y1 - y0))

        if in_symbol:
            rects.append(pygame.Rect(x0, y0, w - x0, y1 - y0))

        return rects

    def _extract_symbol(self, rect: pygame.Rect, *, row_height: int):
        symbol = pygame.Surface((rect.w, row_height), pygame.SRCALPHA)

        symbol.blit(self.sheet, (0, 0), rect)

        # remove background
        px = pygame.PixelArray(symbol)
        bg_mapped = symbol.map_rgb(self.bg)
        px.replace(bg_mapped, (0, 0, 0, 0))
        del px

        if self.trim:
            symbol = self.trim_surface_horizontal(symbol)

        return symbol

    def trim_surface_horizontal(self, surf: pygame.Surface):
        bbox = surf.get_bounding_rect(min_alpha=1)
        if bbox.w == 0:
            return surf

        trimmed = pygame.Surface((bbox.w, surf.get_height()), pygame.SRCALPHA)
        trimmed.blit(surf, (0, 0), pygame.Rect(bbox.x, 0, bbox.w, surf.get_height()))
        return trimmed

    def _tint(self, surf: pygame.Surface, color):
        tinted = surf.copy()
        tinted.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
        return tinted
    
    def recolor_fill_and_outline(
        self,
        surf: pygame.Surface,
        fill_color,
        outline_color,
        outline_src_color=(0, 0, 0),
    ):
        recolored = pygame.Surface(surf.get_size(), pygame.SRCALPHA)

        w, h = surf.get_size()
        for y in range(h):
            for x in range(w):
                r, g, b, a = surf.get_at((x, y))
                if a == 0:
                    continue

                if (r, g, b) == outline_src_color:
                    recolored.set_at((x, y), (*outline_color, a))
                else:
                    recolored.set_at((x, y), (*fill_color, a))

        return recolored

