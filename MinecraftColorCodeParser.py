class MinecraftColorCodeParser:
    COLOR_CODES = {
        '§0': 'black',
        '§1': 'dark_blue',
        '§2': 'dark_green',
        '§3': 'dark_aqua',
        '§4': 'dark_red',
        '§5': 'dark_purple',
        '§6': 'gold',
        '§7': 'gray',
        '§8': 'dark_gray',
        '§9': 'blue',
        '§a': 'green',
        '§b': 'aqua',
        '§c': 'red',
        '§d': 'light_purple',
        '§e': 'yellow',
        '§f': 'white'
    }

    @staticmethod
    def parse_color_codes(text):
        for code, color in MinecraftColorCodeParser.COLOR_CODES.items():
            text = text.replace(code, f'[{color}]')
        return text

if __name__ == "__main__":
    parser = MinecraftColorCodeParser()
    print(parser.parse_color_codes('§1This is some §2colored §etext§f!'))