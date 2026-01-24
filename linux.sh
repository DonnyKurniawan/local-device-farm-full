## run this first chmod +x run_server.sh
## before executing linux.sh

#!/bin/bash
source venv/Scripts/activate
uvicorn main:app --reload