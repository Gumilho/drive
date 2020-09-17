from pathlib import Path
import os
a = Path(os.path.join(*["E:\\Users\\Documents\\mangos\\assigned\\","bom", "dia"]))
print(os.path.exists(a))