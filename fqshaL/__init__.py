import warnings
import numpy as np

# Temporary patch for openquake bug
setattr(np, 'RankWarning', UserWarning)

from .FQSHA import main

if __name__ == "__main__":
    main()

