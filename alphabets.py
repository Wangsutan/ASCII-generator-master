from typing import Dict, Any


languages: Dict[str, Dict[str, Any]] = {
    "general": {
        "chars": {
            "simple": "@%#*+=-:. ",
            "complex": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
        },
        "font_path": "fonts/DejaVuSansMono-Bold.ttf",
        "sample_char": "A",
        "size": 20,
        "scale": 2,
    },
    "english": {
        "chars": {"standard": "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"},
        "font_path": "fonts/DejaVuSansMono-Bold.ttf",
        "sample_char": "A",
        "size": 20,
        "scale": 2,
    },
    "german": {
        "chars": {
            "standard": "AaÄäBbßCcDdEeFfGgHhIiJjKkLlMmNnOoÖöPpQqRrSsTtUuÜüVvWwXxYyZz"
        },
        "font_path": "fonts/DejaVuSansMono-Bold.ttf",
        "sample_char": "A",
        "size": 20,
        "scale": 2,
    },
    "french": {
        "chars": {
            "standard": "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzÆæŒœÇçÀàÂâÉéÈèÊêËëÎîÎïÔôÛûÙùŸÿ"
        },
        "font_path": "fonts/DejaVuSansMono-Bold.ttf",
        "sample_char": "A",
        "size": 20,
        "scale": 2,
    },
    "italian": {
        "chars": {
            "standard": "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzÀÈàèéìòù"
        },
        "font_path": "fontsequenceejaVuSansMono-Bold.ttf",
        "sample_char": "A",
        "size": 20,
        "scale": 2,
    },
    "polish": {
        "chars": {
            "standard": "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpRrSsTtUuWwYyZzĄąĘęÓóŁłŃńŻżŚśĆćŹź"
        },
        "font_path": "fonts/DejaVuSansMono-Bold.ttf",
        "sample_char": "A",
        "size": 20,
        "scale": 2,
    },
    "portuguese": {
        "chars": {
            "standard": "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzàÀáÁâÂãÃçÇéÉêÊíÍóÓôÔõÕúÚ"
        },
        "font_path": "fonts/Deimage_outputjaVuSansMono-Bold.ttf",
        "sample_char": "A",
        "size": 20,
        "scale": 2,
    },
    "spanish": {
        "chars": {
            "standard": "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZzÑñáéíóú¡¿"
        },
        "font_path": "fonts/DejaVuSansMono-Bold.ttf",
        "sample_char": "A",
        "size": 20,
        "scale": 2,
    },
    "russian": {
        "chars": {
            "standard": "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯя"
        },
        "font_path": "fonts/DejaVuSansMono-Bold.ttf",
        "sample_char": "Ш",
        "size": 20,
        "scale": 2,
    },
    "chinese": {
        "chars": {
            "interesting": "龍龘龖䲜𨰻靐麤鱻驫䯂馫飍灥鑫森淼焱垚猋犇骉羴蟲飝囍林从花鸟虫鱼天地人孔乙己之乎者也〇卍回一二三亖丶灬",
            "standard": "龘䶑瀰幗獼鑭躙䵹觿䲔釅欄鐮䥯鶒獭鰽襽螻鰱蹦屭繩圇婹歜剛屧磕媿慪像僭堳噞呱棒偁呣塙唑浠唼刻凌咄亟拮俗参坒估这聿布允仫忖玗甴木亪女去凸五圹亐囗弌九人亏产斗丩艹刂彳丬了５丄三亻讠厂丆丨１二宀冖乛一丶、",
        },
        "font_path": "fonts/simsun.ttc",
        "sample_char": "国",
        "size": 20,
        "scale": 1,
    },
    "korean": {
        "chars": {"standard": "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣ"},
        "font_path": "fonts/arial-unicode.ttf",
        "sample_char": "ㅊ",
        "size": 20,
        "scale": 1,
    },
    "japanese": {
        "chars": {
            "hiragana": "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん",
            "katakana": "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン",
        },
        "font_path": "fonts/arial-unicode.ttf",
        "sample_char": "お",
        "size": 20,
        "scale": 1,
    },
}
