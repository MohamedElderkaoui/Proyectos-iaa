import zipfile
import re

path = r"c:\III DIPLOMA DE EXTENSIÓN UNIVERSITARIA EN INTELIGENCIA ARTIFICIAL AVANZADA SAMSUNG INNOVATION CAMPUS (2025-26)\MÓDULO 10. Proyectos\Theme3.thmx"
with zipfile.ZipFile(path) as z:
    xml = z.read('theme/theme/theme1.xml').decode('utf-8', 'ignore')
    print('--- THEME FILE ---')
    print(xml[:2000])
    colors = sorted(set(re.findall(r'val="([A-Fa-f0-9]{6})"', xml)))
    print('\n--- COLORS ---')
    for color in colors:
        print(color)
